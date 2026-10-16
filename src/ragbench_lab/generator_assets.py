"""Export a native tokenizer from verified local model metadata and a pinned chat template."""

from __future__ import annotations

import json
import shutil
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


def configure_llama_bpe(backend) -> None:
    """Match Llama 3's pre-split and direct whole-vocabulary-token lookup."""
    from tokenizers import Regex, models, pre_tokenizers

    if not isinstance(backend.model, models.BPE) or not hasattr(backend.model, "ignore_merges"):
        raise DataError("Llama native tokenizer requires BPE with ignore_merges support")
    backend.model.ignore_merges = True
    backend.pre_tokenizer = pre_tokenizers.Sequence([
        pre_tokenizers.Split(Regex(LLAMA_PATTERN), behavior="isolated"),
        pre_tokenizers.ByteLevel(add_prefix_space=False, use_regex=False),
    ])


def correct_llama_export(source: Path, expected_files: dict[str, str], output: Path,
                         provenance: Path) -> dict[str, str]:
    """Create a separate export, changing only the verified BPE merge-policy bit."""
    if output.exists() or provenance.exists():
        raise DataError("corrected tokenizer requires fresh artifact paths")
    if ("tokenizer.json" not in expected_files
            or any(Path(name).name != name for name in expected_files)):
        raise DataError("pin tokenizer input filenames before correction")
    actual = {p.name for p in source.iterdir() if p.is_file()
              and p.suffix in {".json", ".txt", ".model", ".jinja"}}
    if actual != set(expected_files) or any(file_sha256(source / name) != sha
                                           for name, sha in expected_files.items()):
        raise DataError("source tokenizer differs from frozen input hashes")
    from tokenizers import Tokenizer

    original = json.loads((source / "tokenizer.json").read_text(encoding="utf-8"))
    backend = Tokenizer.from_str(json.dumps(original))
    if (original["model"]["type"] != "BPE"
            or original["model"].get("ignore_merges") is not False):
        raise DataError("correction requires the diagnosed original BPE merge policy")
    configure_llama_bpe(backend)
    if json.loads(backend.to_str())["pre_tokenizer"] != original["pre_tokenizer"]:
        raise DataError("source does not have the verified Llama split rule")
    corrected = json.loads(json.dumps(original))
    corrected["model"]["ignore_merges"] = True
    checked = Tokenizer.from_str(json.dumps(corrected))
    if checked.get_vocab() != backend.get_vocab():
        raise DataError("correction changed vocabulary IDs")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.mkdir()
    for name in expected_files:
        if name == "tokenizer.json":
            write_new_json(output / name, corrected)
        else:
            shutil.copyfile(source / name, output / name)
    files = {name: file_sha256(output / name) for name in expected_files}
    write_new_json(provenance, {
        "kind": "native_tokenizer_accounting_correction", "schema_version": 1,
        "original_files": expected_files, "files": files,
        "only_semantic_change": {"model.ignore_merges": {"before": False, "after": True}},
        "vocabulary_and_template_unchanged": True,
        "diagnosis": "artifacts/llama-count-diagnosis-v1/summary.json",
        "use_policy": "new manifest and separate run; never replace frozen assets",
    })
    return files


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
    from transformers import PreTrainedTokenizerFast
    from transformers.integrations.ggml import GGUF_TOKENIZER_MAPPING, convert_gguf_tokenizer

    metadata = {target: info[f"tokenizer.{source}"] for source, target in
                GGUF_TOKENIZER_MAPPING["tokenizer"].items()
                if info.get(f"tokenizer.{source}") is not None}
    backend, _ = convert_gguf_tokenizer(architecture, metadata)
    if architecture == "llama":
        configure_llama_bpe(backend)
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
        "conversion": "Transformers GGUF converter; Llama 3 split and ignore_merges rules",
        "llama_ignore_merges": architecture == "llama",
        "validation": "backend prompt count must match before any diagnostic is accepted",
        "llama_rule_source": "https://github.com/meta-llama/llama3/blob/main/llama/tokenizer.py",
    })
    return files
