from functools import partial
from langgraph.graph import StateGraph, END
from langchain_core.language_models import BaseChatModel
from langchain_community.vectorstores import FAISS
from agent.state import AgentState
from agent.router import route
from agent.nodes import retriever_node, synthesizer_node

def build_graph(llm: BaseChatModel, router_llm: BaseChatModel, index: FAISS) -> StateGraph:
    """
    Builds and compiles ÁnimAgent's graph.

    ### Parameters
    `llm` - Instanciated language model
    `index` - FAISS index
    """
    graph = StateGraph(AgentState)

    graph.add_node("router",        partial(route,              llm=router_llm))
    graph.add_node("retriever",     partial(retriever_node,     index=index))
    graph.add_node("synthesizer",   partial(synthesizer_node,   llm=llm))

    graph.set_entry_point("router")

    graph.add_edge("router",        "retriever")
    graph.add_edge("retriever",     "synthesizer")
    graph.add_edge("synthesizer",   END)

    return graph.compile()