
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings



def create_chat_model(model_name = 'openhermes'):

    llm = ChatOllama(
        model = model_name,
        temperature=0,
        # other params...
    )
    return llm

def create_embedding_model(model_name = 'all-minilm'):
    
    embeddings = OllamaEmbeddings(model= model_name)

    return embeddings
    