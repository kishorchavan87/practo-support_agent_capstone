MAX_INPUT_CHARS=4000
LOOKUP_ALLOWED_AGENT="Lookup Agent"

def enforce_budget(text):
    if len(text)>MAX_INPUT_CHARS:
        raise ValueError(f"request exceeds runtime budget: {len(text)} > {MAX_INPUT_CHARS}")

def can_call_lookup(agent_role):
    return agent_role == LOOKUP_ALLOWED_AGENT

RISK_LEVEL="High"
RISK_REASON="This is a healthcare support system handling patient-support and appointment information; it is not permitted to diagnose or make treatment decisions."
