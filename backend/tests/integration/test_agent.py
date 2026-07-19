import pytest
from agent.graph import build_graph
from rag.loader import load_all_documents
from rag.embeddings import load_or_build_index
from models.factory import get_llm

@pytest.fixture(scope="module")
def agent():
    llm   = get_llm()
    index = load_or_build_index(load_all_documents())
    return build_graph(llm, index)

def invoke(agent, query: str) -> str:
    result   = agent.invoke({"messages": [{"role": "user", "content": query}]})
    response = result["messages"][-1].content
    if isinstance(response, list):
        response = " ".join(
            block.get("text", "") if isinstance(block, dict) else str(block)
            for block in response
        )
    return response

def test_agent_returns_response(agent):
    response = invoke(agent, "¿Qué es ÁNIMA?")
    assert isinstance(response, str)
    assert len(response) > 0

def test_agent_faq_query(agent):
    response = invoke(agent, "¿Qué programas ofrece la institución?")
    assert "FINEST" in response or "Bachillerato" in response

def test_agent_convivencia_query(agent):
    response = invoke(agent, "¿Qué pasa si falto más del 25% de las clases?")
    assert len(response) > 0

def test_agent_aranceles_query(agent):
    response = invoke(agent, "¿Cuánto cuesta el FINEST?")
    assert "248" in response or "pesos" in response.lower() or "costo" in response.lower()

def test_agent_timetable_query(agent):
    response = invoke(agent, "¿Qué días tiene Back-end el grupo A del FINEST?")
    assert any(day in response.lower() for day in ["lunes", "martes", "miércoles", "jueves", "viernes"])

def test_agent_greeting(agent):
    response = invoke(agent, "Hola")
    assert len(response) > 0
    assert "248" not in response

def test_agent_off_topic(agent):
    response = invoke(agent, "¿Cuál es la capital de Francia?")
    response_lower = response.lower()
    assert any(phrase in response_lower for phrase in [
        "no puedo", "no está", "no tengo", "no dispongo",
        "no se menciona", "fuera de", "no relacionad"
    ])

def test_agent_with_gemini(agent):
    import os
    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        pytest.skip("GEMINI_API_KEY no configurada")

    from rag.embeddings import load_or_build_index
    llm_gemini   = get_llm(provider="gemini", gemini_key=gemini_key)
    index        = load_or_build_index(load_all_documents())
    agent_gemini = build_graph(llm_gemini, index)

    response = invoke(agent_gemini, "¿Qué es ÁNIMA?")
    assert isinstance(response, str)
    assert len(response) > 0