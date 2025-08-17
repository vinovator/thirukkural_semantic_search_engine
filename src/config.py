# src/config.py
import os

# --- Environment Switch ---
# Detects if the app is running on Hugging Face Spaces or locally.
APP_MODE = os.getenv("APP_MODE", "local")
# APP_MODE = os.getenv("APP_MODE", "spaces") 

# --- Path Configuration ---
# Suggestion 2: Renamed from FAISS_PATH for clarity.
DATA_PATH = "data/thirukkural_data.json"
SEARCH_ARTIFACTS_PATH = "search_artifacts" 
METADATA_FILE = os.path.join(SEARCH_ARTIFACTS_PATH, "kural_metadata.pkl")
# Note: You will also need to update this path in embed_data.py and search_logic.py

# --- Model Configuration ---
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Suggestion 3: Removed old, commented-out GGUF model config.

# --- LLM Provider Switch ---
# Suggestion 1: Implemented the "smart default" logic.
LLM_PROVIDER_HUGGINGFACE = "huggingface"
LLM_PROVIDER_OLLAMA = "ollama"
LLM_PROVIDER_GEMINI = "gemini"

# Determine the default provider based on the environment
if APP_MODE == "spaces":
    default_provider = LLM_PROVIDER_HUGGINGFACE
else:  # 'local'
    default_provider = LLM_PROVIDER_OLLAMA

# Set the provider. The default is now environment-aware.
# For local use, you can change this line directly.
# For Streamlit Cloud, you will set this as a Secret.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", default_provider)

# Configuration for Hugging Face model
HF_MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Configuration for Ollama model
#OLLAMA_MODEL_ID = "phi3" # was "llama3"
OLLAMA_MODEL_ID = "llama3" # was "phi3"

# Google Gemini (for Streamlit Cloud)
GEMINI_MODEL_ID = "gemini-1.5-flash-latest"
# This will read the API key from Streamlit's Secrets manager
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- UI Text Configuration ---
APP_TITLE = os.getenv("APP_TITLE", "There's a kural for that! - Thirukkural Semantic Search")

# Suggestion 4: Polished the UI text.
ABOUT_TEXT = os.getenv(
    "ABOUT_TEXT",
    "An intelligent, AI-powered app to explore the timeless wisdom of the Thirukkural.\n\n"
    "Enter any topic or query in English, and the app will surface the most semantically relevant verses, complete with an AI-generated explanation of why each one fits."
)
CONTACT_TEXT = os.getenv(
    "CONTACT_TEXT",
    "Mail: <a href='mailto:hal.vinoth@yahoo.com'>hal.vinoth@yahoo.com</a> | [Github](https://github.com/vinovator/thirukkural_semantic_search_engine)"
)