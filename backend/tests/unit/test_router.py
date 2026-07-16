import pytest
from models.factory import get_llm
from agent.state import AgentState
from agent.router import route, CATEGORIES

@pytest.fixture(scope="module")
def llm():
    return get_llm()

def test_route_returns_valid_category(llm):
    state = AgentState(query="¿Cuáles son los horarios del lunes?", category=None, context=None, response=None, messages=[])
    result = route(state, llm)
    assert result["category"] in CATEGORIES

def test_route_horarios(llm):
    state = AgentState(query="¿Qué materia tengo el martes a las 19:30?", category=None, context=None, response=None, messages=[])
    result = route(state, llm)
    assert result["category"] == "horarios"

def test_route_convivencia(llm):
    state = AgentState(query="¿Cuántas faltas puedo tener antes de perder la materia?", category=None, context=None, response=None, messages=[])
    result = route(state, llm)
    assert result["category"] == "convivencia"

def test_route_aranceles(llm):
    state = AgentState(query="¿Cuánto cuesta el programa FINEST?", category=None, context=None, response=None, messages=[])
    result = route(state, llm)
    assert result["category"] == "aranceles"

def test_route_faq(llm):
    state = AgentState(query="¿Qué es la formación dual?", category=None, context=None, response=None, messages=[])
    result = route(state, llm)
    assert result["category"] == "faq"

def test_route_preserves_query(llm):
    query = "¿Qué diferencia hay entre FINEST y el Bachillerato?"
    state = AgentState(query=query, category=None, context=None, response=None, messages=[])
    result = route(state, llm)
    assert result["query"] == query