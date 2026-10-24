from __future__ import annotations

import hashlib
import ssl
from dataclasses import asdict
from importlib.metadata import version
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen

from ragbench_lab.config import EmbeddingConfig
from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError
from ragbench_lab.native import require_native_environment, shared_openmp_directory

COMMON_FILES = {
    "special_tokens_map.json": "a8b3208c2884c4efb86e49300fdd3dc877220cdf",
    "tokenizer.json": "688882a79f44442ddc1f60d70334a7ff5df0fb47",
    "vocab.txt": "fb140275c155a9c7c5a3b3e0e77a9e839594a938",
}
MODELS = {
    "bge": {
        "name": "BAAI/bge-small-en-v1.5",
        "directory": "bge-small-en-v1.5",
        "revision": "5c38ec7c405ec4b44b94cc5a9bb96e735b38267a",
        "weight_sha256": "3c9f31665447c8911517620762200d2245a2518d6e7208acc78cd9db317e21ad",
        "files": {**COMMON_FILES, "config.json": "3992bf890728a92476c700e6e657fd696eb94160",
                  "tokenizer_config.json": "37fca74771bc76a8e01178ce3a6055a0995f8093"},
        "query_prefix": "Represent this sentence for searching relevant passages: ",
        "passage_prefix": "", "pooling": "cls",
    },
    "e5": {
        "name": "intfloat/e5-small-v2", "directory": "e5-small-v2",
        "revision": "ffb93f3bd4047442299a41ebb6fa998a38507c52",
        "weight_sha256": "45bfa60070649aae2244fbc9d508537779b93b6f353c17b0f95ceccb1c5116c1",
        "files": {**COMMON_FILES, "config.json": "c5aba64a4d8f4c631ef0beddc89704232d2e649d",
                  "tokenizer_config.json": "8046d4d4aff4529a10e0ad47043bdabd6304fb58"},
        "query_prefix": "query: ", "passage_prefix": "passage: ",
        "pooling": "attention_mask_mean",
    },
}


