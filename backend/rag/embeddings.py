from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pathlib import Path
import config

def get_embeddings_model() -> HuggingFaceEmbeddings:
    """
    Get the Hugging Face model by its name.

    ### .env values
    `EMBEDDINGS_MODEL` (Default: `"sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"`)
    """
    return HuggingFaceEmbeddings(model_name=config.EMBEDDINGS_MODEL)

def split_documents(documents: list[Document]) -> list[Document]:
    """
    Split the documents in chunks for the LLM to digest.

    ### Parameters
    `documents` - List of documents to split
    
    ### .env values
    `CHUNK_SIZE` (default: 500)

    `CHUNK_OVERLAP` (default: 50)
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=config.CHUNK_SIZE,
        chunk_overlap=config.CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(documents)
    print(f"[Embeddings] {len(documents)} documents -> {len(chunks)} chunks")
    return chunks

def build_index(documents: list[Document]) -> FAISS:
    """
    Build and save the FAISS index

    ### .env values
    `FAISS_INDEX_PATH` (default: `./faiss_index`)
    """
    chunks      = split_documents(documents)
    embeddings  = get_embeddings_model()
    index       = FAISS.from_documents(chunks, embeddings)

    config.FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)
    index.save_local(str(config.FAISS_INDEX_PATH))
    print(f"[Embeddings] Index saved on {config.FAISS_INDEX_PATH}")

    return index

def load_index() -> FAISS:
    """
    Try to load the FAISS index

    ### .env values
    `FAISS_INDEX_PATH` (default: ./faiss_index)
    """
    embeddings  = get_embeddings_model()
    index       = FAISS.load_local(
        str(config.FAISS_INDEX_PATH),
        embeddings,
        allow_dangerous_deserialization=True
    )

    print(f"[Embeddings] Index loaded from {config.FAISS_INDEX_PATH}")
    return index

def load_or_build_index(documents: list[Document]) -> FAISS:
    """
    Tries to load the FAISS index file.

    If it doesn't exist or loading fails, it builds the file instead.

    ### Parameters
    `documents` - List of documents needed to build the FAISS index
    """
    try: 
        return load_index()
    except: 
        return build_index(documents)