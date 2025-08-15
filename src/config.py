# src/config.py
import os

# --- Environment Switch ---
# Detects if the app is running on Hugging Face Spaces or locally.
# We'll set the "APP_MODE" environment variable to "spaces" in the HF settings.
APP_MODE = os.getenv("APP_MODE", "local") 

# --- Path Configuration ---
DATA_PATH = "data/thirukkural_data.json"
FAISS_PATH = "faiss"
FAISS_INDEX_FILE = os.path.join(FAISS_PATH, "kural_index.faiss")
METADATA_FILE = os.path.join(FAISS_PATH, "kural_metadata.pkl")

# --- Model Configuration ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Configuration for the Qwen2 GGUF model for explanations
LLM_REPO_ID = "Qwen/Qwen2-1.5B-Instruct-GGUF"
LLM_FILENAME = "qwen2-1_5b-instruct-q4_k_m.gguf"

# --- UI Text Configuration ---
APP_TITLE = os.getenv("APP_TITLE", "There's a kural for that! - Thirukkural Semantic Search")
ABOUT_TEXT = os.getenv(
    "ABOUT_TEXT",
    "An intelligent, AI-powered app to explore the timeless wisdom of the Thirukkural.\n\n"
    "Find the most relevant Thirukkural verses for any theme or topic you provide. It performs semantic search and uses LLM to explain the relevance of each verse to your query.\n"
)
CONTACT_TEXT = os.getenv(
    "CONTACT_TEXT",
    "hal.vinoth@yahoo.com | [Github](https://github.com/vinovator/thirukkural_semantic_search_engine)"
)
