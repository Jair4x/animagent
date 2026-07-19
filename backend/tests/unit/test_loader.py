import pytest
from langchain_core.documents import Document
from rag.loader import load_pdfs, load_all_documents
import config

def test_load_pdfs_returns_list():
    result = load_pdfs(config.DOCUMENTS_PATH)
    assert isinstance(result, list)

def test_load_pdfs_returns_documents():
    result = load_pdfs(config.DOCUMENTS_PATH)
    assert all(isinstance(doc, Document) for doc in result)

def test_load_pdfs_have_source_metadata():
    result = load_pdfs(config.DOCUMENTS_PATH)
    for doc in result:
        assert "source" in doc.metadata
        assert doc.metadata["source"].endswith(".pdf")

def test_load_pdfs_have_category_metadata():
    result = load_pdfs(config.DOCUMENTS_PATH)
    for doc in result:
        assert "category" in doc.metadata
        assert len(doc.metadata["category"]) > 0