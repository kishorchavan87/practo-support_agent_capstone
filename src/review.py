from src.models import VerdictModel

def review(draft, context):
    ctx=" ".join(context).lower()
    supported=all(word.lower() in ctx for word in draft.split() if len(word)>8)
    if supported:
        return VerdictModel(approved=True,final_answer=draft,reason="Draft is supported by supplied context.")
    # Deterministic editor removes unsupported long claims.
    safe=" ".join([s.strip() for s in draft.split(".") if any(w.lower() in ctx for w in s.split() if len(w)>6)])
    return VerdictModel(approved=False,final_answer=safe or "I don't know based on the available context.",reason="Removed unsupported claim(s).")
