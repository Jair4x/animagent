from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from agent.state import AgentState
import re

CATEGORIES = ["horarios", "convivencia", "aranceles", "faq", "general"]

ROUTER_PROMPT = ChatPromptTemplate.from_template(
    """
    Eres el router de un agente institucional de ÁNIMA Formación Dual.
    Tu única tarea es clasificar la pregunta del usuario en una de estas categorías:

    - horarios: preguntas sobre días, horarios, materias, profesores o grupos
    - convivencia: preguntas sobre normas, sanciones, asistencia, vestimenta o comportamiento
    - aranceles: preguntas sobre pagos, cuotas, becas o costos del programa
    - faq: preguntas generales sobre la institución, programas, inscripción o formación dual
    - general: cualquier pregunta que no encaje en las anteriores

    Responde ÚNICAMENTE con una de estas palabras, sin explicación ni puntuación:
    horarios | convivencia | aranceles | faq | general

    Pregunta: {query}
""")

def route(state: AgentState, llm: BaseChatModel) -> AgentState:
    """
    Analyzes the user's query and determines the most adequate document category
    to answer it. Updates the 'category' field of the state

    ### Parameters
    `state` - AgentState instance
    
    `llm` - Router LLM.
    """
    chain       = ROUTER_PROMPT | llm
    result      = chain.invoke({"query": state["query"]})
    content     = result.content

    # Gemini's model responds with a list, so we get the content directly
    if isinstance(content, list):
        content = result.text
    else:
        # Groq's model has extended thinking, so they add it between <think> tags. We get rid of them for the response.
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)
    
    content     = content.strip().lower()
    content     = content.split()[0] # Just in case they add something else. Take the first word.

    category    = content if content in CATEGORIES else "general" # For if the LLM allucinates. Fallback to "general"
    
    print(f"[Router] '{state['query'][:60]}' -> Category: {category}")

    return {**state, "category": category}