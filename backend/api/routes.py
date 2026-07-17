from fastapi import APIRouter, Header
from pydantic import BaseModel
from agent.graph import build_graph
from models.factory import get_llm, get_router_llm
import index_store

router = APIRouter()

class ChatRequest(BaseModel):
    query:      str
    provider:   str | None

class ChatResponse(BaseModel):
    response:   str
    category:   str | None
    source:     str | None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body:           ChatRequest,
    x_gemini_key:   str | None = Header(default=None)
):
    """
    Main endpoint of the agent.

    ### Parameters
    #### `body`
    The user query and LLM provider.

    Content/format:
    ```python
    query:      str
    provider:   str | None
    ```
    #### `x_gemini_key`
    Google Gemini API key, if set by the user, sent via HTTP header.
    
    ### Returns
    ```python
    class ChatResponse(
        response, # The agent's response
        category, # Category determined by the router (for v1.1)
        source, # Document consulted for the information
    )
    ```
    """
    llm         = get_llm(provider=body.provider, gemini_key=x_gemini_key)
    router_llm  = get_router_llm(provider=body.provider, gemini_key=x_gemini_key)
    agent       = build_graph(llm, router_llm, index_store.index)

    result = agent.invoke({
        "query":        body.query,
        "category":     None,
        "context":      None,
        "response":     None,
        "messages":     [],
    })

    return ChatResponse(
        response=result["response"],
        category=result["category"],
        source=result["source"]
    )