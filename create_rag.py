import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader


class Rag:
    """An Abstract RAG generation class"""

    def __init__(
        self, source, destination, embeddings, max_chunk_size=1000, chunk_overlap=400
    ):
        """Initialize the RAG object

        Args:
            source (str): Source path to the files to be loaded into RAG
            destination (str): Destination path to which RAG database is stored
            embeddings (model): Embedding model used for generating the embeddings
            max_chunk_size (int, optional): Max chunk size to partition the documents. Defaults to 1000.
            chunk_overlap (int, optional): Chunk overlap. Defaults to 400.
        """
        self.source = source
        self.destination = destination
        self.embeddings = embeddings
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap

    def create_db(self):
        """Overwrite with appropriate functionality"""
        pass


class CoderRag(Rag):
    """CoderRag is defined to specifically generate a RAG which stores the leetcode codes.

    The idea is to store leetcode question as a chunk and the related answer code in metadata. For a given
    user query, the retriever will find the closest question in the database and use the reference code to generate
    new code.
    """

    def __init__(self, source, destination, embeddings):
        super().__init__(source, destination, embeddings)

    def create_db(self):
        """Method generates the RAG for CODE

        Returns:
            Croma: return a chroma db
        """
        if not os.path.isdir(self.destination):
            splitted_doc = []
            text_splitter = CharacterTextSplitter()
            for i in os.listdir(self.source):
                filepath = self.source + "/" + i
                loader = TextLoader(filepath)
                doc = loader.load()

                for d in doc:
                    question = []
                    for i,x in enumerate(d.page_content.split()):
                        if "class" in x:
                            break
                        question.append(x)
                    res = "".join(question)
                    d.metadata = {"code": "".join(d.page_content.split()[i:])}
                    d.page_content = res

                splitted_doc.extend(text_splitter.split_documents(doc))

            while True:
                if len(splitted_doc) == 0:
                    break
                db = Chroma.from_documents(
                    splitted_doc[:150],
                    self.embeddings,
                    persist_directory=self.destination,
                )
                splitted_doc = splitted_doc[150:]
        else:
            db = Chroma(
                embedding_function=self.embeddings, persist_directory=self.destination
            )

        return db


class SummaryRag(Rag):
    """SummaryRag is defined to specifically generate a RAG which stores the research paper data.

    The idea is to store reasearch papers as a chunks. For a given user query, the retriever will find
    the closest chunks in the database and use the reference info as well as user query as input to LLM to generate summary.
    """

    def __init__(self, source, destination, embeddings):
        super().__init__(source, destination, embeddings)

    def create_db(self):
        """Method generates the RAG for CODE

        Returns:
            Croma: return a chroma db
        """
        if not os.path.isdir(self.destination):

            documents = list()
            for i in os.listdir(self.source):
                filepath = self.source + "/" + i
                loader = PyPDFLoader(filepath)
                doc = loader.load()
                documents.extend(doc)

            text_splitter = CharacterTextSplitter(
                separator="\n",
                chunk_size=self.max_chunk_size,
                chunk_overlap=self.chunk_overlap,
                length_function=len,
            )
            splitted_doc = text_splitter.split_documents(documents)
            while True:
                if len(splitted_doc) == 0:
                    break
                db = Chroma.from_documents(
                    splitted_doc[:150],
                    self.embeddings,
                    persist_directory=self.destination,
                )
                splitted_doc = splitted_doc[150:]
        else:
            db = Chroma(
                embedding_function=self.embeddings, persist_directory=self.destination
            )

        return db
