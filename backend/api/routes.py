from fastapi import APIRouter, Header
from pydantic import BaseModel
from agent.graph import build_graph
from models.factory import get_llm
from rag.embeddings import load_or_build_index
from rag.loader import load_all_documents

router = APIRouter()

class ChatRequest(BaseModel):
    query:      str
    provider:   str | None

class ChatResponse(BaseModel):
    response: str
    category: str | None


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
    )
    ```
    """
    llm     = get_llm(provider=body.provider, gemini_key=x_gemini_key)
    index   = load_or_build_index(load_all_documents())
    agent   = build_graph(llm, index)

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
    )