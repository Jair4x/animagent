from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router
from rag.loader import load_all_documents
from rag.embeddings import load_or_build_index
import config

index = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Loads the FAISS index a single time when initializing the server 
    and stores it in memory to reuse it in every request.
    """
    global index
    print("[ÁnimAgent] Initializing server...")
    documents   = load_all_documents()
    index       = load_or_build_index(documents)
    print("[ÁnimAgent] Index done. Server online.")
    yield
    print("[ÁnimAgent] Shutting down...")

app = FastAPI(
    title="ÁnimAgent API",
    description="Agente de reconocimiento institucional de ÁNIMA Formación Dual",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.FRONTEND_URL],
    allow_methods=["POST"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=config.HOST, port=config.PORT, reload=True)