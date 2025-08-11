#Thirukural Semantic Search Engine 📜
An intelligent, AI-powered web application to explore the timeless wisdom of the Thirukural. This app allows users to enter a query or topic in English and find the most semantically relevant Kural verses, complete with explanations and AI-generated relevance analysis.

##✨ Features
●	Semantic Search: Go beyond keywords. The app understands the meaning behind your query to find the most relevant verses.
●	Dual Language Display: View the original Kural in Tamil, alongside its English and Tamil explanations.
●	AI-Powered Relevance Analysis: For each result, a Large Language Model (LLM) provides a concise explanation of why the verse is relevant to your query.
●	Developer-Friendly LLM Toggling: Easily switch between a powerful cloud API (Google Gemini) and a private, offline local model (Llama 3) for relevance analysis by changing a single line of code.

##🛠️ Tech Stack
●	Backend: Python
●	Web Framework: Streamlit
●	AI & Machine Learning:
○	Embeddings: sentence-transformers
○	Vector Database: ChromaDB
○	LLM Services (configurable):
■	Google Gemini API (google-generativeai)
■	Local Llama 3 via Ollama

##🚀 Getting Started
Follow these steps to set up and run the project on your local machine.
1. Prerequisites
●	Python 3.8 or higher
●	Ollama installed on your machine (for local model support).
2. Installation & Setup
a. Clone the repository:
git clone <your-repository-url>
cd thirukural-search-engine

b. Create a virtual environment:
python3 -m venv venv
source venv/bin/activate

c. Install dependencies:
pip install -r requirements.txt

d. Set up environment variables (for Google Gemini):
Create a file named .env in the root directory of the project and add your Google API key:
GEMINI_API_KEY="your_google_api_key_here"

e. Download the local LLM (for Ollama):
Run the following command in your terminal. This will download the Llama 3 model (one-time download).
ollama run llama3

3. One-Time Data Embedding
Before running the app for the first time, you must process the source data and create the vector database.
Run the embedding script from the root directory:
python embed_data.py

This script will read data/thirukkural_data.json, generate embeddings, and store them in the chromadb/ directory. You only need to do this once.

##Usage
1. Configure the LLM Service
Open the file src/config.py. You can choose which LLM to use for relevance analysis by changing the SELECTED_LLM variable.
●	To use Google Gemini (Cloud API):
SELECTED_LLM = LLM_GEMINI

●	To use Llama 3 (Local Model):
SELECTED_LLM = LLM_LOCAL_LLAMA3

2. Run the Application
Make sure your virtual environment is activated and Ollama is running (if you selected the local model).
streamlit run app.py

The application will open in your web browser.

##📂 Project Structure
thirukural-search-engine/
│
├── .env                  # Stores API keys (not committed to git)
├── .gitignore            # Specifies files to ignore for git
├── app.py                # Main Streamlit application UI
├── embed_data.py         # One-time script to create the vector DB
├── requirements.txt      # Project dependencies
│
├── data/
│   └── thirukkural_data.json # The source data file
│
├── chromadb/             # Directory for the local vector database
│
└── src/
    ├── __init__.py
    ├── config.py         # Central configuration and the LLM master switch
    ├── llm_services.py   # Handles all communication with LLMs
    └── search_logic.py   # Manages database connection and semantic search

##🙏 Acknowledgements
●	The thirukkural_data.json dataset used in this project was sourced from the Thirukkural API repository by tk120404 on GitHub. A huge thank you for making this data publicly available.

##🔮 Future Enhancements
This project has a solid foundation. Here are some potential features and improvements for the future:
●	Display Paal and Adhikaram: Show the "Part" and "Chapter" for each Kural in the UI.
●	Search in Tamil: Allow users to enter queries directly in Tamil by using a multilingual embedding model.
●	Filter by Section: Add dropdowns to filter search results by Paal or Adhikaram.
●	"Random Kural" Button: Add a feature to display a random verse for discovery.
●	Advanced Caching: Cache LLM responses for repeated queries to reduce API calls and improve speed.
●	Deployment Enhancements: Adapt the app to use Streamlit's secrets management for secure key handling in a cloud environment.
