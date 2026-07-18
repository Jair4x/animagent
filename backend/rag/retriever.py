from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def retrieve(
        index: FAISS,
        query: str,
        category: str | None = None,
        k: int = 4
) -> list[Document]:
    """
    Searches the most relevant K chunks in the FAISS index for the given query.
    If a category is given, it only filters inside that document collection.

    ### Args
    #### `index`
    FAISS file
    #### `query`
    Search query
    #### `category`
    Document collection to search in (optional)
    #### `k`
    Number of most relevant chunks to show (default: 4)
    """
    filter_category = {"category": category} if category else None
    
    if category:
        results = index.similarity_search(
            query,
            k=k,
            filter=filter_category
        )
    else:
        results = index.similarity_search(query, k=k)

    if len(query) > 60:
        print(f"[Retriever] '{query[:60]}...' -> {len(results)} chunks recovered")
    else:
        print(f"[Retriever] '{query}' -> {len(results)} chunks recovered")

    return results

def format_context(documents: list[Document]) -> str:
    """
    Converts a recovered document list in a string with a legible format for the LLM,
    including the source and category of each fragment.

    ### Args
    #### `documents`
    List of documents to convert
    """
    fragments = []

    for i, doc in enumerate(documents, start=1):
        source      = doc.metadata.get("source", "desconocido")
        category    = doc.metadata.get("category", "")
        header      = f"[Fragmento {i} - {source} ({category})]"
        fragments.append(f"{header}\n{doc.page_content}")

    return "\n\n".join(fragments)