from langchain_ollama import OllamaLLM, OllamaEmbeddings
from settings import llm_model, num_ctx, embed_model

def create_llm(num_ctx=num_ctx):
    return OllamaLLM(model=llm_model, base_url="http://localhost:11434", num_ctx=num_ctx)

def create_llm_embed():
    return OllamaEmbeddings(model=embed_model, base_url="http://localhost:11434")
