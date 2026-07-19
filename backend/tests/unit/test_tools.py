import pytest
from rag.loader import load_all_documents
from rag.embeddings import load_or_build_index
from agent.tools import make_search_documents_tool, make_search_timetables_tool

@pytest.fixture(scope="module")
def index():
    return load_or_build_index(load_all_documents())

@pytest.fixture(scope="module")
def search_documents(index):
    return make_search_documents_tool(index)

@pytest.fixture(scope="module")
def search_timetables():
    return make_search_timetables_tool()


# --- search_documents ---

def test_search_documents_returns_string(search_documents):
    result = search_documents.invoke({"query": "¿Qué programs ofrece ÁNIMA?"})
    assert isinstance(result, str)
    assert len(result) > 0

def test_search_documents_includes_source(search_documents):
    result = search_documents.invoke({"query": "¿Qué programs ofrece ÁNIMA?"})
    assert "__source__:" in result

def test_search_documents_with_category(search_documents):
    result = search_documents.invoke({"query": "faltas y asistencia", "category": "convivencia"})
    assert len(result) > 0

def test_search_documents_irrelevant_query(search_documents):
    result = search_documents.invoke({"query": "receta de pizza napolitana"})
    assert isinstance(result, str)


# --- search_timetables ---

def test_search_timetables_returns_string(search_timetables):
    result = search_timetables.invoke({"program": "FINEST", "group": "A"})
    assert isinstance(result, str)
    assert len(result) > 0

def test_search_timetables_includes_source(search_timetables):
    result = search_timetables.invoke({"program": "FINEST", "group": "A"})
    assert "__source__:" in result

def test_search_timetables_filters_by_subject(search_timetables):
    result = search_timetables.invoke({"program": "FINEST", "group": "A", "subject": "Back-end"})
    assert "Back-end" in result or "backend" in result.lower()

def test_search_timetables_no_results(search_timetables):
    result = search_timetables.invoke({"program": "FINEST", "group": "A", "subject": "Física Cuántica"})
    assert "No se encontraron" in result

def test_search_timetables_bachillerato(search_timetables):
    result = search_timetables.invoke({"program": "Bachillerato", "group": "A"})
    assert isinstance(result, str)
    assert len(result) > 0