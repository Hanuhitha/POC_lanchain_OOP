from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings


def create_chat_model(model_name="gemma2:9b-instruct-q6_K"):
    """Method returns the chat model
    llama3:instruct
    gemma2:9b-instruct-q6_K

    Args:
        model_name (str, optional): Name of the chat model to be initialized. This only supports free ollama models. Defaults to 'openhermes'.

    Returns:
        llm: Initialized llm model
    """

    llm = ChatOllama(
        model=model_name,
        temperature=0,
        # other params...
    )
    return llm


def create_embedding_model(model_name="all-minilm"):
    """Method returns the embedding model

    Args:
        model_name (str, optional): Name of the embedding model to be initialized. This only supports free ollama models. Defaults to 'all-minilm'.

    Returns:
        llm: Initialized embeddings model
    """

    embeddings = OllamaEmbeddings(model=model_name)

    return embeddings
