# src/qa_model.py

from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq


# -------------------------------
# Prompt Template for Legal Q&A
# -------------------------------
legal_qa_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
        You are a Legal assistant, your job is to analyze the contexts that will be given to you, and understand the context thoroughly, and give the answer that the user is expecting. In order to do that you need to understand what the user is trying to say. Make sure the answer is simple and easier for the user to understand. If you couldnt understand the user's query then clarify it and give answer.
        Answer the query in the way user wants. If the user wants you to explain a point, then explain. gather as much information on the context and give the correct answer to the user.
        Context:
        {context}

        Question:
        {question}

        Answer:"""
)


# -------------------------------
# Legal Q&A Function
# -------------------------------
def answer_query(vector_store, question, groq_api_key: str):
    """
    Retrieves relevant docs from vector store and queries the Groq LLM for legal Q&A.
    """
    retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 4})
    relevant_docs = retriever.get_relevant_documents(question)

    llm = ChatGroq(
        model_name="llama-3.1-8b-instant",
        api_key=groq_api_key,
        temperature=0.2
    )
    chain = LLMChain(llm=llm, prompt=legal_qa_prompt)

    context = "\n\n".join([doc.page_content for doc in relevant_docs])
    response = chain.invoke({"context": context, "question": question})

    if isinstance(response, dict) and "text" in response:
        return response["text"]
    return str(response)
