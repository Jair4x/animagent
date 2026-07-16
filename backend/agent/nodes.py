from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from agent.state import AgentState
from rag.retriever import retrieve, format_context

SYNTH_PROMPT = ChatPromptTemplate.from_template(
    """
    Eres ÁnimAgent, el asistente institucional de ÁNIMA Formación Dual.
    Respondes preguntas de estudiantes e interesados basándote exclusivamente en
    la documentación oficial de la institución.

    Reglas:
    - Responde siempre en español.
    - Sé claro, directo y amable.
    - Si la información no está en el contexto, dilo honestamente. No inventes datos.
    - Al final de tu respuesta, indica de qué documento(s) proviene la información.

    Contexto recuperado:
    {context}

    Pregunta del usuario:
    {query}

    Respuesta:
""")

def retriever_node(state: AgentState, index: FAISS) -> AgentState:
    """
    Recovers the most relevant document fragments for the query, 
    filtering by the category set by the router.
    
    Updates the `context` field of the AgentState with the formatted fragments.

    ### Parameters
    `state` - AgentState

    `index` - FAISS index
    """
    category    = state.get("category")
    query       = state["query"]

    filter_category = None if category == "general" else category

    documents   = retrieve(index, query, category=filter_category)
    context     = format_context(documents)

    return {**state, "context": context}

def synthesizer_node(state: AgentState, llm: BaseChatModel) -> AgentState:
    """
    Generates the final response using the LLM, the recovered context and the original query.

    Updates the `response` field of the AgentState instance.

    ### Parameters
    `state` - AgentState instance

    `llm` - Synthesizer LLM.
    """
    chain   = SYNTH_PROMPT | llm
    result  = chain.invoke({
        "context":  state["context"],
        "query":    state["query"],
    })

    return {**state, "response": result.content}
