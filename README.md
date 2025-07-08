# Minerva (An AI-Powered Academic Companion)

**Minerva** is a personal AI tutoring system that ingests and analyzes university lecture slides to help students understand, summarize, and self-assess their knowledge through intelligent question-answering. Designed as an end-to-end academic assistant, Minerva combines the power of Retrieval-Augmented Generation (RAG), vector embeddings, and language models to transform passive reading into active learning.

---

## Project Overview

Minerva was built as a personal AI agent with three primary capabilities:

1. **Summarizer** – distills dense academic slides into concise, digestible summaries.
2. **Quizmaster** – generates intelligent, context-aware questions to test comprehension.
3. **Explainer** – answers queries directly from your uploaded content using semantic search + LLMs.

This project was created as a proof-of-concept for AI-enabled learning. The system is modular, extensible, and locally deployable with pre-loaded slide embeddings.

---

## Key Features

| Feature        | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| Semantic Search | Uses LanceDB + vector embeddings to retrieve precise answers from slides. |
| Multi-Agent Framework | Specialized agents (oracles) for summarization, questioning, and retrieval. |
| RAG Pipeline | Integrates context retrieval with LLMs to generate relevant and grounded responses. |
| Local Storage | Slide data is embedded and stored locally, ensuring fast, offline querying. |
| Web Interface | Clean and intuitive frontend using HTML/CSS/JS with agent-specific pages. |
| Flask Backend | Lightweight and extendable backend architecture written in Python.        |

---

## Project Structure

Minerva/

app.py # Entry point - Flask app routes

agents.py # Agent definitions and behavior

rag_system.py # RAG-based response pipeline

models.py # LLM models and prompts

config.py # Configuration and secrets

database.py # LanceDB setup and document ingestion


templates/ # HTML templates for web UI

static/ # CSS and JS files

lancedb_data/ # Vector database (embeddings stored here)


requirements.txt # Python dependencies

run_minerva.bat # Local run script (Windows)

.env # API keys and secrets (not tracked)

.gitignore # Git exclusions

---

##  Setup Instructions (Local)

> Recommended: Python 3.10+ and pip

1. **Clone the repository**
git clone https://github.com/Amad-F/Minerva.git
cd Minerva

2. **Create and activate a virtual environment**
python -m venv venv
venv\Scripts\activate  # On Windows
pip install -r requirements.txt

3. **Add your API key**
Create a .env file in the root directory:
ini
OPENAI_API_KEY=your_openai_or_deepseek_key

4. **Run the application**
python app.py
Open in browser
http://127.0.0.1:5000/

## Use Case
Minerva is designed for:

- University students seeking better ways to digest lecture slides.
- Learners who want interactive revision tools.
- Developers exploring applied LLMs and vector databases.


## Tech Stack

- Python

- Flask

- SQL Alchemy

- LangChain (for RAG architecture)

- LanceDB (as vector store)

- DeepSeek APIs

- HTML, CSS, JavaScript (for UI)

## Data Handling & Privacy
All embedded content (e.g., slides) is stored locally via lancedb_data/. No user data is transmitted externally. API keys are securely handled through .env.

## Limitations & Next Steps

- No live PDF viewer or annotation support.

- Currently single-user & single-device (not multi-session).

- Slide ingestion is manual (future: drag & drop + auto-ingest).

## Planned Enhancements:

- Cloud deployment (e.g., Hugging Face Spaces or Render).

- Streamlit or Gradio-based alternate UI.

- Mobile adaptation.

- Peer-sharing mode for study groups.


## Author

Amad Fareed

📌 GitHub: @Amad-F

🌐 LinkedIn: https://www.linkedin.com/in/amad-fareed-308229239/

## Feedback & Contributions
Pull requests and feedback are welcome. If you’re interested in extending Minerva or collaborating, feel free to open an issue or reach out via LinkedIn.
