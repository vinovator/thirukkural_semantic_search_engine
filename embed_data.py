#embed_data.py
#This is where we adapt to the JSON format. The script opens the JSON, extracts the kural list and creates a clean DataFrame.
#We will combine Line1 and Line2 and rename columns like Number and explanation to a standard format that rest of our app can use.

import json
import pandas as pd
from sentence_transformers import SentenceTransformer
from src.search_logic import get_db_collection
from src.config import DATA_PATH, EMBEDDING_MODEL

def main():
    # Load the Thirukkural data from the JSON file
    with open(DATA_PATH, 'r', encoding='utf-8') as file:
        thirukkural_data = json.load(file)

    # Extract the kural list and create a DataFrame
    kural_list = thirukkural_data['kural']
    df = pd.DataFrame(kural_list)

    # --- Data Transformation ---
    # Combine Line1 and Line2 into a single column named 'verse'
    df['kural_tamil'] = df['Line1'] + " " + df['Line2']

    # Rename columns to standard format
    df.rename(columns={'Number': 'kural_no', 
                       'explanation': 'kural_english_explanation',
                       'mv': 'kural_tamil_explanation'}, inplace=True)

    # Select the document we want to embed for semantic search. The "explanation" column is best fit.
    documents_to_embed = df["kural_english_explanation"].tolist()

    # Get the database collection
    collection = get_db_collection()

    if collection.count() > 0:
        print("Collection already exists. Skipping embedding process.")
        return
    
    # Initialize the embedding model
    print(f"Initializing the embedding model: {EMBEDDING_MODEL}")
    model = SentenceTransformer(EMBEDDING_MODEL)

    # Generate embeddings for the documents
    print("Generating embeddings for the documents... This may take a while.")
    embeddings = model.encode(documents_to_embed, show_progress_bar=True)

    # We will store the entire record of each kural as metadata in the collection
    metadatas = df.to_dict(orient='records')
    ids = [str(i) for i in df.index]

    print("Adding data to the vector database... ")
    collection.add(
        embeddings=embeddings.tolist(),
        documents=documents_to_embed,
        metadatas=metadatas,
        ids=ids
    )

    print(f"\n Process completed successfully! {collection.count()} records embedded and added to the collection.")

if __name__ == "__main__":
    main()
