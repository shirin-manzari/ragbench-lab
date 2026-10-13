"""Local Ollama generation diagnostics with pinned identity and explicit limits."""

from __future__ import annotations

import json
import math
import re
import socket
from dataclasses import asdict, dataclass
from datetime import datetime
from http.client import HTTPConnection, HTTPException
from pathlib import Path
from time import perf_counter
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse

from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256

INSTRUCTION = (
    "Answer the question using only the evidence below. Give a short answer. "
    "If the evidence is insufficient, answer exactly INSUFFICIENT_EVIDENCE."
)
ABSTENTION = "INSUFFICIENT_EVIDENCE"


def _invalid_number(token):
    raise DataError(f"non-finite JSON number from generation backend: {token}")


class _TimedResponse:
    def __init__(self, connection, response, transport, deadline):
        self.connection, self.response = connection, response
        self.transport, self.deadline = transport, deadline

    def _remaining(self):
        remaining = self.deadline - perf_counter()
        if remaining <= 0:
            raise TimeoutError("generation HTTP deadline exceeded")
        self.transport.settimeout(remaining)

    def read(self, size):
        self._remaining()
        return self.response.read(size)

    def readline(self, size):
        self._remaining()
        return self.response.readline(size)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.response.close()
        self.connection.close()


@dataclass(frozen=True)
class GeneratorSettings:
    model: str
    model_digest: str
    backend_version: str
    quantization: str
    tokenizer_revision: str
    tokenizer_files: dict[str, str]
    context_window: int = 4096
    maximum_output_tokens: int = 64
    timeout_seconds: float = 120.0
    seed: int = 20261011
    base_url: str = "http://127.0.0.1:11434"
    template_date: str = "12 Oct 2026"
    threads: int = 4

    def __post_init__(self):
        url = urlparse(self.base_url)
        if (url.scheme != "http" or url.hostname not in {"127.0.0.1", "localhost", "::1"}
                or url.username or url.password or url.path not in {"", "/"}
                or url.query or url.fragment):
            raise DataError("generation backend must be a local HTTP endpoint")
        if (not self.model or not re.fullmatch(r"[0-9a-f]{64}", self.model_digest)
                or not self.backend_version or not self.quantization
                or not re.fullmatch(r"[0-9a-f]{40}", self.tokenizer_revision)):
            raise DataError("pin model digest, backend, quantization and tokenizer revision")
        if (not {"tokenizer.json", "tokenizer_config.json"} <= self.tokenizer_files.keys()
                or any(Path(name).name != name or not re.fullmatch(r"[0-9a-f]{64}", value)
                       for name, value in self.tokenizer_files.items())):
            raise DataError("pin all native tokenizer inputs by filename and SHA-256")
        for name in ("context_window", "maximum_output_tokens", "threads"):
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise DataError(f"{name} must be a positive integer")
        if self.maximum_output_tokens >= self.context_window:
            raise DataError("output allowance must be smaller than the context window")
        if (type(self.timeout_seconds) not in {int, float}
                or not math.isfinite(self.timeout_seconds) or self.timeout_seconds <= 0):
            raise DataError("timeout must be finite and positive")
        if type(self.seed) is not int or not 0 <= self.seed < 2**32:
            raise DataError("seed must be an unsigned 32-bit integer")
        try:
            datetime.strptime(self.template_date, "%d %b %Y")
        except (ValueError, TypeError) as error:
            raise DataError("pin the template date in day/month-name/year form") from error


class GenerationError(DataError):
    def __init__(self, record: dict):
        self.record = record
        super().__init__(record["error"])


def load_native_tokenizer(directory: Path, settings: GeneratorSettings):
    # Acquisition is separate. Reject unpinned loader inputs and never download.
    inputs = {p.name for p in directory.iterdir()
              if p.is_file() and p.suffix in {".json", ".txt", ".model", ".jinja"}}
    if inputs != settings.tokenizer_files.keys():
        raise DataError("native tokenizer directory has missing or unpinned inputs")
    for name, expected in settings.tokenizer_files.items():
        if file_sha256(directory / name) != expected:
            raise DataError("native tokenizer file identity mismatch")
    from transformers import AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(directory, local_files_only=True,
                                              trust_remote_code=False)
    if not isinstance(tokenizer.chat_template, str) or not tokenizer.chat_template:
        raise DataError("one explicit native chat template is required")
    tokenizer.backend_tokenizer.no_truncation()
    tokenizer.backend_tokenizer.no_padding()
    return tokenizer


