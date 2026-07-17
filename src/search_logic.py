# src/search_logic.py
import pickle
import streamlit as st
from sentence_transformers import SentenceTransformer, CrossEncoder
import numpy as np
from src.config import (
    EMBEDDING_MODEL,
    METADATA_FILE,
    SEARCH_ARTIFACTS_PATH,
    QUERY_PREFIX,
    RERANK_MODEL,
    RETRIEVE_K,
    RERANK_TOP_K,
    RELEVANCE_THRESHOLD,
)
import os
from sklearn.metrics.pairwise import cosine_similarity

# Path to the new embeddings file
EMBEDDINGS_FILE = os.path.join(SEARCH_ARTIFACTS_PATH, "kural_embeddings.npy")

@st.cache_resource
def load_search_artifacts():
    """
    Loads the sentence transformer model, embeddings, and metadata.
    """
    print("Loading search artifacts...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    embeddings = np.load(EMBEDDINGS_FILE)
    with open(METADATA_FILE, 'rb') as f:
        metadata = pickle.load(f)
    print("Search artifacts loaded successfully.")
    return model, embeddings, metadata

@st.cache_resource
def load_reranker():
    """
    Loads the cross-encoder used to re-rank retrieval candidates.
    """
    print("Loading re-ranker model...")
    reranker = CrossEncoder(RERANK_MODEL)
    print("Re-ranker loaded successfully.")
    return reranker

def semantic_search(query: str, model: SentenceTransformer, embeddings: np.ndarray, metadata: list, top_k: int = RERANK_TOP_K):
    """
    Two-stage retrieval:
      1. Bi-encoder + cosine similarity retrieves the top RETRIEVE_K candidates.
      2. A cross-encoder re-scores (query, candidate) pairs and keeps the best
         top_k above RELEVANCE_THRESHOLD.
    Returns a list of metadata dicts (possibly empty if nothing is relevant).
    """
    # --- Stage 1: bi-encoder candidate retrieval ---
    # bge/e5-family models expect the instruction prefix on the query only.
    query_embedding = model.encode([QUERY_PREFIX + query])
    similarities = cosine_similarity(query_embedding, embeddings)[0]

    # Take the top RETRIEVE_K candidate indices, highest similarity first.
    candidate_indices = np.argsort(similarities)[-RETRIEVE_K:][::-1]

    # --- Stage 2: cross-encoder re-ranking ---
    reranker = load_reranker()
    pairs = [
        (query, metadata[i].get("kural_english_explanation", ""))
        for i in candidate_indices
    ]
    rerank_scores = reranker.predict(pairs)

    # Sort candidates by cross-encoder score (descending) and keep those that
    # clear the relevance threshold, up to top_k.
    ranked = sorted(zip(candidate_indices, rerank_scores), key=lambda x: x[1], reverse=True)
    results = [metadata[i] for i, score in ranked if score >= RELEVANCE_THRESHOLD][:top_k]

    return results