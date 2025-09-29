from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain_google_genai import ChatGoogleGenerativeAI

# -------------------------------
# Summarization Function
# -------------------------------
def summarize_document(docs, gemini_api_key: str):
    """
    Summarize a list of LangChain Document objects using Google Gemini LLM.
    """
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=gemini_api_key,
        temperature=0.3
    )

    summarization_prompt = PromptTemplate(
        input_variables=["document"],
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

                    **(Include other relevant sections as determined by the document's content)**"""
    )
    summarize_chain = StuffDocumentsChain(
        llm_chain=LLMChain(llm=llm, prompt=summarization_prompt),
        document_variable_name="document"
    )

    result = summarize_chain.invoke(docs)
    return result["output_text"] if isinstance(result, dict) and "output_text" in result else str(result)