def render_prompt(tokenizer, question: str, context: str,
                  template_date: str, backend_add_bos: bool = False) -> tuple[str, int]:
    if not isinstance(question, str) or not question.strip() or not isinstance(context, str):
        raise DataError("generation requires question text and an explicit context string")
    messages = [{"role": "system", "content": INSTRUCTION},
                {"role": "user", "content": f"Evidence:\n{context}\n\nQuestion: {question}"}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True,
                                           date_string=template_date)
    if backend_add_bos:
        bos = tokenizer.bos_token
        if not isinstance(bos, str) or not bos:
            raise DataError("backend adds BOS but native tokenizer has no explicit BOS token")
        # Raw serving adds BOS itself. Send the template body to avoid two BOS tokens.
        if prompt.startswith(bos):
            prompt = prompt[len(bos):]
    ids = tokenizer.encode(prompt, add_special_tokens=False, truncation=False)
    return prompt, len(ids) + int(backend_add_bos)


class LocalGenerator:
    def __init__(self, settings: GeneratorSettings, tokenizer):
        self.settings, self.tokenizer = settings, tokenizer
        version = self._json("/api/version")["version"]
        tags = self._json("/api/tags")["models"]
        model = next((row for row in tags if row["name"] == settings.model), None)
        show = self._json("/api/show", {"model": settings.model})
        if (version != settings.backend_version or model is None
                or model["digest"] != settings.model_digest
                or show["details"]["quantization_level"] != settings.quantization):
            raise DataError("local generator identity differs from pinned settings")
        info = show["model_info"]
        if info["general.architecture"] not in {"qwen2", "llama"}:
            raise DataError("only the planned Qwen2 and Llama generator families are supported")
        maximum = info[f'{info["general.architecture"]}.context_length']
        if type(maximum) is not int or settings.context_window > maximum:
            raise DataError("configured generator context exceeds supported context length")
        self.backend_add_bos = info.get("tokenizer.ggml.add_bos_token",
                                        info["general.architecture"] == "llama")
        if type(self.backend_add_bos) is not bool:
            raise DataError("invalid backend BOS-token policy")
        self.identity = {
            "settings": asdict(settings), "show_sha256": digest(show),
            "chat_template_sha256": digest(tokenizer.chat_template),
            "instruction_sha256": digest(INSTRUCTION),
            "cache_policy": "unverified diagnostic; Phase 6 verification required",
            "backend_add_bos": self.backend_add_bos,
        }

    def _request(self, path, payload=None, deadline=None):
        content = None if payload is None else json.dumps(payload, allow_nan=False).encode()
        deadline = deadline or perf_counter() + self.settings.timeout_seconds
        remaining = deadline - perf_counter()
        if remaining <= 0:
            raise TimeoutError("generation HTTP deadline exceeded")
        parsed = urlparse(self.settings.base_url)
        connection = HTTPConnection(parsed.hostname, parsed.port, timeout=remaining)
        try:
            connection.request("GET" if payload is None else "POST", path, body=content,
                               headers={"Content-Type": "application/json"})
            transport = connection.sock
            remaining = deadline - perf_counter()
            if remaining <= 0:
                raise TimeoutError("generation HTTP deadline exceeded")
            transport.settimeout(remaining)
            response = connection.getresponse()
            if response.status != 200:
                response.close()
                raise HTTPError(self.settings.base_url + path, response.status,
                                response.reason, response.headers, None)
            return _TimedResponse(connection, response, transport, deadline)
        except BaseException:
            connection.close()
            raise

    def _json(self, path, payload=None, deadline=None):
        with self._request(path, payload, deadline=deadline) as response:
            content = response.read(2 * 1024 * 1024 + 1)
        if len(content) > 2 * 1024 * 1024:
            raise DataError("generator metadata response exceeds limit")
        value = json.loads(content, parse_constant=_invalid_number)
        if not isinstance(value, dict) or "error" in value:
            raise DataError("invalid generator metadata response")
        return value

    def generate(self, question: str, context: str) -> dict:
        started = perf_counter()
        deadline = started + self.settings.timeout_seconds
        record = {"schema_version": 1, "purpose": "development generation diagnostic",
                  "status": "failed", "generator": self.identity, "question": question,
                  "context": context, "context_sha256": digest(context), "partial_answer": ""}
        try:
            prompt, count = render_prompt(self.tokenizer, question, context,
                                          self.settings.template_date, self.backend_add_bos)
            record.update(prompt=prompt, prompt_sha256=digest(prompt), native_prompt_tokens=count)
            record["backend_added_bos_tokens"] = int(self.backend_add_bos)
            if count + self.settings.maximum_output_tokens > self.settings.context_window:
                raise DataError("full prompt plus output allowance exceeds context window")
            # Model tags are mutable: check the resolved digest again for each request.
            tags = self._json("/api/tags", deadline=deadline)["models"]
            if not any(row["name"] == self.settings.model
                       and row["digest"] == self.settings.model_digest for row in tags):
                raise DataError("generator model tag changed before request")
            payload = {"model": self.settings.model, "prompt": prompt, "raw": True,
                       "stream": True, "keep_alive": "10m",
                       "options": {"temperature": 0, "seed": self.settings.seed,
                                   "num_predict": self.settings.maximum_output_tokens,
                                   "num_thread": self.settings.threads,
                                   "num_ctx": self.settings.context_window}}
            final, first_output = None, None
            with self._request("/api/generate", payload, deadline=deadline) as response:
                while True:
                    line = response.readline(1024 * 1024 + 1)
                    if not line:
                        break
                    if len(line) > 1024 * 1024:
                        raise DataError("generator response line exceeds limit")
                    chunk = json.loads(line, parse_constant=_invalid_number)
                    if not isinstance(chunk, dict):
                        raise DataError("generator stream returned a non-object record")
                    if "error" in chunk:
                        raise DataError(str(chunk["error"]))
                    text = chunk.get("response", "")
                    if not isinstance(text, str):
                        raise DataError("generator returned non-text output")
                    if text and first_output is None:
                        first_output = perf_counter() - started
                    record["partial_answer"] += text
                    if len(record["partial_answer"]) > 1024 * 1024:
                        raise DataError("generator output exceeds recording limit")
                    if chunk.get("done") is True:
                        final = chunk
                        break
            record["generation_seconds"] = perf_counter() - started
            record["client_first_visible_output_seconds"] = first_output
            if final is None:
                raise DataError("generator stream ended before a completion record")
            record["backend_final"] = final
            if final.get("model") != self.settings.model:
                raise DataError("generation response model mismatch")
            # A mismatch may mean silent overflow or a different native tokenizer.
            if (type(final.get("prompt_eval_count")) is not int
                    or final["prompt_eval_count"] != count):
                raise DataError("backend prompt count differs from untruncated native count")
            output = final.get("eval_count")
            if (type(output) is not int or not 0 <= output <= self.settings.maximum_output_tokens
                    or final.get("done_reason") not in {"stop", "length"}):
                raise DataError("invalid output token count or completion reason")
            cached = final.get("prompt_eval_cached_count")
            if cached is not None and (type(cached) is not int or not 0 <= cached <= count):
                raise DataError("invalid cached prompt token count")
            record.update(status="success", answer=record.pop("partial_answer"),
                          native_output_tokens=output, cached_prompt_tokens=cached,
                          output_truncated=final["done_reason"] == "length",
                          abstained=False)
            record["abstained"] = record["answer"].strip() == ABSTENTION
            return record
        except (DataError, OSError, URLError, HTTPException,
                ValueError, KeyError, TypeError) as error:
            reason = getattr(error, "reason", error)
            record.update(error=str(error), error_type=type(error).__name__,
                          timed_out=isinstance(reason, (TimeoutError, socket.timeout)),
                          generation_seconds=perf_counter() - started)
            if isinstance(error, HTTPError):
                record["http_status"] = error.code
                error.close()
            raise GenerationError(record) from error
