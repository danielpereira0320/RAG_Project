from chroma_server import create_chroma_client, create_chroma_collection, create_vector_store, delete_collection
from langchain_text_splitters import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
from settings import chat_collection, kb_collection
import json

chroma_client = create_chroma_client()


def save_current(current_section, current_content, documents):
    """ Save the current section before moving to the next one """
    if current_section and current_content:
        full_content = f"{current_section}\n\n" + "\n".join(current_content)

        documents.append({
            "title": current_section,
            "content": full_content
        })
    return documents


def extract_text_from_html(file_path):
    """Extract meaningful text from an HTML file, removing unnecessary elements."""
    with open(file_path, "r", encoding="utf-8") as file:
        soup = BeautifulSoup(file, "html.parser")

    # Extract sections
    documents = []
    current_section = None
    current_content = []
    using_h1_structure = True  # Start by using h1 as section headers

    # Loop through all relevant elements
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "p", "ul", "ol", "table"]):
        if tag.name == "h1":  
            documents = save_current(current_section=current_section, current_content=current_content, documents=documents)
            current_section = tag.get_text(strip=True)
            current_content = []
            using_h1_structure = True  # Ensure we're in the first part

        elif tag.name == "h3" and not using_h1_structure:  
            documents = save_current(current_section=current_section, current_content=current_content, documents=documents)
            current_section = tag.get_text(strip=True)
            current_content = []

        elif tag.name == "h3" and using_h1_structure:  
            # If an h3 appears AFTER h1, it means the "Modules" section has started
            documents = save_current(current_section=current_section, current_content=current_content, documents=documents)
            current_section = tag.get_text(strip=True)
            current_content = []
            using_h1_structure = False  # Switch to using h3 as section headers

        elif tag.name == "h2" and not using_h1_structure:  
            # h2 is a subsection inside the modules
            current_content.append(f"**{tag.get_text(strip=True)}**")  

        elif tag.name in ["h4", "h5"]:  
            current_content.append(f"**{tag.get_text(strip=True)}**")  

        elif tag.name == "p":  
            current_content.append(tag.get_text(strip=True))

        elif tag.name in ["ul", "ol"]:  
            for li in tag.find_all("li"):
                current_content.append(f"- {li.get_text(strip=True)}")  

        elif tag.name == "table":  
            table_rows = []
            for row in tag.find_all("tr"):
                columns = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
                table_rows.append(" | ".join(columns))
            current_content.append("\n".join(table_rows))

        # Save the last collected section
    documents = save_current(current_section=current_section, current_content=current_content, documents=documents)
    output_json = "documents.json"
    with open(output_json, "w", encoding="utf-8") as outfile:
        json.dump(documents, outfile, indent=4, ensure_ascii=False)


    with open(output_json, "r", encoding="utf-8") as file:
        data = json.load(file)

    documents = []
    for doc in data:
        documents.append(doc["content"])
    return documents

def update_collection():
    
    file_path = "data/helpcenter.html"
    texts = extract_text_from_html(file_path)
    
    delete_collection(chroma_client, kb_collection)
    collection = create_chroma_collection(chroma_client, kb_collection)
    # Initialize ChromaDB with persistence
    vectorstore = create_vector_store(chroma_client, kb_collection)
    # Store the extracted text into ChromaDB
    vectorstore.add_texts(
        texts=texts, 
    )
    return collection.count() 
    
def clear_user_history(uid):
    chroma_client = create_chroma_client()
    collection = create_chroma_collection(chroma_client, chat_collection)
    collection.delete(where={"user_id": uid})

    
def clear_entire_history():
    chroma_client = create_chroma_client()
    delete_collection(chroma_client, chat_collection)
    collection = create_chroma_collection(chroma_client, chat_collection)


