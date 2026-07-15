from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

def retrieve(
        index: FAISS,
        query: str,
        category: str | None = None,
        k: int = 4
) -> list[Document]:
    
    if category:
        results = index.similarity_search(
            query,
            k=k,
            filter={"category": category}
        )
    else:
        results = index.similarity_search(query, k=k)

    if len(query) > 60:
        print(f"[Retriever] '{query[:60]}...' -> {len(results)} chunks recovered")
    else:
        print(f"[Retriever] '{query}' -> {len(results)} chunks recovered")

    return results

def format_context(documents: list[Document]) -> str:
    fragments = []

    for i, doc in enumerate(documents, start=1):
        source      = doc.metadata.get("source", "desconocido")
        category    = doc.metadata.get("category", "")
        header      = f"[Fragment {i} - {source} ({category})]"
        fragments.append(f"{header}\n{doc.page_content}")

    return "\n\n".join(fragments)