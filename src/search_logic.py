import chromadb
from sentence_transformers import SentenceTransformer
from src.config import CHROMA_PATH, COLLECTION_NAME


def get_db_collection():
    """
    Initializes a persistent ChromaDB client and returns the collection.
    """
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection(name=COLLECTION_NAME)
    return collection

def semantic_search(query: str, collection: chromadb.Collection, model: SentenceTransformer):
    """
    Performs a semantic search on the given collection using the provided query.
    """
    
    # Generate embeddings for the query
    query_embedding = model.encode(query).tolist()
    
    # Perform the search
    results = collection.query(
        query_embeddings=[query_embedding], 
        n_results=3,
        include=["metadatas", "documents"]
    )
    
    return results