from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

# ------
# Server
# ------
HOST: str           = os.getenv("HOST", "localhost")
PORT: int           = int(os.getenv("PORT", 8000))
FRONTEND_URL: str   = os.getenv("FRONTEND_URL", "http://localhost:4321")

# ------
# LLM Config
# ------
DEFAULT_PROVIDER: str       = os.getenv("DEFAULT_PROVIDER", "groq")

GROQ_API_KEY: str           = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL_NAME: str        = os.getenv("GROQ_MODEL_NAME", "llama-3.1-8b-instant")

GEMINI_API_KEY: str         = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL_NAME: str      = os.getenv("GEMINI_MODEL_NAME", "gemini-3.5-flash")

# ------
# RAG
# ------
DOCUMENTS_PATH: Path    = Path(os.getenv("DOCUMENTS_PATH", "../documents")).resolve()
FAISS_INDEX_PATH: Path  = Path(os.getenv("FAISS_INDEX_PATH", "./faiss_index")).resolve()
EMBEDDINGS_MODEL: str   = os.getenv("EMBEDDINGS_MODEL", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
CHUNK_SIZE: int         = int(os.getenv("CHUNK_SIZE", 300))
CHUNK_OVERLAP: int      = int(os.getenv("CHUNK_OVERLAP", 50))

# ------
# Validations
# ------
if DEFAULT_PROVIDER not in ("groq", "gemini"):
    raise ValueError(f"DEFAULT_PROVIDER must be 'groq' or 'gemini', received: {DEFAULT_PROVIDER}")

if DEFAULT_PROVIDER == "groq" and not GROQ_API_KEY:
    raise ValueError("DEFAULT_PROVIDER is groq but GROQ_API_KEY is undefined")

if DEFAULT_PROVIDER == "gemini" and not GEMINI_API_KEY:
    raise ValueError("DEFAULT_PROVIDER is gemini but GEMINI_API_KEY is undefined")

if not DOCUMENTS_PATH.exists():
    raise FileNotFoundError(f"DOCUMENTS_PATH doens't exist, received: {DOCUMENTS_PATH}")