def file_sha256(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def verify_file(path: Path, spec: dict) -> str:
    if path.name == "model.safetensors":
        checksum = file_sha256(path)
        expected = spec["weight_sha256"]
    else:
        content = path.read_bytes()
        checksum = hashlib.sha1(b"blob " + str(len(content)).encode() + b"\0" + content).hexdigest()
        expected = spec["files"][path.name]
    if checksum != expected:
        raise DataError(f"model artifact identity mismatch: {path.name}")
    return checksum if path.name == "model.safetensors" else file_sha256(path)


def download_models(root: Path) -> dict:
    """Explicit acquisition only; reuse verified files, never replace an existing artifact."""
    import certifi

    result = {}
    for family, spec in MODELS.items():
        directory = root / spec["directory"]
        directory.mkdir(parents=True, exist_ok=True)
        files = {}
        for filename in [*spec["files"], "model.safetensors"]:
            path = directory / filename
            if not path.exists():
                partial = directory / (filename + ".part")
                if partial.exists():
                    raise DataError(f"unfinished model download exists: {partial}; "
                                    "preserve or move it")
                url = f"https://huggingface.co/{spec['name']}/resolve/{spec['revision']}/{filename}"
                try:
                    request = Request(url, headers={"User-Agent": "ragbench-lab/0.1"})
                    context = ssl.create_default_context(cafile=certifi.where())
                    with urlopen(request, timeout=60, context=context) as response:
                        with partial.open("xb") as stream:
                            while block := response.read(1024 * 1024):
                                stream.write(block)
                except (URLError, OSError) as error:
                    raise DataError(f"model download failed for {family}/{filename}: "
                                    f"{error}") from error
                # Verify with the intended filename before exposing the downloaded asset.
                if filename == "model.safetensors":
                    if file_sha256(partial) != spec["weight_sha256"]:
                        raise DataError("downloaded weights failed SHA-256 verification")
                else:
                    content = partial.read_bytes()
                    blob = hashlib.sha1(b"blob " + str(len(content)).encode()
                                        + b"\0" + content).hexdigest()
                    if blob != spec["files"][filename]:
                        raise DataError("downloaded model metadata failed Git blob verification")
                partial.rename(path)
            files[filename] = verify_file(path, spec)
        result[family] = {"name": spec["name"], "revision": spec["revision"], "files": files}
    return result


def prefixed_texts(family: str, texts: list[str], kind: str) -> list[str]:
    if family not in MODELS or kind not in {"query", "passage"}:
        raise DataError("unsupported encoder family or input kind")
    return [MODELS[family][kind + "_prefix"] + text for text in texts]


def validate_lengths(lengths: list[int], maximum: int, kind: str) -> None:
    for index, length in enumerate(lengths):
        if length > maximum:
            raise DataError(f"embedding {kind} input {index} has {length} tokens including "
                            f"prefix/special tokens; limit {maximum}; truncation forbidden")


def pool_hidden(hidden, mask, pooling: str):
    if pooling == "cls":
        return hidden[:, 0]
    if pooling == "attention_mask_mean":
        return hidden.masked_fill(~mask[..., None].bool(), 0.0).sum(1) / mask.sum(1)[..., None]
    raise DataError("unsupported embedding pooling")


class LocalEncoder:
    def __init__(self, family: str, root: Path, settings: EmbeddingConfig):
        require_native_environment()
        import torch
        from safetensors import safe_open
        from transformers import AutoModel, AutoTokenizer
        from transformers.utils import logging

        if family not in MODELS:
            raise DataError("unsupported encoder")
        self.family, self.settings = family, settings
        spec = MODELS[family]
        directory = root / spec["directory"]
        allowed = {*spec["files"], "model.safetensors"}
        unexpected = {p.name for p in directory.iterdir()
                      if p.is_file() and p.suffix in {".json", ".bin", ".safetensors", ".txt"}
                      and p.name not in allowed}
        if unexpected:
            raise DataError(f"unfingerprinted model inputs: {sorted(unexpected)}")
        files = {name: verify_file(directory / name, spec)
                 for name in [*spec["files"], "model.safetensors"]}
        torch.manual_seed(settings.seed)
        torch.set_num_threads(settings.threads)
        torch.use_deterministic_algorithms(True)
        self.tokenizer = AutoTokenizer.from_pretrained(directory, local_files_only=True,
                                                       trust_remote_code=False)
        self.tokenizer.backend_tokenizer.no_truncation()
        logging.disable_progress_bar()
        self.model, loading = AutoModel.from_pretrained(
            directory, local_files_only=True, trust_remote_code=False,
            use_safetensors=True, attn_implementation="eager", output_loading_info=True)
        if (loading["missing_keys"] or loading["mismatched_keys"] or loading["error_msgs"]
                or set(loading["unexpected_keys"]) - {"embeddings.position_ids"}):
            raise DataError(f"embedding weight loading mismatch: {loading}")
        if "embeddings.position_ids" in loading["unexpected_keys"]:
            # Transformers 5 rebuilds this non-trainable buffer; verify exact equivalence.
            weights_path = directory / "model.safetensors"
            with safe_open(weights_path, framework="pt", device="cpu") as weights:
                if not torch.equal(weights.get_tensor("embeddings.position_ids"),
                                   self.model.embeddings.position_ids):
                    raise DataError("reconstructed position buffer differs from pinned weights")
        self.model.to(device="cpu", dtype=torch.float32).eval()
        self.maximum = min(512, self.model.config.max_position_embeddings,
                           self.tokenizer.model_max_length)
        if self.maximum != 512 or self.model.config.hidden_size != 384:
            raise DataError("unsupported embedding model length or dimension")
        self.identity = {
            "name": spec["name"], "revision": spec["revision"], "files": files,
            "pooling": spec["pooling"], "query_prefix": spec["query_prefix"],
            "passage_prefix": spec["passage_prefix"], "maximum_tokens": self.maximum,
            "dimension": 384, "normalization": "l2", "dtype": "float32",
            "attention": "eager", "settings": asdict(settings),
            "loading_report": {key: sorted(value) for key, value in loading.items()},
            "torch_threads": torch.get_num_threads(),
            "torch_interop_threads": torch.get_num_interop_threads(),
            "shared_openmp_sha256": file_sha256(shared_openmp_directory() / "libomp.dylib")
            if shared_openmp_directory() is not None else None,
            "versions": {name: version(name) for name in
                         ("torch", "transformers", "tokenizers", "numpy", "safetensors")},
        }
        self.identity["sha256"] = digest(self.identity)
        self.last_lengths: list[int] = []

    def encode(self, texts: list[str], kind: str):
        import numpy as np
        import torch

        inputs = prefixed_texts(self.family, texts, kind)
        # Validate every untruncated input before any corpus forward pass.
        tokens = self.tokenizer(inputs, truncation=False, padding=False,
                                add_special_tokens=True)
        self.last_lengths = [len(row) for row in tokens["input_ids"]]
        validate_lengths(self.last_lengths, self.maximum, kind)
        vectors = []
        for start in range(0, len(inputs), self.settings.batch_size):
            batch = {key: values[start:start + self.settings.batch_size]
                     for key, values in tokens.items()}
            batch = self.tokenizer.pad(batch, padding=True, return_tensors="pt")
            with torch.inference_mode():
                hidden = self.model(**batch).last_hidden_state
                pooled = pool_hidden(hidden, batch["attention_mask"],
                                     MODELS[self.family]["pooling"])
                pooled = torch.nn.functional.normalize(pooled, p=2, dim=1)
            vectors.append(pooled.cpu().numpy().astype("float32"))
        return np.concatenate(vectors) if vectors else np.empty((0, 384), dtype="float32")
