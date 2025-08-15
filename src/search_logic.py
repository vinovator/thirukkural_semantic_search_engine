# src/search_logic.py
import faiss
import pickle
import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
from src.config import EMBEDDING_MODEL, FAISS_INDEX_FILE, METADATA_FILE

@st.cache_resource
def load_search_artifacts():
    """
    Loads the sentence transformer model, FAISS index, and metadata.
    This is cached to avoid reloading on every interaction.
    """
    print("Loading search artifacts...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    index = faiss.read_index(FAISS_INDEX_FILE)
    with open(METADATA_FILE, 'rb') as f:
        metadata = pickle.load(f)
    print("Search artifacts loaded successfully.")
    return model, index, metadata

def semantic_search(query: str, model: SentenceTransformer, index: faiss.Index, metadata: list, top_k: int = 3):
    """
    Performs semantic search using the loaded FAISS index.
    """
    query_embedding = model.encode([query]).astype('float32')
    distances, indices = index.search(query_embedding, top_k)
    results = [metadata[i] for i in indices[0]]
    return results