import PyPDF2
import pytesseract
from pdf2image import convert_from_bytes
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.docstore.document import Document
import torch
import hashlib
import os

# Directory for Chroma persistence
PERSIST_DIR = "chroma_db"
os.makedirs(PERSIST_DIR, exist_ok=True)


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from PDF pages. If no text is found, fall back to OCR.
    Returns a list of langchain Document objects with page metadata.
    """
    pdf_bytes = uploaded_file.read()
    uploaded_file.seek(0)  # reset pointer for re-use

    reader = PyPDF2.PdfReader(uploaded_file)
    images = convert_from_bytes(pdf_bytes)
    documents = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            documents.append(Document(page_content=text.strip(), metadata={"page": i + 1}))
        else:
            ocr_text = pytesseract.image_to_string(images[i])
            if ocr_text.strip():
                documents.append(Document(page_content=ocr_text.strip(), metadata={"page": i + 1}))

    return documents


def split_text_into_chunks(documents, chunk_size=800, chunk_overlap=100):
    """
    Split extracted documents into smaller overlapping chunks
    for better handling in embedding/vectorization.
    """
    text_chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    for doc in documents:
        chunks = splitter.split_text(doc.page_content)
        for c in chunks:
            text_chunks.append(Document(page_content=c, metadata=doc.metadata))

    return text_chunks


def get_doc_hash(file_bytes: bytes) -> str:
    """
    Generate a unique hash for a PDF file (used for caching embeddings).
    """
    return hashlib.md5(file_bytes).hexdigest()


def get_or_create_vector_store(docs, file_bytes, batch_size=32):
    """
    Create a fresh vector store for each new document (single-doc mode).
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
        encode_kwargs={"batch_size": batch_size, "normalize_embeddings": True}
    )

    # Create a fresh vector store (no persistence for single-doc mode)
    vectordb = Chroma(embedding_function=embeddings)
    
    print("⚡ Creating fresh embeddings for new document...")
    doc_id = get_doc_hash(file_bytes)
    vectordb.add_documents(docs, ids=[f"{doc_id}_{i}" for i in range(len(docs))])
    
    return vectordb