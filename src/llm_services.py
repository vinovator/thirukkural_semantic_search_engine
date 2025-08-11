import google.generativeai as genai
import ollama
from src.config import GEMINI_API_KEY, SELECTED_LLM, LLM_GEMINI, LLM_LOCAL_LLAMA3, GEMINI_MODEL_ID, LLAMA3_MODEL_ID

def get_relevance_explanation(query:str, kural_explanation: str) -> str:
    """
    Generates an explanation for relevance from Google Gemini API.
    """

    # Create a prompt for the Gemini model
    prompt = f"""
    Analyze the connection between the user's query and the provided Thirukkural explanation.
    **User's Query:** {query}
    **Thirukkural Explanation:** {kural_explanation}
    **Your Task:** In 2-3 concise sentences, explain how the Thirukkural verse is semantically relevant to the user's query.
    """

    # --- Dispatch to the selected LLM service ---
    if SELECTED_LLM == LLM_GEMINI:
        try:
            if not GEMINI_API_KEY:
                return "Error: GEMINI_API_KEY is not set. Please check your .env file."
            
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel(GEMINI_MODEL_ID)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error with Gemini API: {str(e)}"
        

    elif SELECTED_LLM == LLM_LOCAL_LLAMA3:
        try: 
            response = ollama.chat(
                model=LLAMA3_MODEL_ID,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response['message']['content']
        except Exception as e:
            return f"Error with Local Llama3: {str(e)}"
        
    else:
        return f"Error: Unsupported LLM service selected: {SELECTED_LLM}. Please check your configuration."