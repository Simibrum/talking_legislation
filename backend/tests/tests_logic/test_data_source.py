import pytest
from backend.common_logic.data_source import DataSource

def test_data_source_init():
    ds = DataSource('some_path')
    assert ds.logger is not None
    assert ds.url == 'some_path'
    assert ds.data is None
    assert ds.vectorstore is None
    assert ds.qa_chain is None
    assert ds.embedder is None
    assert ds.llm is not None
    assert ds.core_embedding_model is not None
    assert ds.store is not None