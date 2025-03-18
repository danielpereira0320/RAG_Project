from chroma_server import create_chroma_client, create_chroma_collection, create_vector_store, get_retriever, get_documents_from_chroma
from ollama_server import create_llm
from rag_chain_initiate import refine_query, get_relevant_documents
from chat_history import save_chat_to_chromadb, get_chat_history
from settings import num_docs, kb_collection

chroma_client = create_chroma_client()
llm = create_llm()

def ask_question(query, user_id):
    collection = create_chroma_collection(chroma_client, kb_collection)
    vectorstore = create_vector_store(chroma_client, kb_collection)
    retriever = get_retriever(vectorstore, num_docs)

    history = get_chat_history(user_id=user_id)
    refined_query = refine_query(query=query, chat_history=history, llm=llm)
    documents = get_documents_from_chroma(query=refined_query, retriever=retriever)
    relevant_documents = get_relevant_documents(query=query, documents=documents, history=history, llm=llm)
    
    system_prompt = f"""
    You are the customer service assistant for the company 'Clinicpoints'. 
    Your name is Clinicpoint's Chat Assistant.
    Use the following pieces of retrieved context to answer 
    the question. If you don't know the answer, say that you 
    don't know. Use five sentences maximum and keep the 
    answer concise. Answer only in English and not in any other language.
    Answer as if you are a customer service agent of the company.
    You can refer to the chat history to understand past conversations but answer only the question 
    and not the questions given in the chat history. The question to be answered is at the end.
    Don't use the chat history to answer. Refer to the context as documentation.
    You may refer to teh chat history to understand the query but do not answer from the chat history.
    Answer only from the context. If the answer is not in the context, say you do not know.
    \n
    Chat History: {history} \n
    Context: {relevant_documents} \n

    Query: {query}
    
    """
    
    response = llm.invoke(system_prompt)
    save_chat_to_chromadb(user_id, query, response)
    return response
    