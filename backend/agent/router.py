from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from agent.state import AgentState

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
    category    = result.content.strip().lower()

    # For if the LLM allucinates.
    if category not in CATEGORIES:
        category = "general"
    
    print(f"[Router] '{state['query'][:60]}' -> Category: {category}")

    return {**state, "category": category}