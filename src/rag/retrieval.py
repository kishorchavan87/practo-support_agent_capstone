from .vector_store import retrieve

# Run scripts/run_evaluation.py to empirically inspect these values for your environment.
DEFAULT_THRESHOLD = 0.35

def retrieve_grounded(query, collection="sentence_based", k=3, threshold=DEFAULT_THRESHOLD):
    rows=retrieve(query,k,collection)
    top=rows[0]["similarity"] if rows else -1
    return rows, top >= threshold
