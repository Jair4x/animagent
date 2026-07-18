from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pathlib import Path
import config

def load_pdfs(directory: Path) -> list[Document]:
    """
    Loads the PDF files in the designated folder
    and converts each page into a LangChain Document

    ### Args
    #### `directory`
    Folder in which to search the PDF files
    """
    documents = []

    for pdf_path in directory.rglob("*.pdf"):
        loader  = PyPDFLoader(str(pdf_path))
        pages   = loader.load()

        for page in pages:
            page.metadata["source"]     = pdf_path.name
            page.metadata["category"]   = pdf_path.parent.name # Since documents are in category sub-folders
        
        documents.extend(pages)

    return documents

def load_all_documents() -> list[Document]:
    """
    Loads every PDF and CSV file

    ### .env values
    `DOCUMENTS_PATH` (default: ../documents)
    """
    base = config.DOCUMENTS_PATH
    docs = load_pdfs(base)
    print(f"[Loader] Loaded {len(docs)} PDF pages")
    return docs
