import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

class Rag:

    def __init__(self, source, destination,embeddings,max_chunk_size = 1000,chunk_overlap = 400):
        self.source =source
        self.destination =destination
        self.embeddings = embeddings
        self.max_chunk_size = max_chunk_size
        self.chunk_overlap = chunk_overlap

    
    def create_db(self):
        pass



class CoderRag(Rag):
    def __init__(self, source, destination,embeddings):
        super().__init__( source, destination,embeddings)

    def create_db(self):
        if not os.path.isdir(self.destination):
            splitted_doc = []
            text_splitter = CharacterTextSplitter()
            for i in os.listdir(self.source):
                filepath = self.source + "/" +  i
                loader = TextLoader(filepath)
                doc = loader.load()
            
                for d in doc:
                    question = []
                    for x in d.page_content.split():
                        if 'class' in x:
                            break
                        question.append(x)
                    res = ''.join(question)
                    d.metadata = {"code":d.page_content}
                    d.page_content = res

                splitted_doc.extend(text_splitter.split_documents(doc))

            while True:
                if len(splitted_doc) == 0:
                    break
                db = Chroma.from_documents(splitted_doc[:150], self.embeddings, persist_directory=self.destination)
                splitted_doc = splitted_doc[150:]
        else:
            db = Chroma(embedding_function=self.embeddings, persist_directory=self.destination)


        return db

class SummaryRag(Rag):
    def __init__(self,source, destination,embeddings):
        super().__init__(source, destination,embeddings)

    def create_db(self):
        if not os.path.isdir(self.destination):

            documents = list()
            for i in os.listdir(self.source):
                filepath = self.source + "/" +  i
                loader = PyPDFLoader(filepath)
                doc = loader.load()
                documents.extend(doc)

            text_splitter = CharacterTextSplitter(separator='\n',chunk_size=self.max_chunk_size, chunk_overlap=self.chunk_overlap,length_function=len)
            splitted_doc = text_splitter.split_documents(documents)
            while True:
                if len(splitted_doc) == 0:
                    break
                db = Chroma.from_documents(splitted_doc[:150], self.embeddings, persist_directory=self.destination)
                splitted_doc = splitted_doc[150:]
        else:
            db = Chroma(embedding_function=self.embeddings, persist_directory=self.destination)

        return db
