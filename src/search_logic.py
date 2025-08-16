# src/search_logic.py
import pickle
import streamlit as st
from sentence_transformers import SentenceTransformer
import numpy as np
from src.config import EMBEDDING_MODEL, METADATA_FILE, SEARCH_ARTIFACTS_PATH
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

def semantic_search(query: str, model: SentenceTransformer, embeddings: np.ndarray, metadata: list, top_k: int = 3):
    """
    Performs semantic search using scikit-learn's cosine similarity.
    """
    # 1. Generate the embedding for the user's query
    query_embedding = model.encode([query])
    
    # 2. Calculate cosine similarity between the query and all Kurals
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    
    # 3. Get the indices of the top_k most similar Kurals
    # We use argsort to sort the indices by similarity, then take the top_k from the end
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]
    
    # 4. Retrieve the original data using the indices
    results = [metadata[i] for i in top_k_indices]
    
    return results