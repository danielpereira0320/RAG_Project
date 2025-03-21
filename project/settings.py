llm_model = "llama3.2" # The model used for queries
embed_model = "mxbai-embed-large" # The model used for document queries. If the model is changed, the collections have to be reset.
num_ctx = 16000 # The number of tokens that the model will use. Depends on context size.
num_docs = 25 # The number of documents imported. More documents mean higher context size.
chat_collection = "chat_history"
kb_collection = "clinicpoints"


