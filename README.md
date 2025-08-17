# Thirukkural Semantic Search Engine 📜

An intelligent, AI-powered Streamlit app to explore the timeless wisdom of the **Thirukkural**. Enter any topic or natural‑language query in English and the app surfaces the most semantically relevant Kurals — with the original Tamil, translations, and an AI explanation of *why* each verse matches your query.

---

## 🖼️ App Preview

![Homepage](img/homepage.png)
*Homepage of the Thirukkural Semantic Search Engine*

![Semantic Search](img/semantic_search.png)
*Example of a semantic search result*

---

## 🔗 Quick Links
- **Run the app:** `streamlit run app.py`
- **One-time setup:** `python embed_data.py` to build the search artifacts

---

## ✨ Features
- **Semantic Search:** Uses sentence-level embeddings and **NumPy** to calculate cosine similarity, finding meaningfully related Kurals beyond simple keywords.
- **Dual-Language Display:** Presents the original Tamil verse as a couplet, alongside both Tamil and English explanations.
- **Self-Contained AI Reasoning:** Utilizes a powerful, locally-run language model (`microsoft/Phi-3-mini`) to provide relevance explanations without needing external APIs or keys.
- **Cloud-Ready:** Architected for simple, free deployment on platforms like Hugging Face Spaces.

---

## 🛠️ Tech Stack
- **Language:** Python
- **Web Framework:** Streamlit
- **Embeddings:** `sentence-transformers`
- **Vector Search:** `NumPy` (Cosine Similarity)
- **LLM:** `microsoft/Phi-3-mini` (via Hugging Face `transformers`)

---

## 🚀 Getting Started

### Prerequisites
- Python **3.9+**
- macOS/Linux/Windows supported

### 1) Clone the repository
```bash
git clone [https://github.com/vinovator/thirukkural_semantic_search_engine.git](https://github.com/vinovator/thirukkural_semantic_search_engine.git)
cd thirukkural_semantic_search_engine
```

### 2) Create and activate a virtual environment
```bash
python3 -m venv venv
# macOS/Linux
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) One-time: build the search artifacts
```bash
python embed_data.py
```
This script reads data/thirukkural_data.json, generates sentence embeddings, and saves them as kural_embeddings.npy and kural_metadata.pkl in the search_artifacts/ directory. You only need to run this once.

---

## ▶️ Usage


### Run the app
```bash
streamlit run app.py
```
Streamlit will open the app in your browser. If you selected the local model, ensure **Ollama** is running in the background.

---

## 📂 Project Structure
```text
thirukkural_semantic_search_engine/
├── README.md                  # This file
├── app.py                     # Streamlit app (UI)
├── embed_data.py              # One-time script to build search artifacts
├── requirements.txt           # Python dependencies
├── data/
│   └── thirukkural_data.json  # Source dataset
├── search_artifacts/          # Stored embeddings and metadata
│   ├── kural_embeddings.npy
│   └── kural_metadata.pkl
├── img/                       # App screenshots/diagrams
└── src/
    ├── __init__.py
    ├── config.py              # Central configuration
    ├── llm_services.py        # All LLM calls live here
    └── search_logic.py        # Embedding + NumPy search pipeline
```
---

## 🤝 Acknowledgements
- The [`thirukkural_data.json`](data/thirukkural_data.json) dataset is sourced from the [**Thirukkural API**](https://github.com/tk120404/thirukkural) repository by **tk120404** on GitHub. Immense thanks for making this data publicly available.

---

## 🔮 Roadmap / Future Enhancements
- **Tamil Query Support:** Accept Tamil queries using a multilingual embedding model.
- **Filter by Section:** Dropdowns to filter by Paal/Adhikaram.
- **“Random Kural” Button:** Discover a random verse.
- **LLM Response Caching:** Reduce API calls and speed up repeated queries.
- **Cloud Deployment:** Use Streamlit secrets or env management (e.g., Spaces) safely.

---

## 🔐 Privacy & Security Notes
- No user queries are stored by default. Add logging consciously if needed.
- The app is self-contained and does not require API keys or external network calls after the initial model download.

---

## 🧰 Troubleshooting
- **`ModuleNotFoundError`**: Confirm your virtual env is activated and deps are installed.
- **`ImportError: numpy.core.multiarray failed to import`**: Your **`numpy`** version is likely too new. Ensure **`numpy<2.0`** is in your **`requirements.txt`** and reinstall dependencies in a clean virtual environment.
- No search results: Ensure you have successfully run **`python embed_data.py`** and that the **`search_artifacts/`** directory and its files exist.
- Slow first load: The initial download and loading of the language model can take a significant amount of time and memory. This is expected.

---

## 📜 License
This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License.
You may not use the material for commercial purposes. See the [LICENSE](LICENSE) file for details.

