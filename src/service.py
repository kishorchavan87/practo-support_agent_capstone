import re
from src.guardrails import input_guard
from src.memory import add_turn
from src.models import AgentResponse
from src.tools.rag_tool import rag_lookup
from src.tools.appointment_tool import check_appointment_status
from src.rag.vector_store import retrieve
from functools import lru_cache

cache={}
tool_calls={"rag":0,"lookup":0}

def normalize(q): return re.sub(r"\s+"," ",q.strip().lower())

def answer(query, session_id="default"):
    g=input_guard(query)
    if g["injection"]:
        return AgentResponse(answer="I can't process that request because it contains an instruction-manipulation pattern.",grounded=False,refused=True,reason="prompt_injection")
    q=g["text"]
    key=normalize(q)
    if key in cache:
        result=cache[key].model_copy()
        result.reason="cache_hit"
        return result

    appointment=re.search(r"\bAPT-\d{4}\b",q,re.I)
    lookup=None
    if appointment:
        tool_calls["lookup"]+=1
        lookup=check_appointment_status(appointment.group(0))
    tool_calls["rag"]+=1
    rag=rag_lookup(q)
    if not rag["grounded"]:
        result=AgentResponse(answer="I don't know based on the available Practo policy knowledge base.",sources=rag["sources"],grounded=False,refused=True,reason="insufficient_retrieval")
    else:
        text=rag["answer"]
        if lookup and lookup.get("found"):
            text += f" Appointment {lookup['record_id']} is {lookup['status']} with a consultation fee of INR {lookup['consultation_fee_inr']}. Escalation score: {lookup['escalation_score']}."
        result=AgentResponse(answer=text,sources=rag["sources"],appointment_status=lookup.get("status") if lookup else None,escalation_score=lookup.get("escalation_score") if lookup else None,grounded=True)
    cache[key]=result
    add_turn(session_id,q,result.answer)
    return result
