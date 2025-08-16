# embed_data.py
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import numpy as np
import os
import pickle
from src.config import DATA_PATH, EMBEDDING_MODEL, SEARCH_ARTIFACTS_PATH, METADATA_FILE

# Define a new path for the embeddings file in your config or here
EMBEDDINGS_FILE = os.path.join(SEARCH_ARTIFACTS_PATH, "kural_embeddings.npy")

def main():
    # --- 1. Load and Prepare Data ---
    with open(DATA_PATH, 'r', encoding='utf-8') as file:
        thirukkural_data = json.load(file)

    df = pd.DataFrame(thirukkural_data['kural'])
    df.rename(columns={'Number': 'kural_no',
                       'explanation': 'kural_english_explanation',
                       'mv': 'kural_tamil_explanation'}, inplace=True)
    metadata = df.to_dict(orient='records')
    documents_to_embed = df["kural_english_explanation"].tolist()

    # --- 2. Generate and Save Embeddings ---
    print(f"Initializing embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("Generating embeddings... This may take a while.")
    embeddings = model.encode(documents_to_embed, show_progress_bar=True)
    
    # Create the directory if it doesn't exist
    if not os.path.exists(SEARCH_ARTIFACTS_PATH):
        os.makedirs(SEARCH_ARTIFACTS_PATH)
    
    # Save the embeddings array and the metadata list
    np.save(EMBEDDINGS_FILE, embeddings)
    with open(METADATA_FILE, 'wb') as f:
        pickle.dump(metadata, f)
        
    print(f"Embeddings saved to: {EMBEDDINGS_FILE}")
    print(f"Metadata saved to: {METADATA_FILE}")
    print("\nProcess completed successfully!")

if __name__ == "__main__":
    main()