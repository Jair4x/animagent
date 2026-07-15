from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document
from pathlib import Path
import pandas as pd
import config

# Load PDFs and convert each page in a Document.
def load_pdfs(directory: Path) -> list[Document]:
    documents = []

    for pdf_path in directory.rglob("*.pdf"):
        loader  = PyPDFLoader(str(pdf_path))
        pages   = loader.load()

        for page in pages:
            page.metadata["source"]     = pdf_path.name
            page.metadata["category"]   = pdf_path.parent.name # Since documents are in category sub-folders
        
        documents.extend(pages)

    return documents

# Load CSVs and convert each row in a Document.
def load_csvs(directory: Path) -> list[Document]:
    documents = []

    for csv_path in directory.rglob("*.csv"):
        df = pd.read_csv(csv_path)

        for _, row in df.iterrows():
            content = "\n".join(
                f"{col}: {val}" 
                for col, val in row.items()
                if pd.notna(val) # Filters empty cells to prevent adding innecesary noice
            )

            doc = Document(
                page_content=content,
                metadata={
                    "source": csv_path.name,
                    "category": csv_path.parent.name
                }
            )
            documents.append(doc)

    return documents

# Load every single document
def load_all_documents() -> list[Document]:
    base = config.DOCUMENTS_PATH

    pdfs = load_pdfs(base)
    csvs = load_csvs(base)

    all_docs = pdfs + csvs

    print(f"[Loader] Loaded {len(pdfs)} PDF pages")
    print(f"[Loader] Loaded {len(csvs)} CSV rows")
    print(f"[Loader] Total documents loaded: {len(all_docs)}")

    return all_docs
