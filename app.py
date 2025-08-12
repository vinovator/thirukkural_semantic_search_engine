import streamlit as st
from sentence_transformers import SentenceTransformer

from src.config import EMBEDDING_MODEL, GEMINI_API_KEY, SELECTED_LLM, LLM_GEMINI, LLM_LOCAL_LLAMA3
from src.search_logic import get_db_collection, semantic_search
from src.llm_services import get_relevance_explanation

@st.cache_resource
def load_resources():
    """Loads the search model and gets the database collection."""
    model = SentenceTransformer(EMBEDDING_MODEL)
    collection = get_db_collection()
    return model, collection

# --- Page Config ---
st.set_page_config(page_title="Thirukkural Semantic Search", page_icon="📜", layout="wide")

# --- Load Resources ---
search_model, db_collection = load_resources()

# --- Sidebar ---
with st.sidebar:
    st.image("img/logo.png", width=100) # A simple logo
    st.title("About")
    st.markdown("""
        This app uses AI to find the most relevant Thirukkural verses for any topic you provide. It performs a semantic search against the English explanations and uses a Large Language Model (LLM) to explain the relevance.
    """)
    
    st.markdown("---")

    with st.expander("⚙️ Configuration", expanded=True):
        st.info(f"Using model: **{SELECTED_LLM}**")
        # Only show API key status if Gemini is the selected model
        if SELECTED_LLM == LLM_GEMINI:
            if GEMINI_API_KEY:
                st.success("Google API Key loaded.", icon="✅")
            else:
                st.error("Google API Key not found.", icon="🚨")

# --- Main UI ---
st.title("Thirukkural Semantic Search Engine 📜")
st.subheader("There's a kural for that!")
st.markdown("Discover the timeless wisdom of Thirukkural that resonates with any concept.")

query = st.text_input("Enter a theme or topic in English that you want to explore in Thirukkural:", placeholder="e.g., 'the importance of time management'")

if st.button("Search for Wisdom", type="primary"):
    if not query:
        st.warning("Please enter a query to search.")
    elif SELECTED_LLM == LLM_GEMINI and not GEMINI_API_KEY:
        st.error("Cannot search. The Google API Key is missing or invalid.")
    else:
        results = semantic_search(query, db_collection, search_model)

        st.subheader("Top 3 Relevant Kurals:")
        if not results['ids'][0]:
            st.info("No relevant Kurals were found for your query.")
        else:
            for metadata, document in zip(results['metadatas'][0], results['documents'][0]):
                with st.spinner(f"Asking {SELECTED_LLM} for its interpretation..."):
                    relevance = get_relevance_explanation(query, document)

                st.markdown("---")
                # We use the standardized keys we created in embed_data.py
                st.markdown(f"**Kural {metadata.get('kural_no', 'N/A')}** | **Paal (Section):** {metadata.get('paal_name_tamil', 'N/A')} ({metadata.get('paal_translation_english', 'N/A')}) | **Adhikaram (Chapter):** {metadata.get('adhikaram_name_tamil', 'N/A')} ({metadata.get('adhikaram_translation_english', 'N/A')})")
                st.markdown(f"### {metadata.get('kural_tamil', 'Tamil text not found.')}")
                st.info(f"**English Explanation:** {document}\n\n**Tamil Explanation:** {metadata.get('kural_tamil_explanation', 'Tamil text not found.')}")
                #st.info(f"**Tamil Explanation:** {metadata.get('kural_tamil_explanation', 'Tamil text not found.')}")
                if "Error:" not in relevance:
                    st.success(f"**Relevance Analysis:** {relevance}")
                else:
                    st.error(relevance)