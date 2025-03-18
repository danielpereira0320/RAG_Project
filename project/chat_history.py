from chroma_server import create_chroma_collection, create_chroma_client, create_vector_store
from settings import chat_collection

chroma_client = create_chroma_client()

def save_chat_to_chromadb(user_id, query, response):
    collection = create_chroma_collection(chroma_client, chat_collection)

    collection.add(
        ids=[f"{user_id}-{len(collection.get()['ids'])}"],  # Unique ID per message
        documents=[query],
        metadatas=[{"user_id": user_id, "query": query, "response": response}]
    )

def get_entire_chat():
    collection = create_chroma_collection(chroma_client, chat_collection)
    results = collection.get()
    chat = results["metadatas"]

    return chat

def get_chat_history(user_id, k=2):
    collection = create_chroma_collection(chroma_client, chat_collection)
    results = collection.get(where={"user_id": user_id})  # Get messages for this user
    chat_history = results["metadatas"][-k:]  # Get last k messages

    # Convert to LangChain format
    formatted_history = []
    for entry in chat_history:
        chat = f"Query: {entry['query']}, Response: {entry['response']}"
        formatted_history.append(chat)

    return formatted_history
