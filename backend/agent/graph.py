from functools import partial
from langgraph.graph import StateGraph, END
from langchain_core.language_models import BaseChatModel
from langchain_community.vectorstores import FAISS
from agent.state import AgentState
from agent.router import route
from agent.nodes import retriever_node, synthesizer_node
from agent.csv_node import csv_retriever_node

def _route_retriever(state: AgentState) -> str:
    """
    Decides which retrieving node to use according to the category set by the router agent.
    """
    return "csv_retriever" if state["category"] == "horarios" else "retriever"

def build_graph(llm: BaseChatModel, router_llm: BaseChatModel, index: FAISS) -> StateGraph:
    """
    Builds and compiles ÁnimAgent's graph.

    ### Parameters
    
    #### `llm`
    Instanciated language model
    
    #### `index`
    Loaded FAISS index
    
    ### Returns
    `CompiledStateGraph` object
    """
    graph = StateGraph(AgentState)

    graph.add_node("router",        partial(route,              llm=router_llm))
    graph.add_node("retriever",     partial(retriever_node,     index=index))
    graph.add_node("csv_retriever", partial(csv_retriever_node, llm=llm))
    graph.add_node("synthesizer",   partial(synthesizer_node,   llm=llm))

    graph.set_entry_point("router")

    graph.add_conditional_edges("router", _route_retriever, {
        "retriever":        "retriever",
        "csv_retriever":    "csv_retriever"
    })

    graph.add_edge("retriever",         "synthesizer")
    graph.add_edge("csv_retriever",     "synthesizer")
    graph.add_edge("synthesizer",       END)

    return graph.compile()