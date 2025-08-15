# src/llm_services.py
import streamlit as st
from llama_cpp import Llama
from huggingface_hub import hf_hub_download
import logging
from src.config import LLM_REPO_ID, LLM_FILENAME

logging.basicConfig(level=logging.INFO)

@st.cache_resource
def load_llm_model():
    """
    Downloads the GGUF model and initializes the Llama model.
    Cached to load the model only once.
    """
    try:
        logging.info("Downloading and loading LLM model...")
        model_path = hf_hub_download(repo_id=LLM_REPO_ID, filename=LLM_FILENAME)
        llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_gpu_layers=-1, # Offload all layers to GPU if available
            verbose=False
        )
        logging.info("LLM model loaded successfully.")
        return llm
    except Exception as e:
        logging.error(f"Error loading LLM model: {e}")
        return None

def get_relevance_explanation(query: str, kural_explanation: str, llm: Llama) -> str:
    """
    Generates an explanation for relevance using the loaded Llama model.
    """
    if not llm:
        return "Explanation not available: LLM failed to load."

    prompt = f"""
    Analyze the connection between the user's query and the provided Thirukkural explanation.
    **User's Query:** {query}
    **Thirukkural Explanation:** {kural_explanation}
    **Your Task:** In 2-3 concise sentences, explain how the Thirukkural verse is semantically relevant to the user's query.
    """
    system_prompt = "You are a helpful assistant who analyzes ancient texts."
    
    try:
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150, temperature=0.3
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        logging.error(f"Error during LLM inference: {e}")
        return "Explanation not available due to a technical issue."