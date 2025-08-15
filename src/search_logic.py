# src/search_logic.py
# FAISS-only semantic search for BOTH local and Hugging Face Spaces.
# Simple, minimal imports; loads index/model once per process.

import json
from pathlib import Path

from sentence_transformers import SentenceTransformer
import faiss

from src.config import EMBEDDING_MODEL, FAISS_INDEX_PATH, FAISS_META_PATH

# Module-level singletons (simple cache)
_FAISS_INDEX = None
_FAISS_META = None
_MODEL = None

def _ensure_loaded():
    """Load FAISS index, metadata, and encoder exactly once."""
    global _FAISS_INDEX, _FAISS_META, _MODEL

    if _FAISS_INDEX is None or _FAISS_META is None:
        index_path = Path(FAISS_INDEX_PATH)
        meta_path = Path(FAISS_META_PATH)
        if not index_path.exists() or not meta_path.exists():
            raise FileNotFoundError(
                "FAISS artifacts missing. Run `python embed_data.py` then commit "
                "faiss/index.faiss and faiss/meta.json."
            )
        _FAISS_INDEX = faiss.read_index(str(index_path))
        _FAISS_META = json.loads(meta_path.read_text(encoding="utf-8"))

    if _MODEL is None:
        _MODEL = SentenceTransformer(EMBEDDING_MODEL)

def semantic_search(query, top_k=3):
    """
    Return a list of dicts with keys:
      kural_no, kural_tamil, kural_tamil_explanation, kural_english_explanation,
      paal_name_tamil, paal_translation_english, adhikaram_name_tamil,
      adhikaram_translation_english, score
    """
    _ensure_loaded()

    # Encode query (float32) and normalize for cosine search (inner product)
    q = _MODEL.encode([query]).astype("float32")
    faiss.normalize_L2(q)

    scores, idxs = _FAISS_INDEX.search(q, top_k)

    results = []
    for rank, row in enumerate(idxs[0]):
        if row == -1:
            continue
        m = _FAISS_META[row]
        results.append({
            "score": float(scores[0][rank]),
            "kural_no": m["kural_no"],
            "kural_tamil": m["kural_tamil"],
            "kural_tamil_explanation": m.get("kural_tamil_explanation"),
            "kural_english_explanation": m["kural_english_explanation"],
            "paal_name_tamil": m.get("paal_name_tamil"),
            "paal_translation_english": m.get("paal_translation_english"),
            "adhikaram_name_tamil": m.get("adhikaram_name_tamil"),
            "adhikaram_translation_english": m.get("adhikaram_translation_english"),
        })
    return results
