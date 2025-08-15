# src/config.oy

# This file acts the control panel. It defines our application's settings and securely loads the API key from the .env file
# Control panel for app settings. Backward-compatible with your existing names.

import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file into the environment
load_dotenv()

# ---------- Runtime mode ----------
# Set RUN_ENV=spaces in Hugging Face Spaces (Settings → Variables & secrets)
RUN_ENV: str = os.getenv("RUN_ENV", "local").strip().lower()
IS_SPACES: bool = RUN_ENV == "spaces"

# Project root
ROOT_DIR = Path(__file__).resolve().parents[1]

# --- LLM Services Configuration ---
# Define the available LLM services
LLM_GEMINI = "Google Gemini"
LLM_LOCAL_LLAMA3 = "Local Llama3 (via Ollama)"

# Define the Model IDs for the LLM services
GEMINI_MODEL_ID = "gemini-1.5-flash-latest"
LLAMA3_MODEL_ID = "llama3"

# --- The Master Switch ---
# To toggle between services, change the value of this variable.
SELECTED_LLM = LLM_LOCAL_LLAMA3
# SELECTED_LLM = LLM_GEMINI  # Uncomment this line to switch to Google Gemini

# APIS Keys (Loaded securelty from .env file)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Paths
DATA_PATH = os.getenv("DATA_PATH", "data/thirukkural_data.json")  # legacy string
CHROMA_PATH = os.getenv("CHROMA_PATH", "chromadb")
COLLECTION_NAME = os.getenv("COLLECTION_NAME", "thirukkural_collection")

# Pathlib versions for new code
DATA_FILE = ROOT_DIR / DATA_PATH
CHROMA_DIR = ROOT_DIR / CHROMA_PATH

# FAISS read-only artifacts (committed)
FAISS_DIR = ROOT_DIR / "faiss"
FAISS_INDEX_PATH = FAISS_DIR / "index.faiss"
FAISS_META_PATH = FAISS_DIR / "meta.json"

# ---------- Embeddings ----------
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIM", "384"))

# ---------- Spaces explainer (llama-cpp / Qwen) ----------
ENABLE_EXPLAINER = True  # harmless if it can't load; code skips

QWEN_GGUF_REPO = os.getenv("QWEN_GGUF_REPO", "Qwen/Qwen2.5-1.5B-Instruct-GGUF")
QWEN_GGUF_FILE = os.getenv("QWEN_GGUF_FILE", "qwen2.5-1.5b-instruct-q4_k_m.gguf")

LLM_N_CTX = int(os.getenv("LLM_N_CTX", "2048"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "128"))
LLAMA_CPP_N_THREADS = int(os.getenv("LLAMA_CPP_N_THREADS", "4"))
LLM_LOAD_TIMEOUT_S = int(os.getenv("LLM_LOAD_TIMEOUT_S", "30"))

# ---------- UI (optional centralization) ----------
APP_TITLE = os.getenv("APP_TITLE", "There's a kural for that! - Thirukkural Semantic Search")
ABOUT_TEXT = os.getenv(
    "ABOUT_TEXT",
    "An intelligent, AI-powered Streamlit app to explore the timeless wisdom of the Thirukkural.\n\n"
    "Enter any topic or natural‑language query in English and the app surfaces the most semantically relevant Kurals — with the original Tamil, translations, and an AI explanation of why each verse matches your query."
)
CONTACT_TEXT = os.getenv(
    "CONTACT_TEXT",
    "Contact: hal.vinoth@yahoo.com • LinkedIn: https://www.linkedin.com/in/vinothhaldorai/"
)