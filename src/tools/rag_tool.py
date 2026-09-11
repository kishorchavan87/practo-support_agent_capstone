from src.rag.retrieval import retrieve_grounded
from src.rag.grounded_generation import mock_answer

def rag_lookup(query: str) -> dict:
    rows, grounded = retrieve_grounded(query)
    return {
        "grounded": grounded,
        "answer": mock_answer(query, rows) if grounded else "I don't know based on the available knowledge base.",
        "sources": list(dict.fromkeys(r["document_id"] for r in rows)),
        "similarities": [round(r["similarity"],4) for r in rows],
    }
