from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import TextSplitter
from langchain_core.documents import Document
from pathlib import Path
import config

# Model name defined .env file.
# Default: "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
def get_embeddings_model() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=config.EMBEDDINGS_MODEL)

# Split the documents in chunks, size and overlap defined on .env file.
# Default: CHUNK_SIZE = 500, CHUNK_OVERLAP = 50
def split_documents(documents: list[Document]) -> list[Document]:
    splitter = TextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"[Embeddings] {len(documents)} documents -> {len(chunks)} chunks")
    return chunks

# Build FAISS index
# FAISS index path is defined on .env file
# Default: ./faiss_index
def build_index(documents: list[Document]) -> FAISS:
    chunks      = split_documents(documents)
    embeddings  = get_embeddings_model()
    index       = FAISS.from_documents(chunks, embeddings)

    config.FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)
    index.save_local(str(config.FAISS_INDEX_PATH))
    print(f"[Embeddings] Index saved on {config.FAISS_INDEX_PATH}")

    return index

def load_index() -> FAISS:
    embeddings  = get_embeddings_model()
    index       = FAISS.load_local(
        str(config.FAISS_INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    print(f"[Embeddings] Index loaded from {config.FAISS_INDEX_PATH}")
    return index

def get_or_build_index(documents: list[Document]) -> FAISS:
    index_file = config.FAISS_INDEX_PATH / "index.faiss"

    if index_file.exists():
        return load_index()
    
    return build_index(documents)