# 🚀 DONNA Impact Log – 09 April 2025

## 🧠 Summary
Kicked off development of **DONNA** (Document-Oriented Neural Network Assistant), a GenAI project aimed at legal document summarization and question answering.  
The underlying architecture is **TALQS** (Transformer-based Architecture for Legal Question Answering & Summarization).

## ✅ Progress
- Finalized project branding:  
  - **Product Name:** DONNA  
  - **Architecture Codename:** TALQS  
- Broke project into 2 core modules:
  - Legal Summarization
  - Legal Question Answering
- Mapped end-to-end input/output pipeline from PDF ingestion to final response.
- Explored PDF parsing, chunking strategies, and transformer-based summarization.

## 🧰 Stack & Tools
- Python, Hugging Face Transformers
- PyMuPDF for PDF parsing
- T5 / BART / LongformerEncoderDecoder (LED) for summarization
- GitHub for version control and documentation

## 🔥 Next Steps
- Begin building PDF-to-text extraction module
- Implement document chunking and test with `t5-base`
- Start setting up summarizer pipeline

> "If you're gonna do this, you better go all in. Like Donna would."  
> — Logged by Hrishikesh Raparthi
