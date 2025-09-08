import streamlit as st
import requests
import os
from datetime import datetime, timedelta
from urllib.parse import urlparse
import streamlit.components.v1 as components
import PyPDF2
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.question_answering import load_qa_chain
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.prompts import PromptTemplate
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract
from pdf2image import convert_from_bytes
from langchain.docstore.document import Document
from dateutil import parser as date_parser
import torch
import hashlib

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")

PERSIST_DIR = "chroma_db"
os.makedirs(PERSIST_DIR, exist_ok=True)

# Prompt template for legal Q&A
legal_qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
        You are a highly intelligent and experienced legal assistant trained to respond to legal questions based on the provided context. Your role is to help users understand complex legal concepts, documents, and case details in simple, clear terms while ensuring high accuracy. 

        Follow these guidelines strictly to minimize errors:

        1. **Interpret and identify legal roles**: When a name is mentioned, immediately identify its role in the legal context (e.g., defendant, plaintiff, judge, attorney, etc.). If a name is associated with a particular role, clearly state the name and its role.

        2. **Provide direct and precise answers**: If the question is asking for specific details like names, roles, or events, extract the relevant information from the context and give it directly.

        3. **Clarify the context of the question**: When a question is broad or vague, ensure to frame the answer with the correct legal context, explaining who the person is and their role in the case.

        4. **Answer in clear and simple language**: Always ensure that your responses are understandable to someone without legal training. Use simple and plain language, avoiding legal jargon unless necessary for clarity. When using legal terms, provide a brief explanation for non-experts.

        5. **Contextual awareness**: If the question asks for information that's not present in the context, do not invent an answer. Instead, be honest and respond with: "The information provided does not contain sufficient details to answer this question."

        6. **Handle ambiguity carefully**: If a name or role is mentioned without sufficient context, provide a cautious answer.

        7. **Cross-check for consistency**: If the context includes multiple references to the same person or event, make sure your response aligns with those references. Be careful not to introduce inconsistencies in the answer.

        8. **Avoid assumptions**: Do not assume facts that aren't directly provided in the context. If the document doesn't clarify a role, relationship, or specific information, simply state that the information is missing.

        Context:
        {context}

        Question:
        {question}

        Answer:"""
)

# -------------------------------
# Section 1: PDF Assistant Logic
# -------------------------------                                           
def extract_text_from_pdf(uploaded_file):
    pdf_bytes = uploaded_file.read()
    uploaded_file.seek(0)  # reset pointer for re-use

    reader = PyPDF2.PdfReader(uploaded_file)
    images = convert_from_bytes(pdf_bytes)
    documents = []

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text and text.strip():
            documents.append(Document(page_content=text.strip(), metadata={"page": i+1}))
        else:
            ocr_text = pytesseract.image_to_string(images[i])
            if ocr_text.strip():
                documents.append(Document(page_content=ocr_text.strip(), metadata={"page": i+1}))
    
    return documents


def split_text_into_chunks(documents, chunk_size=800, chunk_overlap=100):
    text_chunks = []
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    for doc in documents:
        chunks = splitter.split_text(doc.page_content)
        for c in chunks:
            text_chunks.append(Document(page_content=c, metadata=doc.metadata))

    return text_chunks

def get_doc_hash(file_bytes: bytes) -> str:
    """Generate unique hash for a PDF (cache key)."""
    return hashlib.md5(file_bytes).hexdigest()

def get_or_create_vector_store(docs, file_bytes, batch_size=32):
    """
    Create/load Chroma vector store with caching.
    """
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={"device": "cuda" if torch.cuda.is_available() else "cpu"},
        encode_kwargs={"batch_size": batch_size, "normalize_embeddings": True}
    )

    vectordb = Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    doc_id = get_doc_hash(file_bytes)
    existing_ids = vectordb.get()["ids"]

    if any(doc_id in i for i in existing_ids):
        print("✅ Loaded embeddings from cache")
    else:
        print("⚡ Creating embeddings & caching for future use...")
        vectordb.add_documents(
            docs,
            ids=[f"{doc_id}_{i}" for i in range(len(docs))]
        )
        vectordb.persist()

    return vectordb

def answer_query(vector_store, question):
    # Proper RAG: retrieve docs → feed to Groq model
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 4})
    relevant_docs = retriever.get_relevant_documents(question)

    llm = ChatGroq(model_name="llama3-8b-8192", api_key=groq_api_key, temperature=0.0)
    chain = LLMChain(llm=llm, prompt=legal_qa_prompt)

    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    response = chain.invoke({"context": context, "question": question})
    
    if isinstance(response, dict) and "text" in response:
        return response["text"]
    return str(response)


def summarize_document(docs):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=gemini_api_key, temperature=0.3)
    summarization_prompt = PromptTemplate(
        input_variables=["document"], # Change to 'document' as we are stuffing all docs
        template="""You are a legal document summarizer. Your task is to extract the most important and relevant information from the provided legal document.

                    Summarize the document by organizing the key details into logical, clearly titled sections. The specific headings for these sections should be determined by the content and nature of the document itself.

                    For each section, use bullet points to present individual pieces of information clearly and concisely. Ensure all information is directly relevant to the document's main purpose. Maintain a neutral, objective, and professional tone throughout the summary.

                    **Input Text:**
                    [{document}]

                    **Expected Output Format Example (Headings will vary based on document content):**

                    **[Main Topic/Document Type Title]:**
                    * [Key point 1 about the topic]
                    * [Key point 2 about the topic]

                    **[Relevant Section Heading 1]:**
                    * [Important detail 1]
                    * [Important detail 2]

                    **[Relevant Section Heading 2]:**
                    * [Important detail 1]
                    * [Important detail 2]

                    **(Include other relevant sections as determined by the document's content)**""")
    summarize_chain = StuffDocumentsChain(
        llm_chain=LLMChain(llm=llm, prompt=summarization_prompt),
        document_variable_name="document"
    )

    result = summarize_chain.invoke(docs)
    return result["output_text"] if isinstance(result, dict) and "output_text" in result else str(result)

# -------------------------------
# Section 2: Legal News Logic
# -------------------------------
def fetch_legal_news():
    today = datetime.today().strftime('%Y-%m-%d')
    last_week = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    url = (
        "https://newsapi.org/v2/everything?"
        "q=("
        "%22court ruling%22 OR %22supreme court%22 OR %22high court%22 OR lawsuit OR "
        "%22legal battle%22 OR %22constitutional law%22 OR %22judicial decision%22 OR "
        "%22human rights law%22 OR %22legal reform%22 OR %22legislation passed%22"
        ") AND NOT entertainment AND NOT cinema AND NOT film AND NOT tv AND NOT drama&"
        f"from={last_week}&to={today}&"
        "language=en&"
        "sortBy=popularity&"
        "pageSize=5&"
        f"apiKey={NEWS_API_KEY}"    
    )   
    response = requests.get(url)
    if response.status_code != 200:
        st.warning("Unable to fetch news at this time.")
        return []
    return response.json().get("articles", [])


def show_news_articles(articles):
    st.markdown("### 📰 Latest Trending Legal News")
    if not articles:
        st.info("No news articles found.")
        return

    for i, article in enumerate(articles):
        st.markdown("---")
        st.markdown(f"**[{article['title']}]({article['url']})**")
        try:
            published_at = date_parser.parse(article['publishedAt'])
            st.write(f"🕒 Published: {published_at.strftime('%d %b %Y, %H:%M')}")
        except Exception:
            st.write("🕒 Published: Unknown")
        st.write(f"🏛 Source: {article['source']['name']}")
        if article.get("description"):
            st.write(f"📄 {article['description']}")


# -------------------------------
# Streamlit Combined App
# -------------------------------
def main():
    st.set_page_config(page_title="Legal Assistant", layout="wide")
    st.sidebar.title("🧭 Navigation")
    section = st.sidebar.radio("Go to", ["📚 PDF Assistant", "🗞️ Global Legal News"])

    if section == "📚 PDF Assistant":
        st.title("📚 PDF Assistant: Summarization + Legal Q&A")
        uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])
        if uploaded_file:
            documents = extract_text_from_pdf(uploaded_file)

            total_length = sum(len(doc.page_content) for doc in documents)
            if total_length < 50:
                st.warning("Text too short. Please upload a valid document.")
                return

            docs = split_text_into_chunks(documents)

            if "vector_store" not in st.session_state or st.session_state.get("file") != uploaded_file.name:
                st.session_state.vector_store = get_or_create_vector_store(docs)
                st.session_state.file = uploaded_file.name

            mode = st.radio("Choose an option", ["Summarize Document", "Ask a Question"])
            if mode == "Summarize Document" and st.button("Generate Summary"):
                with st.spinner("Summarizing..."):
                    summary = summarize_document(docs)
                st.markdown("#### 🧾 Summary:")
                st.markdown(summary)
            elif mode == "Ask a Question":
                question = st.text_input("Enter your legal question:")
                if st.button("💬 Get Answer") and question.strip():
                    with st.spinner("Thinking..."):
                        answer = answer_query(st.session_state.vector_store, question)
                    st.markdown("### 💬 Answer:")
                    st.write(answer)

    elif section == "🗞️ Global Legal News":
        st.title("🗞️ Global Legal News Digest")
        st.markdown("Latest popular legal news from around the world.")
        articles = fetch_legal_news()
        show_news_articles(articles)

if __name__ == "__main__":
    main()
