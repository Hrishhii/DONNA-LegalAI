from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from src.pdf_handler import extract_text_from_pdf, split_text_into_chunks, get_or_create_vector_store
from src.qa_model import answer_query
from src.summarization_model import summarize_document
from src.news_fetcher import fetch_legal_news
import os
import io

# -------------------------
# Load API keys from env
# -------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# -------------------------
# FastAPI setup
# -------------------------
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict to your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# In-memory storage (only one doc at a time)
# -------------------------
active_pdf = {
    "name": None,
    "documents": None,
    "vectorstore": None,
}

# -------------------------
# Routes
# -------------------------
@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """
    Upload a single PDF and replace any existing one.
    """
    try:
        # Read file bytes
        file_bytes = await file.read()
        
        # Create a file-like object from bytes for extract_text_from_pdf
        file_obj = io.BytesIO(file_bytes)
        
        # Extract text from uploaded file
        documents = extract_text_from_pdf(file_obj)
        
        if not documents:
            return {"error": "Failed to extract text from PDF"}
        
        # Create chunks and vector store
        chunks = split_text_into_chunks(documents)
        vectordb = get_or_create_vector_store(chunks, file_bytes)
        
        # Replace active doc
        active_pdf["name"] = file.filename
        active_pdf["documents"] = documents
        active_pdf["vectorstore"] = vectordb
        
        return {"message": f"Uploaded {file.filename} successfully", "pages": len(documents)}
        
    except Exception as e:
        return {"error": f"Failed to process PDF: {str(e)}"}

@app.post("/summarize")
async def summarize():
    """
    Summarize the active PDF.
    """
    try:
        if not active_pdf["documents"]:
            return {"error": "No PDF uploaded yet."}
        
        summary = summarize_document(active_pdf["documents"], GEMINI_API_KEY)
        return {"summary": summary}
        
    except Exception as e:
        return {"error": f"Failed to summarize: {str(e)}"}

@app.post("/ask-query")
async def ask_query(question: str = Form(...)):
    """
    Answer a legal question using the active PDF only.
    """
    try:
        if not active_pdf["vectorstore"]:
            return {"error": "No PDF uploaded yet."}
        
        answer = answer_query(active_pdf["vectorstore"], question, GROQ_API_KEY)
        return {"question": question, "answer": answer}
        
    except Exception as e:
        return {"error": f"Failed to process question: {str(e)}"}

@app.get("/legal-news")
def legal_news():
    """
    Fetch trending legal news.
    """
    try:
        articles = fetch_legal_news(NEWS_API_KEY)
        return {"articles": articles}
        
    except Exception as e:
        return {"error": f"Failed to fetch news: {str(e)}"}