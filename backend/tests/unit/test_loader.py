import pytest
from langchain_core.documents import Document
from rag.loader import load_pdfs, load_csvs, load_all_documents
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

def test_load_csvs_returns_list():
    result = load_csvs(config.DOCUMENTS_PATH)
    assert isinstance(result, list)

def test_load_csvs_returns_documents():
    result = load_csvs(config.DOCUMENTS_PATH)
    assert all(isinstance(doc, Document) for doc in result)

def test_load_csvs_have_source_metadata():
    result = load_csvs(config.DOCUMENTS_PATH)
    for doc in result:
        assert "source" in doc.metadata
        assert doc.metadata["source"].endswith(".csv")

def test_load_csvs_content_is_not_empty():
    result = load_csvs(config.DOCUMENTS_PATH)
    for doc in result:
        assert len(doc.page_content.strip()) > 0

def test_load_all_documents_combines_both():
    pdfs = load_pdfs(config.DOCUMENTS_PATH)
    csvs = load_csvs(config.DOCUMENTS_PATH)
    all_docs = load_all_documents()
    assert len(all_docs) == len(pdfs) + len(csvs)