import pytest
from agent.graph import build_graph
from rag.loader import load_all_documents
from rag.embeddings import load_or_build_index
from models.factory import get_llm
from agent.router import CATEGORIES

@pytest.fixture(scope="module")
def agent():
    llm   = get_llm()
    index = load_or_build_index(load_all_documents())
    return build_graph(llm, index)

def invoke(agent, query: str) -> dict:
    return agent.invoke({
        "query":    query,
        "category": None,
        "context":  None,
        "response": None,
        "messages": [],
    })

def test_agent_returns_response(agent):
    result = invoke(agent, "¿Qué es ÁNIMA?")
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0

def test_agent_returns_category(agent):
    result = invoke(agent, "¿Cuáles son los horarios del grupo A del FINEST?")
    assert result["category"] in ["horarios", "faq", "general"]

def test_agent_horarios_query(agent):
    result = invoke(agent, "¿Qué materia tiene el grupo A del FINEST el lunes a las 18:00?")
    assert result["category"] == "horarios"
    assert len(result["response"]) > 0

def test_agent_convivencia_query(agent):
    result = invoke(agent, "¿Qué pasa si falto más del 25% de las clases?")
    assert result["category"] == "convivencia"
    assert len(result["response"]) > 0

def test_agent_aranceles_query(agent):
    result = invoke(agent, "¿Cuánto cuesta el FINEST y cómo se paga?")
    assert result["category"] == "aranceles"
    assert len(result["response"]) > 0

def test_agent_does_not_hallucinate(agent):
    result = invoke(agent, "¿Cuál es el número de teléfono de ÁNIMA?")
    response = result["response"].lower()
    assert any(phrase in response for phrase in [
        "no tengo", "no encuentro", "no está", "no dispongo",
        "no se menciona", "no figura", "consultar"
    ])

def test_agent_with_gemini(agent):
    import os
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        pytest.skip("GEMINI_API_KEY no configurada, saltando test de Gemini")

    llm_gemini   = get_llm(provider="gemini", gemini_key=gemini_key)
    index        = load_or_build_index(load_all_documents())
    agent_gemini = build_graph(llm_gemini, index)

    result = invoke(agent_gemini, "¿Qué es ÁNIMA?")
    assert isinstance(result["response"], str)
    assert len(result["response"]) > 0
    assert result["category"] in CATEGORIES