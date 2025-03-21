from chroma_server import create_chroma_client, create_chroma_collection, create_vector_store, get_retriever, get_documents_from_chroma
from ollama_server import create_llm, create_llm2
from rag_chain_initiate import refine_query, get_relevant_documents
from chat_history import save_chat_to_chromadb, get_chat_history
from settings import num_docs, kb_collection

chroma_client = create_chroma_client()
llm = create_llm()
llm2 = create_llm2(num_ctx=4096)

def ask_question(query, user_id):
    collection = create_chroma_collection(chroma_client, kb_collection)
    vectorstore = create_vector_store(chroma_client, kb_collection)
    retriever = get_retriever(vectorstore, num_docs)

    history = get_chat_history(user_id=user_id)
    refined_query = refine_query(query=query, chat_history=history, llm=llm2)
    documents = get_documents_from_chroma(query=refined_query, retriever=retriever)
    relevant_documents = get_relevant_documents(query=query, documents=documents, history=history, llm=llm2)
    
    system_prompt = f"""
    You are the customer service assistant for the company 'Clinicpoints'. 
    Your name is Clinicpoint's Chat Assistant.
    Use the following pieces of retrieved context to answer 
    the question. If you don't know the answer, say that you don't know. 
    Keep the answer concise and mention all the details in the documentation.
    You can refer to the chat history to understand past conversations but answer only the question 
    and not the questions given in the chat history. The question to be answered is at the end.
    Don't use the chat history to answer. Refer to the context as documentation.
    You may refer to the chat history to understand the query but do not answer from the chat history.
    Answer only from the context/documentation. If the answer is not in the context/documentation, say you do not know.
    \n
    Chat History: {history} \n
    Context: {relevant_documents} \n

    Query: {query}
    
    """
    
    response = llm.invoke(system_prompt)
    save_chat_to_chromadb(user_id, query, response)
    return response
    
def query_documents(query, user_id):
    collection = create_chroma_collection(chroma_client, kb_collection)
    vectorstore = create_vector_store(chroma_client, kb_collection)
    retriever = get_retriever(vectorstore, num_docs)

    history = get_chat_history(user_id=user_id)
    refined_query = refine_query(query=query, chat_history=history, llm=llm2)
    documents = get_documents_from_chroma(query=refined_query, retriever=retriever)
    relevant_documents = get_relevant_documents(query=query, documents=documents, history=history, llm=llm2)
    return relevant_documents
