from pathlib import Path
import chromadb
from .chunking import fixed_chunks, sentence_chunks
from .embeddings import embed
from src.config import KB_DIR, CHROMA_DIR

def load_docs():
    docs=[]
    for p in sorted(KB_DIR.glob("*.md")):
        if p.name == "README.md": continue
        docs.append((p.stem, p.read_text(encoding="utf-8")))
    return docs

def build():
    client=chromadb.PersistentClient(path=str(CHROMA_DIR))
    result={}
    for cname, chunker in [("fixed_overlap", fixed_chunks),("sentence_based",sentence_chunks)]:
        try: client.delete_collection(cname)
        except Exception: pass
        col=client.get_or_create_collection(cname, metadata={"hnsw:space":"cosine"})
        ids=[]; texts=[]; metas=[]
        for doc_id,text in load_docs():
            for i,ch in enumerate(chunker(text)):
                ids.append(f"{doc_id}-{i}")
                texts.append(ch)
                metas.append({"document_id":doc_id})
        col.upsert(ids=ids, documents=texts, metadatas=metas, embeddings=embed(texts))
        result[cname]=col.count()
    return result

def get_collection(name="sentence_based"):
    client=chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name, metadata={"hnsw:space":"cosine"})

def retrieve(query, k=3, collection="sentence_based"):
    col=get_collection(collection)
    emb=embed([query])[0]
    res=col.query(query_embeddings=[emb], n_results=k, include=["documents","metadatas","distances"])
    rows=[]
    for i,doc in enumerate(res["documents"][0]):
        # Chroma cosine distance -> similarity
        sim=1-float(res["distances"][0][i])
        rows.append({"text":doc,"document_id":res["metadatas"][0][i]["document_id"],"similarity":sim})
    return rows
