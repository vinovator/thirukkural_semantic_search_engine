# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

A Streamlit app for semantic search over the Thirukkural (1,330 classical Tamil couplets). A user enters an English query; the app embeds it, ranks Kurals by cosine similarity, and uses an LLM to explain *why* each top result matches the query.

## Commands

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# One-time: build search artifacts (embeddings + metadata). Required before first run.
python embed_data.py

# Run the app
streamlit run app.py
```

There is no test suite, linter, or build step configured.

## Architecture

Deterministic retrieval narrows to the top 3 Kurals, then an **LLM explains relevance** for each. These are fully decoupled — the LLM never affects ranking. Retrieval itself is two-stage: a bi-encoder retrieves candidates, then a cross-encoder re-ranks them.

- `embed_data.py` — Offline, run once. Reads `data/thirukkural_data.json`, builds a **composite document** per Kural (English `explanation` + `couplet` + `adhikaram_translation_english`), embeds it with the bi-encoder in `config.EMBEDDING_MODEL` (`BAAI/bge-small-en-v1.5`), and writes `search_artifacts/kural_embeddings.npy` (the vectors) + `kural_metadata.pkl` (the full per-Kural records). Rerun this whenever the dataset, the composite-document construction, or the embedding model changes.
- `src/search_logic.py` — `load_search_artifacts()` and `load_reranker()` (both cached via `@st.cache_resource`) load the bi-encoder + `.npy` + `.pkl` and the cross-encoder. `semantic_search()` is two-stage: (1) embed the query (with `config.QUERY_PREFIX`, required by bge/e5 models) and take the top `RETRIEVE_K` by scikit-learn cosine similarity, then (2) re-score those candidates with the cross-encoder (`RERANK_MODEL`), drop anything below `RELEVANCE_THRESHOLD`, and return the top `RERANK_TOP_K`. Returns `[]` when nothing clears the threshold (off-topic queries). No vector DB.
- `src/llm_services.py` — `get_relevance_explanation()` dispatches to one of three LLM backends based on `LLM_PROVIDER`. This is the only file with LLM calls.
- `src/config.py` — Central config. All tunables (paths, model IDs, provider switch, UI text) live here and are overridable via env vars.
- `app.py` — Streamlit UI. Loads artifacts, renders results, then fills per-result placeholders with LLM explanations (Kurals appear immediately; explanations stream in after).
- `transform/merge_kural_data.py` — One-off dataset prep (not part of runtime). Flattened raw `json/thirukkural.json` + `json/detail.json` into the current `data/thirukkural_data.json`, adding `paal`/`adhikaram` metadata. Its inputs live under `transform/json/` (gitignored) and are not present.

## LLM provider switching

The "Relevance Explainer" runs on one of three backends, selected by `LLM_PROVIDER` in `src/config.py` (env-overridable):

- `ollama` — local Ollama service (default when `APP_MODE=local`); requires `ollama run llama3` running.
- `huggingface` — in-process `transformers` model (`TinyLlama-1.1B-Chat`); default when `APP_MODE=spaces`. First run downloads the model.
- `gemini` — Google Gemini API; requires `GEMINI_API_KEY` env var / Streamlit secret.

`APP_MODE` sets the default provider; `LLM_PROVIDER` overrides it. Only the HF backend loads a model into the app process (`load_hf_model()` in `app.py`, gated on the provider); Ollama and Gemini are external calls. When adding a provider, add a branch in `get_relevance_explanation()` and a constant + default in `config.py`.

## Data schema notes

Each record in `data/thirukkural_data.json` (`kural` list) carries: `Number`, `Line1`/`Line2` (Tamil couplet), `explanation` (English), `couplet` (English poetic rendering), `mv` (Tamil explanation), plus `paal_*`/`adhikaram_*` category metadata. `embed_data.py` renames `Number`→`kural_no`, `explanation`→`kural_english_explanation`, `mv`→`kural_tamil_explanation` into the metadata; the app reads these renamed keys. The embedded document is a composite of `kural_english_explanation` + `couplet` + `adhikaram_translation_english` (see `build_document` in `embed_data.py`), while the cross-encoder re-ranks against `kural_english_explanation` alone.

## Gotchas

- `numpy` must be `<2.0` — newer versions break the pickled artifacts (`numpy.core.multiarray failed to import`).
- Empty search results are expected for genuinely off-topic queries (nothing clears `RELEVANCE_THRESHOLD`). But if *every* query returns nothing, `python embed_data.py` was likely never run (missing `search_artifacts/`), or the threshold is set too high for the current cross-encoder.
- The `chromadb/` directory is a leftover from an earlier vector-DB approach and is gitignored/unused — search now uses NumPy + scikit-learn.
