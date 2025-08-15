# app.py
import streamlit as st
from src.config import APP_TITLE, ABOUT_TEXT, CONTACT_TEXT
from src.search_logic import load_search_artifacts, semantic_search
from src.llm_services import load_llm_model, get_relevance_explanation

# --- Page Config ---
# This is retained from your original code.
st.set_page_config(page_title="Thirukkural Semantic Search", page_icon="📜", layout="wide")

# --- Load Resources (done once and cached for performance) ---
search_model, faiss_index, metadata_list = load_search_artifacts()
llm = load_llm_model()

# --- Main UI ---
# The main title and subheader from your original UI are used here.
st.title("Thirukkural Semantic Search Engine 📜")
st.subheader("There's a kural for that!")

# We use tabs as requested to create the "About" and "Contact" sections.
tab_search, tab_about, tab_contact = st.tabs(["🔍 Search", "ℹ️ About", "📧 Contact"])

# The primary search functionality is placed in the first tab.
with tab_search:
    st.markdown("Discover the timeless wisdom of Thirukkural that resonates with any concept.")
    
    # The text input and button are preserved.
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
            
            # The results header is retained.
            st.subheader("Top 3 Relevant Kurals:")
            if not results:
                st.info("No relevant Kurals were found for your query.")
            else:
                # The loop for displaying results preserves your original structure.
                for kural_data in results:
                    st.markdown("---")
                    
                    # The detailed header format is retained.
                    header = (
                        f"**Kural {kural_data.get('kural_no', 'N/A')}** | "
                        f"**Paal:** {kural_data.get('paal_name_tamil', 'N/A')} ({kural_data.get('paal_translation_english', 'N/A')}) | "
                        f"**Adhikaram:** {kural_data.get('adhikaram_name_tamil', 'N/A')} ({kural_data.get('adhikaram_translation_english', 'N/A')})"
                    )
                    st.markdown(header)
                    
                    # The Tamil Kural is displayed as a sub-headline.
                    st.markdown(f"### {kural_data.get('kural_tamil', 'Tamil text not found.')}")
                    
                    # An expander is used to keep the UI tidy, containing the explanations.
                    with st.expander("Show Explanations"):
                        st.info(f"**English Explanation:** {kural_data.get('kural_english_explanation', '')}\n\n"
                                f"**Tamil Explanation:** {kural_data.get('kural_tamil_explanation', '')}")

                    # The spinner and relevance analysis display are retained.
                    with st.spinner("Analyzing relevance with AI..."):
                        relevance = get_relevance_explanation(query, kural_data.get('kural_english_explanation', ''), llm)
                    
                    if "not available" in relevance:
                         st.warning(f"💬 **Relevance Analysis:** {relevance}")
                    else:
                         st.success(f"💬 **Relevance Analysis:** {relevance}")

# The "About" tab contains the content from your original sidebar.
with tab_about:
    st.subheader("About This App")
    st.image("img/logo.png", width=150) # The logo is retained here.
    st.markdown(ABOUT_TEXT)


# The "Contact" tab uses the new text from your config.
with tab_contact:
    st.subheader("Get In Touch")
    st.markdown(CONTACT_TEXT)