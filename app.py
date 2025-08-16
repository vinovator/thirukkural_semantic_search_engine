# app.py
import streamlit as st
from src.config import APP_TITLE, ABOUT_TEXT, CONTACT_TEXT, LLM_PROVIDER, LLM_PROVIDER_HUGGINGFACE
from src.search_logic import load_search_artifacts, semantic_search
from src.llm_services import load_hf_model, get_relevance_explanation

# --- Page Config ---
st.set_page_config(page_title="Thirukkural Semantic Search", page_icon="📜", layout="wide")

# --- CUSTOM CSS ---
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        width: 350px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Load Resources ---
search_model, embeddings, metadata_list = load_search_artifacts()

# Conditionally load the Hugging Face model
model, tokenizer = None, None
if LLM_PROVIDER == LLM_PROVIDER_HUGGINGFACE:
    model, tokenizer = load_hf_model()

# --- Sidebar ---
with st.sidebar:
    st.image("img/logo.png", width=120)
    st.header("About This App")
    st.markdown(ABOUT_TEXT)
    st.markdown("---")
    st.header("Contact")
    st.markdown(CONTACT_TEXT, unsafe_allow_html=True)

# --- Main UI ---
st.title("Thirukkural Semantic Search Engine 📜")
st.subheader("There's a kural for that!")
st.markdown("Discover the timeless wisdom of Thirukkural that resonates with any concept.")

query = st.text_input(
    "Enter a theme or topic in English that you want to explore in Thirukkural:",
    placeholder="e.g., 'the importance of time management'"
)

if st.button("Search for Wisdom", type="primary"):
    if not query:
        st.warning("Please enter a query to search.")
    else:
        with st.spinner("Searching for the most relevant verses..."):
            results = semantic_search(query, search_model, embeddings, metadata_list)
        
        st.subheader("Top 3 Relevant Kurals:")
        if not results:
            st.info("No relevant Kurals were found for your query.")
        else:
            # --- MODIFIED LOGIC STARTS HERE ---
            
            # Step 1: Display all Kurals and create empty placeholders.
            placeholders = []
            for kural_data in results:
                st.markdown("---")
                header = (
                    f"**Kural {kural_data.get('kural_no', 'N/A')}** | "
                    f"**Paal:** {kural_data.get('paal_name_tamil', 'N/A')} ({kural_data.get('paal_translation_english', 'N/A')}) | "
                    f"**Adhikaram:** {kural_data.get('adhikaram_name_tamil', 'N/A')} ({kural_data.get('adhikaram_translation_english', 'N/A')})"
                )
                st.markdown(header)
                
                line1 = kural_data.get('Line1', '')
                line2 = kural_data.get('Line2', '')
                st.markdown(f"### {line1}<br>{line2}", unsafe_allow_html=True)
                
                with st.expander("Show Explanations", expanded=True):
                    st.info(f"**English Explanation:** {kural_data.get('kural_english_explanation', '')}\n\n"
                            f"**Tamil Explanation:** {kural_data.get('kural_tamil_explanation', '')}")
                
                placeholders.append(st.empty())

            # Step 2: Now, fill each placeholder with a spinner while generating its explanation.
            for i, kural_data in enumerate(results):
                # Use the placeholder as a container for the spinner
                with placeholders[i]:
                    with st.spinner("💬 Analyzing relevance with AI..."):
                        relevance = get_relevance_explanation(
                            query, 
                            kural_data.get('kural_english_explanation', ''),
                            model,
                            tokenizer
                        )
                
                # After the spinner is done, fill the placeholder with the final result
                if "not available" in relevance:
                     placeholders[i].warning(f"💬 **Relevance Analysis:** {relevance}")
                else:
                     placeholders[i].success(f"💬 **Relevance Analysis:** {relevance}")
else:
    st.info("Enter a query above and click 'Search for Wisdom' to begin.")