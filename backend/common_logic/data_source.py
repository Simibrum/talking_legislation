import logging
import pickle
from langchain.embeddings import CacheBackedEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler
from langchain.schema.document import Document

from config import logger, DATA_DIR
from common_logic.XMLparser import UKLegislationParser
from common_logic.utils import url_to_filename

class DataSource:
    def __init__(self):
        self.logger = logger
        self.logger.info("Initializing data source")

        self.data = None
        self.logger.info("Creating local file store")
        # Initialize common functionalities
        embeddings_cache_dir = DATA_DIR / "embeddings_cache/"
        self.store = LocalFileStore(embeddings_cache_dir)
        self.logger.info("Initialising OpenAI Embeddings and Chat")
        # Use the OpenAIEmbeddings model - means it's easier to host remotely as we don't need a GPU
        self.core_embedding_model = OpenAIEmbeddings()
        self.llm = ChatOpenAI()

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
            namespace=self.core_embedding_model.model
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

class LegislationDataSource(DataSource):
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.parser = None

    def load_data(self, use_cache: bool = True):
        """Initialise loading of data."""
        self.logger.info(f"Loading legislation data from {self.url}")
        if use_cache:
            # Check if there is a file created from the url
            filename = url_to_filename(self.url) + ".pkl"
            full_path = DATA_DIR / filename
            try:
                self.logger.info(f"Attempting to load cached parser from {filename}")
                with open(full_path, "rb") as f:
                    self.parser = pickle.load(f)
                self.logger.info("Loaded cached parser")
            except FileNotFoundError:
                self.logger.info("Cached parser not found, parsing XML")
                use_cache = False
        if not use_cache:
            self.logger.info("Parsing XML from URL")
            self.parser = UKLegislationParser(self.url, parse_sections=True)
            self.logger.info("Saving parser to cache")
            self.parser.save()
        # Get documents from the parser
        self.data = [
            Document(
                page_content=x['flattened_text'],
                metadata={
                    "title": x['title'],
                    "section": x['number'],
                    "source": x['DocumentURI']
                }
            ) for x in self.parser.get_section_dicts()]
        self.post_data_load_setup()