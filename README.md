# DONNA - Domain-Specific Legal AI Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)  
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)  
![FastAPI](https://img.shields.io/badge/FastAPI-API%20Backend-teal.svg)  
![React](https://img.shields.io/badge/React-Frontend-blue.svg)  
![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC.svg)

> *"AI is transforming industries — but law remains locked in complexity. DONNA is built to change that."*

**DONNA** (Document-Oriented Legal AI Assistant) is a legal AI system designed to make legal documents and processes **accessible, understandable, and efficient**. It combines **state-of-the-art LLMs** with **intelligent retrieval pipelines** to assist lawyers, students, and citizens in navigating complex legal information. 

---

## Features

- **Multi-LLM Architecture**  
  - **Groq Llama 3.1** for precision legal reasoning  
  - **Google Gemini Flash** for structured summarization  
- **RAG-Powered Pipeline**  
  - Smart chunking + semantic retrieval (Chroma + HuggingFace embeddings)  
- **Human-Centered Design**  
  - Session-based chat (temporary memory, like a legal co-pilot)  
  - Inline news digest (no distraction, no extra clicks)  
- **Efficiency First**  
  - Embedding caching for fast re-queries  
  - GPU/CPU-optimized batching  

---

## Tech Stack

- **Backend:** FastAPI + LangChain + ChromaDB + HuggingFace Embeddings
- **LLMs:** Groq Llama 3.1 (Q&A), Gemini 2.0 Flash (Summarization)
- **Frontend:** React.js + TailwindCSS
- **OCR/Parsing:** PyPDF2, pdf2image, pytesseract

---

## Installation & Setup

### Prerequisites

- Python **3.10+**
- Node.js **18+**
- [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/) installed on your system
- [Poppler](https://poppler.freedesktop.org/) (required for `pdf2image`)
- API Keys for:
  - [Groq](https://console.groq.com/)
  - [Google Gemini](https://aistudio.google.com/)
  - [News API](https://newsapi.org/)

---

### Environment Variables
#### 1. Copy the template file:

```bash
cp .env.example .env
```
#### 2. Replace the placeholder values in `.env` with your actual API keys:

```bash
# .env
GROQ_API_KEY="your_real_groq_api_key"
GEMINI_API_KEY="your_real_gemini_api_key"
NEWS_API_KEY="your_real_news_api_key"
```
⚠️ Do not commit your `.env` file to GitHub, it is already ignored in `.gitignore`.

Make sure to setup backend and frontend in different terminals.
(*use cmd, not powershell*)
#### 3. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### 4. Frontend Setup 
```bash
cd frontend
npm install
npm start
```
---
## Project structure
```bash
DONNA-LegalAI/
├── .env              # API keys (not committed, you will be creating this file.)
├── .env.example      # Example template for ".env"
├── .gitignore        # Ignore env
├── LICENSE           # MIT License
├── README.md         # Project documentation
├── backend/          # Python FastAPI backend
│   ├── main.py
│   └── src/
│       ├── __init__.py
│       ├── pdf_handler.py
│       ├── summarization_model.py
│       ├── qa_model.py
│       └── news_fetcher.py
└── frontend/         # React frontend
    ├── package.json
    ├── public/
    │   └──index.html
    └── src/
        ├── App.css
        ├── App.js
        ├── index.css
        ├── index.js
        ├──LandingPage.css
        └──LandingPage.js
```
---

## Example Use Cases  

- **Law Students**: Quickly summarize 200-page case law before class.  
- **Lawyers**: Ask direct questions from a client's contract PDF.  
- **Policy Analysts**: Track global legal reforms in real time.  
- **Citizens**: Understand your rights without needing to parse jargon.  

---
## Research Basis  

- [*Attention Is All You Need* - Vaswani et al. (2017)](https://arxiv.org/abs/1706.03762)  
- [*Retrieval-Augmented Generation for Knowledge-Intensive NLP* - Lewis et al. (2020)](https://arxiv.org/abs/2005.11401)  
- Recent advancements in **domain-specific LLMs** & **efficient retrieval pipelines**  

---

## License  

This project is licensed under the [MIT License](LICENSE).  

---
## Authors

- [@Hrishhii](https://www.github.com/Hrishhii)

