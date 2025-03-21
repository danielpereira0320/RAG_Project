def refine_query(llm, query, chat_history):
    prompt = f"""
    Given a chat history and the latest user question 
    which might reference context in the chat history,
    formulate a standalone question which can be understood 
    without the chat history. Do NOT answer the question,
    just reformulate it if needed and otherwise return it as is.
    
    Query: {query};
    Chat History: {chat_history}
    """
    
    response = llm.invoke(prompt)
    return response

def get_relevant_documents(query, documents, history, llm):
    reranked_docs = []
    for doc in documents:
        prompt = f"""
        You are an AI assistant that rates the relevance of a document to a given query.
        You can use the history to understand the query but only rate the relevance of the document to the query and nothing else.
        Score from 1 (least relevant) to 10 (most relevant). Return only an integer and nothing else.
        History: {history}
        Query: {query}

        Document:
        {doc.page_content}

        Score (1-10):
        """
        response = llm.invoke(prompt)
        try:
            score = int(response)  # Extract score
        except ValueError:
            score = 5  # Default to neutral score if parsing fails

        reranked_docs.append((doc, score))

    # Sort documents based on LLM relevance score (higher is better)
    sorted_docs = sorted(reranked_docs, key=lambda x: x[1], reverse=True)
    return [doc[0] for doc in sorted_docs][:15]
