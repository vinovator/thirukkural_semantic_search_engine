# app.py
import streamlit as st
from src.config import APP_TITLE, ABOUT_TEXT, CONTACT_TEXT
from src.search_logic import load_search_artifacts, semantic_search
from src.llm_services import load_llm_model, get_relevance_explanation

# --- Page Config ---
st.set_page_config(page_title="Thirukkural Semantic Search", page_icon="📜", layout="wide")

# --- Load Resources (done once and cached for performance) ---
search_model, faiss_index, metadata_list = load_search_artifacts()
llm = load_llm_model()

# --- Sidebar ---
# The "About" and "Contact" sections are now combined in the sidebar.
with st.sidebar:
    st.image("img/logo.png", width=120)
    st.header("About This App")
    st.markdown(ABOUT_TEXT)
    st.markdown("---")
    st.header("Contact")
    st.markdown(CONTACT_TEXT)

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
            results = semantic_search(query, search_model, faiss_index, metadata_list)
        
        st.subheader("Top 3 Relevant Kurals:")
        if not results:
            st.info("No relevant Kurals were found for your query.")
        else:
            for kural_data in results:
                st.markdown("---")
                header = (
                    f"**Kural {kural_data.get('kural_no', 'N/A')}** | "
                    f"**Paal:** {kural_data.get('paal_name_tamil', 'N/A')} ({kural_data.get('paal_translation_english', 'N/A')}) | "
                    f"**Adhikaram:** {kural_data.get('adhikaram_name_tamil', 'N/A')} ({kural_data.get('adhikaram_translation_english', 'N/A')})"
                )
                st.markdown(header)
                #st.markdown(f"### {kural_data.get('kural_tamil', 'Tamil text not found.')}")
                line1 = kural_data.get('Line1', '')
                line2 = kural_data.get('Line2', '')
                st.markdown(f"### {line1}<br>{line2}", unsafe_allow_html=True)
                
                # The expander is now set to be expanded by default.
                with st.expander("Show Explanations", expanded=True):
                    st.info(f"**English Explanation:** {kural_data.get('kural_english_explanation', '')}\n\n"
                            f"**Tamil Explanation:** {kural_data.get('kural_tamil_explanation', '')}")

                with st.spinner("Analyzing relevance with AI..."):
                    relevance = get_relevance_explanation(query, kural_data.get('kural_english_explanation', ''), llm)
                
                if "not available" in relevance:
                     st.warning(f"💬 **Relevance Analysis:** {relevance}")
                else:
                     st.success(f"💬 **Relevance Analysis:** {relevance}")