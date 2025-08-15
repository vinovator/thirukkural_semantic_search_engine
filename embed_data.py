# embed_data.py
import json
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle
from src.config import DATA_PATH, EMBEDDING_MODEL, FAISS_PATH, FAISS_INDEX_FILE, METADATA_FILE

def main():
    # --- 1. Load and Prepare Data ---
    with open(DATA_PATH, 'r', encoding='utf-8') as file:
        thirukkural_data = json.load(file)

    df = pd.DataFrame(thirukkural_data['kural'])
    df['kural_tamil'] = df['Line1'] + " " + df['Line2']
    df.rename(columns={'Number': 'kural_no',
                       'explanation': 'kural_english_explanation',
                       'mv': 'kural_tamil_explanation'}, inplace=True)
    metadata = df.to_dict(orient='records')
    documents_to_embed = df["kural_english_explanation"].tolist()

    # --- 2. Generate Embeddings ---
    print(f"Initializing embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)
    print("Generating embeddings... This may take a while.")
    embeddings = model.encode(documents_to_embed, show_progress_bar=True)
    embeddings = np.array(embeddings).astype('float32')

    # --- 3. Build and Save FAISS Index ---
    embedding_dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dimension)
    index.add(embeddings)
    print(f"FAISS index built successfully with {index.ntotal} vectors.")

    if not os.path.exists(FAISS_PATH):
        os.makedirs(FAISS_PATH)
    
    faiss.write_index(index, FAISS_INDEX_FILE)
    with open(METADATA_FILE, 'wb') as f:
        pickle.dump(metadata, f)
        
    print(f"FAISS index saved to: {FAISS_INDEX_FILE}")
    print(f"Metadata saved to: {METADATA_FILE}")
    print("\nProcess completed successfully!")

if __name__ == "__main__":
    main()