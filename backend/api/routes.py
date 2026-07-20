from fastapi import APIRouter, Header
from pydantic import BaseModel
from agent.graph import build_graph
from models.factory import get_llm
import index_store

router = APIRouter()

class ChatRequest(BaseModel):
    query:      str
    provider:   str | None = None
    history:    list[dict] = []

class ChatResponse(BaseModel):
    response:   str
    source:     str | None = None


@router.post("/chat", response_model=ChatResponse)
async def chat(
    body:           ChatRequest,
    x_gemini_key:   str | None = Header(default=None)
):
    """
    Main endpoint of the agent.

    ### Args
    #### `body`
    The user query and LLM provider.
    #### `x_gemini_key`
    Google Gemini API key sent via HTTP header.
    ### Returns
    Agent response and source document.
    """
    llm         = get_llm(provider=body.provider, gemini_key=x_gemini_key)
    agent       = build_graph(llm, index_store.index)

    if body.history:
        messages = body.history + [{"role": "user", "content": body.query}]
    else:
        messages = [{"role": "user", "content": body.query}]

    result      = agent.invoke({"messages": messages})
    messages    = result["messages"]

    source      = None

    for msg in reversed(messages):
        if hasattr(msg, "name") and hasattr(msg, "content"):
            if "__source__:" in (msg.content or ""):
                source = msg.content.split("__source__:")[-1].strip().split("\n")[0]
                break

    response    = messages[-1].content

    if isinstance(response, list):
        response = messages[-1].text

    return ChatResponse(response=response, source=source)