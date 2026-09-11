from sentence_transformers import SentenceTransformer

_MODEL = None
def model():
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer("all-MiniLM-L6-v2")
    return _MODEL

def embed(texts):
    return model().encode(texts, normalize_embeddings=True).tolist()
