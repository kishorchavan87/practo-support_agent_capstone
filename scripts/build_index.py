from src.dataset import save
from src.rag.vector_store import build
save()
print("index:", build())
