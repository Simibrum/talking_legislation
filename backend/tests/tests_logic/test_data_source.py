import pytest
from langchain.schema.document import Document
from common_logic.data_source import DataSource, LegislationDataSource
from common_logic.XMLparser import UKLegislationParser
from tests.tests_logic import CURRENT_DIR

def test_data_source_init():
    ds = DataSource()
    assert ds.logger is not None
    assert ds.data is None
    assert ds.vectorstore is None
    assert ds.qa_chain is None
    assert ds.embedder is None
    assert ds.llm is not None
    assert ds.core_embedding_model is not None
    assert ds.store is not None

def test_legislation_data_source_init():
    ds = LegislationDataSource("https://www.legislation.gov.uk/ukpga/2010/15/contents")
    assert ds.logger is not None
    assert ds.data is None
    assert ds.vectorstore is None
    assert ds.qa_chain is None
    assert ds.embedder is None
    assert ds.llm is not None
    assert ds.core_embedding_model is not None
    assert ds.store is not None
    assert ds.url == "https://www.legislation.gov.uk/ukpga/2010/15/contents"
    assert ds.parser is None
    # Load test data
    ds.parser = UKLegislationParser.load(CURRENT_DIR / "test_parser.pkl")
    documents = [
                Document(
                    page_content=x['flattened_text'],
                    metadata={
                        "title": x['title'],
                        "section": x['number'],
                        "source": x['DocumentURI']
                    }
                ) for x in ds.parser.get_section_dicts()
    ]
    assert len(documents) == 166
    assert documents[0].metadata["title"] == "Patentable inventions."
    assert documents[0].metadata["section"] == "1"
    assert documents[0].page_content is not None
    assert documents[0].page_content.startswith("1. Patentable inventions.\n\n    1) A patent may be granted only")