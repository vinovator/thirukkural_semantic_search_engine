# embed_data.py
# Build read-only FAISS artifacts (Spaces + local fallback).

import json
from pathlib import Path
from typing import Dict, Any, List

from sentence_transformers import SentenceTransformer
import faiss

from src.config import (
    DATA_FILE,
    FAISS_DIR, FAISS_INDEX_PATH, FAISS_META_PATH,
    EMBEDDING_MODEL, EMBEDDING_DIM,
)

def _join_tamil(line1: str, line2: str) -> str:
    return f"{line1.strip()}\n{line2.strip()}"

def build_faiss() -> None:
    # Ensure output dir exists
    FAISS_DIR.mkdir(parents=True, exist_ok=True)

    # Load dataset
    data = json.loads(Path(DATA_FILE).read_text(encoding="utf-8"))
    items: List[Dict[str, Any]] = data["kural"]  

    # --- Embeddings: English-only from 'explanation' ---
    texts = [it["explanation"] for it in items]

    model = SentenceTransformer(EMBEDDING_MODEL)
    embs = model.encode(
        texts,
        batch_size=64,
        show_progress_bar=True,
        convert_to_numpy=True
    ).astype("float32")

    # Cosine similarity via inner product
    faiss.normalize_L2(embs)
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(embs)
    faiss.write_index(index, str(FAISS_INDEX_PATH))

    # --- Meta: standardized keys for the app/renderer ---
    meta = []
    for it in items:
        meta.append({
            # Renames you asked for:
            "kural_no": it["Number"],                                 # Number -> kural_no
            "kural_english_explanation": it["explanation"],           # explanation -> kural_english_explanation
            "kural_tamil_explanation": it["mv"],                      # mv -> kural_tamil_explanation

            # Extra fields your UI shows:
            "kural_tamil": _join_tamil(it["Line1"], it["Line2"]),
            "paal_name_tamil": it["paal_name_tamil"],
            "paal_translation_english": it["paal_translation_english"],
            "adhikaram_name_tamil": it["adhikaram_name_tamil"],
            "adhikaram_translation_english": it["adhikaram_translation_english"],
        })

    Path(FAISS_META_PATH).write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    print(f"FAISS index: {FAISS_INDEX_PATH}")
    print(f"FAISS meta : {FAISS_META_PATH}")
    print(f"Records    : {len(items)}")

if __name__ == "__main__":
    build_faiss()
