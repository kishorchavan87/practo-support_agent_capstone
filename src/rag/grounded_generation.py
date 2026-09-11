def mock_answer(query, rows):
    if not rows:
        return "I don't know based on the available Practo policy knowledge base."
    context=" ".join(r["text"] for r in rows)
    q=query.lower()
    # Deterministic extractive MOCK_LLM: answer only from retrieved policy text.
    sentences=[s.strip() for s in context.split(".") if s.strip()]
    relevant=[s for s in sentences if any(w in s.lower() for w in q.split() if len(w)>4)]
    selected=relevant[:2] or sentences[:2]
    return ". ".join(selected) + ("." if selected else "")
