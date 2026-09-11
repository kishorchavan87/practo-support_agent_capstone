import re

PHONE=re.compile(r"(?<!\d)(?:\+91[- ]?)?[6-9]\d{9}(?!\d)")
INJECTION_TERMS=("ignore previous instructions","ignore all instructions","system prompt","jailbreak","developer message")

def mask_pii(text):
    return PHONE.sub(lambda m: m.group(0)[:2] + "******" + m.group(0)[-2:], text)

def detect_injection(text):
    low=text.lower()
    return any(term in low for term in INJECTION_TERMS)

def input_guard(text):
    masked=mask_pii(text)
    return {"text":masked,"pii_masked":masked!=text,"injection":detect_injection(text)}

def output_grounded(answer, retrieved):
    if not retrieved: return False
    context=" ".join(x["text"] for x in retrieved).lower()
    # Conservative lexical support check for MOCK_LLM.
    significant=[w for w in re.findall(r"[a-z]{5,}",answer.lower())]
    return sum(w in context for w in significant) >= max(1, len(significant)//3)
