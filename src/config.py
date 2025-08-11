# src/config.oy

# This file acts the control panel. It defines our application's settings and securely loads the API key from the .env file

import os
from dotenv import load_dotenv

# Load environment variables from .env file into the environment
load_dotenv()

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
DATA_PATH = "data/thirukkural_data.json"
CHROMA_PATH = "chromadb"

# Database
COLLECTION_NAME = "thirukkural_collection"

# Models
EMBEDDING_MODEL = "all-MiniLM-L6-v2"