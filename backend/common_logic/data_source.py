import logging
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.document_loaders import JSONLoader
from langchain.embeddings import CacheBackedEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.llms.openai import OpenAIChat
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler

from backend.config import logger

class DataSource:
    def __init__(self, url: str):
        self.logger = logger
        self.logger.info("Initializing data source")

        self.url = url
        self.data = None

        # Initialize common functionalities
        self.store = LocalFileStore("../embeddings_cache/")
        # Use the OpenAIEmbeddings model - means it's easier to host remotely as we don't need a GPU
        self.core_embedding_model = OpenAIEmbeddings()
        self.llm = OpenAIChat()

        # Initialize these after data is loaded
        self.embedder = None
        self.vectorstore = None
        self.qa_chain = None

    def load_data(self):
        raise NotImplementedError("This method should be overridden by subclass")

    def post_data_load_setup(self):
        self.logger.info("Creating cache backed embeddings")
        self.embedder = CacheBackedEmbeddings.from_bytes_store(
            self.core_embedding_model,
            self.store,
            namespace=self.core_embedding_model.model_name
        )
        self.logger.info("Storing embeddings in vector store")
        self.vectorstore = FAISS.from_documents(self.data, self.embedder)
        self.logger.info("Initializing the QA chain")
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.vectorstore.as_retriever(),
            callbacks=[StdOutCallbackHandler()],
            return_source_documents=True
        )

    def get_answers_and_documents(self, query):
        self.logger.info("Getting answers and documents")
        return self.qa_chain({"query": query})