import pytest
from rag.loader import load_all_documents
from rag.embeddings import load_or_build_index
from rag.retriever import retrieve, format_context

@pytest.fixture(scope="module")
def index():
    documents = load_all_documents()
    return load_or_build_index(documents)

def test_retrieve_returns_list(index):
    results = retrieve(index, "¿Cuáles son los horarios del FINEST?")
    assert isinstance(results, list)

def test_retrieve_returns_k_results(index):
    results = retrieve(index, "¿Cuáles son los horarios del FINEST?", k=4)
    assert len(results) <= 4

def test_retrieve_with_category_filter(index):
    results = retrieve(index, "horarios de Back-end", category="horarios")
    for doc in results:
        assert doc.metadata.get("category") == "horarios"

def test_retrieve_without_category_searches_all(index):
    results = retrieve(index, "beca", category=None)
    assert len(results) > 0

def test_format_context_returns_string(index):
    results = retrieve(index, "¿Cuánto cuesta el FINEST?")
    context = format_context(results)
    assert isinstance(context, str)
    assert len(context) > 0

def test_format_context_includes_source(index):
    results = retrieve(index, "¿Cuánto cuesta el FINEST?")
    context = format_context(results)
    assert "Fragmento" in context