from src.dataset import APPOINTMENTS

def check_appointment_status(record_id: str) -> dict:
    record=next((x for x in APPOINTMENTS if x["record_id"].upper()==record_id.upper()),None)
    if not record:
        return {"found":False,"record_id":record_id}
    recency=record["days_since_created"]/30
    # Designed score: 60% follow-up signal + 40% normalized recency.
    score=0.6*float(record["follow_up_required"])+0.4*recency
    return {
        "found":True,
        "record_id":record["record_id"],
        "status":record["status"],
        "consultation_fee_inr":record["consultation_fee_inr"],
        "escalation_score":round(min(1,score),4),
        "escalate":score >= 0.70,
    }
