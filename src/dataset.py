from dataclasses import asdict, dataclass
from pathlib import Path
import json, random
from collections import Counter

SEED = 20260912
N = 50
CATEGORIES = ["General Medicine", "Cardiology", "Dermatology", "Pediatrics", "Orthopedics"]
STATUSES = ["Scheduled", "Completed", "Cancelled", "No-Show", "Rescheduled"]

@dataclass
class Appointment:
    record_id: str
    category: str
    status: str
    consultation_fee_inr: int
    days_since_created: int
    follow_up_required: bool

def generate_appointments():
    rng = random.Random(SEED)
    records = []
    for i in range(N):
        records.append(Appointment(
            record_id=f"APT-{i+1:04d}",
            category=rng.choice(CATEGORIES),
            status=rng.choice(STATUSES),
            consultation_fee_inr=rng.randrange(500, 2501, 100),
            days_since_created=rng.randint(0, 30),
            follow_up_required=rng.random() < 0.20,
        ))
    records = [asdict(x) for x in records]
    validate(records)
    return records

def validate(records):
    cc = Counter(x["category"] for x in records)
    sc = Counter(x["status"] for x in records)
    follow = sum(x["follow_up_required"] for x in records) / len(records) * 100
    assert len(records) >= 40
    assert all(cc[c] >= 3 for c in CATEGORIES), cc
    assert all(sc[s] >= 1 for s in STATUSES), sc
    assert 10 <= follow <= 30, follow
    assert all(0 <= x["days_since_created"] <= 30 for x in records)
    return cc, sc, follow

APPOINTMENTS = generate_appointments()

def save():
    out = Path(__file__).resolve().parents[1] / "data" / "appointments.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(APPOINTMENTS, indent=2), encoding="utf-8")
    cc, sc, follow = validate(APPOINTMENTS)
    print("category_counts:", dict(cc))
    print("status_counts:", dict(sc))
    print("follow_up_true_percent:", round(follow, 2))
    print("saved:", out)

if __name__ == "__main__":
    save()
