# src/llm_services.py
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import logging
import ollama
from src.config import LLM_PROVIDER, HF_MODEL_ID, OLLAMA_MODEL_ID, LLM_PROVIDER_HUGGINGFACE, LLM_PROVIDER_OLLAMA

logging.basicConfig(level=logging.INFO)

@st.cache_resource
def load_hf_model():
    """
    Loads the Hugging Face model and tokenizer.
    """
    try:
        logging.info(f"Loading Hugging Face model: {HF_MODEL_ID}")
        tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_ID)
        model = AutoModelForCausalLM.from_pretrained(HF_MODEL_ID, torch_dtype=torch.float32)
        logging.info("Hugging Face model loaded successfully.")
        return model, tokenizer
    except Exception as e:
        logging.error(f"Error loading Hugging Face model: {e}")
        return None, None

def get_relevance_explanation(query: str, kural_explanation: str, model=None, tokenizer=None) -> str:
    """
    Generates an explanation by dispatching to the configured LLM provider.
    """
    prompt = f"""
    Analyze the connection between the user's query and the provided Thirukkural explanation.
    **User's Query:** {query}
    **Thirukkural Explanation:** {kural_explanation}
    **Your Task:** In 2-3 concise sentences, explain how the Thirukkural verse is semantically relevant to the user's query.
    """

    # --- OLLAMA LOGIC ---
    if LLM_PROVIDER == LLM_PROVIDER_OLLAMA:
        try:
            logging.info(f"Getting explanation from Ollama model: {OLLAMA_MODEL_ID}")
            response = ollama.chat(
                model=OLLAMA_MODEL_ID,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content'].strip()
        except Exception as e:
            logging.error(f"Error with Ollama: {e}")
            return "Explanation not available: Could not connect to Ollama."

    # --- HUGGING FACE TRANSFORMERS LOGIC ---
    elif LLM_PROVIDER == LLM_PROVIDER_HUGGINGFACE:
        if not model or not tokenizer:
            return "Explanation not available: Hugging Face LLM failed to load."

        system_prompt = "You are a helpful assistant who analyzes ancient texts."
        chat_prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze the connection between this query and this text.\n\n**User's Query:** {query}\n\n**Thirukkural Explanation:** {kural_explanation}"}
        ]
        input_ids = tokenizer.apply_chat_template(chat_prompt, add_generation_prompt=True, return_tensors="pt")

        try:
            logging.info(f"Getting explanation from Hugging Face model: {HF_MODEL_ID}")
            outputs = model.generate(input_ids, max_new_tokens=150, temperature=0.3, do_sample=True)
            response = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
            return response.strip()
        except Exception as e:
            logging.error(f"Error during LLM inference: {e}")
            return "Explanation not available due to a technical issue."

    else:
        return f"Error: Unknown LLM_PROVIDER '{LLM_PROVIDER}' configured."