from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from agent.state import AgentState
from rag.retriever import retrieve, format_context
import re

SYNTH_PROMPT = ChatPromptTemplate.from_template(
    """
    Eres ÁnimAgent, el asistente institucional de ÁNIMA Formación Dual.
    Respondes preguntas de estudiantes e interesados basándote exclusivamente en
    la documentación oficial de la institución.

    Reglas:
    - Responde siempre en español.
    - Sé claro, directo y amable.
    - Si la información no está en el contexto, dilo honestamente. NO INVENTES DATOS.
    - Si el dato exacto NO APARECE textualmente en el contexto, responde únicamente: "Lo siento, no puedo ayudarte con eso." Esto incluye direcciones, teléfonos, nombres, fechas o cualquier dato específico que no figure en los fragmentos recuperados.

    Contexto recuperado:
    {context}

    Pregunta del usuario:
    {query}

    Respuesta:
""")

def retriever_node(state: AgentState, index: FAISS) -> AgentState:
    """
    Recovers the most relevant document fragments for the query, filtering by the category set by the router.

    ### Parameters
    #### `state`
    `AgentState` instance

    #### `index`
    FAISS index

    ### Returns
    Updated `AgentState` instance with `'context'` field containing the formatted fragments and `'source'` field with consulted document.
    """
    category    = state.get("category")
    query       = state["query"]

    filter_category = None if category == "general" else category

    documents   = retrieve(index, query, category=filter_category)
    context     = format_context(documents)
    source      = documents[0].metadata.get("source") if documents else None

    return {**state, "context": context, "source": source}

def synthesizer_node(state: AgentState, llm: BaseChatModel) -> AgentState:
    """
    Generates the final response using the LLM, the recovered context and the original query.

    ### Parameters
    
    #### `state`
    `AgentState` instance

    #### `llm`
    Synthesizer's LLM model

    ### Returns
    Updated `AgentState` instance with the `'response'` field containing the final response from the agent.
    """
    chain   = SYNTH_PROMPT | llm
    result  = chain.invoke({
        "context":  state["context"],
        "query":    state["query"],
    })

    content = result.content

    # Gemini's model responds with a list, so we get the content directly
    if isinstance(content, list):
        content = result.text
    else:
        # Groq's model has extended thinking, so they add it between <think> tags. We get rid of them for the response.
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL)

    content = content.strip() 

    return {**state, "response": content}
