"""Export a native tokenizer from verified local model metadata and a pinned chat template."""

from __future__ import annotations

from pathlib import Path

from ragbench_lab.data.preparation import digest
from ragbench_lab.data.records import DataError
from ragbench_lab.embeddings import file_sha256
from ragbench_lab.pipeline import write_new_json

# Published Llama 3 pre-tokenization rule. Persist this in the exported tokenizer.
LLAMA_PATTERN = (
    r"(?i:'s|'t|'re|'ve|'m|'ll|'d)|[^\r\n\p{L}\p{N}]?\p{L}+|\p{N}{1,3}|"
    r" ?[^\s\p{L}\p{N}]+[\r\n]*|\s*[\r\n]+|\s+(?!\S)|\s+"
)


def export_native_tokenizer(show: dict, hf_metadata: dict, revision: str,
                            model_digest: str, output: Path, provenance: Path) -> dict:
    if output.exists() or provenance.exists():
        raise DataError("native tokenizer export requires fresh artifact paths")
    if hf_metadata["sha"] != revision:
        raise DataError("native chat-template source revision mismatch")
    info = show["model_info"]
    architecture = info["general.architecture"]
    if architecture not in {"qwen2", "llama"}:
        raise DataError("unsupported generator architecture")
    if hf_metadata["config"]["model_type"] != architecture:
        raise DataError("native template family differs from the local model")
    tokens = info.get("tokenizer.ggml.tokens")
    merges = info.get("tokenizer.ggml.merges")
    if not isinstance(tokens, list) or not tokens or not isinstance(merges, list) or not merges:
        raise DataError("model metadata lacks full native vocabulary/merges; use verbose show")
    if architecture == "llama" and info.get("tokenizer.ggml.pre") not in {"llama-bpe", "llama3"}:
        raise DataError("unsupported Llama pre-tokenization rule")
    template = hf_metadata["config"]["tokenizer_config"]["chat_template"]
    if not isinstance(template, str) or not template:
        raise DataError("native source lacks one pinned chat template")
    from tokenizers import Regex, pre_tokenizers
    from transformers import PreTrainedTokenizerFast
    from transformers.integrations.ggml import GGUF_TOKENIZER_MAPPING, convert_gguf_tokenizer

    metadata = {target: info[f"tokenizer.{source}"] for source, target in
                GGUF_TOKENIZER_MAPPING["tokenizer"].items()
                if info.get(f"tokenizer.{source}") is not None}
    backend, _ = convert_gguf_tokenizer(architecture, metadata)
    if architecture == "llama":
        backend.pre_tokenizer = pre_tokenizers.Sequence([
            pre_tokenizers.Split(Regex(LLAMA_PATTERN), behavior="isolated"),
            pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=False),
        ])
    special = {}
    for key, identifier in (("bos_token", "bos_token_id"), ("eos_token", "eos_token_id"),
                            ("unk_token", "unk_token_id"), ("pad_token", "pad_token_id")):
        if identifier in metadata:
            special[key] = tokens[metadata[identifier]]
    tokenizer = PreTrainedTokenizerFast(tokenizer_object=backend, chat_template=template,
                                       model_max_length=4096, **special)
    vocabulary = tokenizer.get_vocab()
    if any(vocabulary.get(token) != index for index, token in enumerate(tokens)):
        raise DataError("exported native vocabulary IDs differ from the local model")
    tokenizer.backend_tokenizer.no_truncation()
    tokenizer.backend_tokenizer.no_padding()
    output.mkdir(parents=True)
    tokenizer.save_pretrained(output)
    files = {path.name: file_sha256(path) for path in output.iterdir() if path.is_file()}
    write_new_json(provenance, {
        "model_digest": model_digest, "native_vocabulary_source": "local Ollama model metadata",
        "model_info_sha256": digest(info), "chat_template_revision": revision,
        "chat_template_sha256": digest(template), "architecture": architecture, "files": files,
        "conversion": "Transformers GGUF converter; explicit published Llama 3 split rule",
        "validation": "backend prompt count must match before any diagnostic is accepted",
        "llama_rule_source": "https://github.com/meta-llama/llama3/blob/main/llama/tokenizer.py",
    })
    return files
