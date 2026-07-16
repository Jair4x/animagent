from langgraph.graph import MessagesState

class AgentState(MessagesState):
    """
    State that travels throughout the agent graph.

    Extends `MessagesState` to include the message history along
    other metadata from the agent.

    ### Parameters

    `query` - User's query in plain text

    `category` - Query category, defined by the router

    `context` - Fragments recovered by the retriever, already formatted as string
    
    `response` - LLM's response
    """
    query:      str
    category:   str | None
    context:    str | None
    response:   str | None
    source:     str | None