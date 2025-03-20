from langchain_chroma import Chroma
import chromadb
from ollama_server import create_llm_embed

def create_chroma_client():
    return chromadb.HttpClient(host="localhost", port=8000)


def create_chroma_collection(chroma_client, collection_name):
    try:
        return chroma_client.create_collection(name=collection_name, embedding_function=create_llm_embed())
    except:
        return chroma_client.get_collection(name=collection_name)        

def create_vector_store(chroma_client, collection_name):
    vectorstore = Chroma(
        client=chroma_client,  # Use the running ChromaDB server
        collection_name=collection_name,
        embedding_function=create_llm_embed()
    )
    return vectorstore

def get_retriever(vectorstore, k_num):
    return vectorstore.as_retriever(search_type="mmr",search_kwargs={"k": k_num}, search_params={"lambda": 0.6}) 

def delete_collection(chroma_client, collection_name):
    try:
        chroma_client.delete_collection(collection_name)
    except:
        pass

def get_documents_from_chroma(query, retriever):
    documents = retriever.invoke(query)
    return documents
