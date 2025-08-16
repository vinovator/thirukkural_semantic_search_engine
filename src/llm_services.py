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
    # --- PROMPT REFINEMENT ---
    system_prompt = """You are an insightful analyst of philosophy and literature. Your task is to explain the connection between a user's query and a verse from the ancient Tamil text, the Thirukkural."""
    
    user_prompt = f"""
    Analyze the following.
    
    **Query:** "{query}"
    **Thirukkural Verse Explanation:** "{kural_explanation}"

    Now, in 2-3 concise and natural sentences, provide your analysis of the semantic connection:
    """
    
    # --- OLLAMA LOGIC ---
    if LLM_PROVIDER == LLM_PROVIDER_OLLAMA:
        try:
            logging.info(f"Getting explanation from Ollama model: {OLLAMA_MODEL_ID}")
            response = ollama.chat(
                model=OLLAMA_MODEL_ID,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            # --- Clean-up Step ---
            # Ensures we only return the generated text
            clean_response = response['message']['content'].split("semantic connection:")[-1].strip()
            return clean_response

        except Exception as e:
            logging.error(f"Error with Ollama: {e}")
            return "Explanation not available: Could not connect to Ollama."

    # --- HUGGING FACE TRANSFORMERS LOGIC ---
    elif LLM_PROVIDER == LLM_PROVIDER_HUGGINGFACE:
        if not model or not tokenizer:
            return "Explanation not available: Hugging Face LLM failed to load."

        chat_prompt = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        input_ids = tokenizer.apply_chat_template(chat_prompt, add_generation_prompt=True, return_tensors="pt")

        try:
            logging.info(f"Getting explanation from Hugging Face model: {HF_MODEL_ID}")
            outputs = model.generate(input_ids, max_new_tokens=150, temperature=0.3, do_sample=True)
            response_text = tokenizer.decode(outputs[0][input_ids.shape[-1]:], skip_special_tokens=True)
            
            # --- Clean-up Step ---
            # Ensures we only return the generated text
            clean_response = response_text.split("semantic connection:")[-1].strip()
            return clean_response
            
        except Exception as e:
            logging.error(f"Error during LLM inference: {e}")
            return "Explanation not available due to a technical issue."

    else:
        return f"Error: Unknown LLM_PROVIDER '{LLM_PROVIDER}' configured."