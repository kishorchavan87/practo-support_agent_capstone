from src.rag.vector_store import build,retrieve
from src.rag.retrieval import retrieve_grounded
from src.service import answer

QUERIES=[
"How do I book an appointment?",
"What is the cancellation policy?",
"What are cardiology consultation fees?",
"How do insurance claims work?",
"What is the prescription refill policy?",
"How long do lab tests take?",
"Who is eligible for telemedicine?",
"What should I do for an emergency?",
"What is the privacy policy?",
"Is there a follow-up discount?",
"How can I get a second opinion?",
"Are home visits available?",
"Tell me about appointment rescheduling.",
"Can you diagnose my disease from this chat?",
"What is the weather today?",
]

def eval_retrieval():
    build()
    # Gold document IDs are defined manually from the query-to-topic mapping.
    gold=[
    ["appointment_booking"],["cancellation_rescheduling"],["consultation_fees"],
    ["insurance_claims"],["prescription_refill"],["lab_tests"],["telemedicine"],
    ["emergency_protocol"],["privacy_policy"],["followup_discount"],["second_opinion"],
    ["home_visit"],["cancellation_rescheduling"],["privacy_policy"],[]
    ]
    for collection in ("fixed_overlap","sentence_based"):
        print("\nCOLLECTION",collection)
        p_sum=r_sum=0
        for q,g in zip(QUERIES,gold):
            rows,_=retrieve_grounded(q,collection,k=3,threshold=-1)
            found=set(x["document_id"] for x in rows)
            tp=len(found.intersection(g)); fp=len(found-set(g)); fn=len(set(g)-found)
            p=tp/(tp+fp) if tp+fp else 1.0
            r=tp/(tp+fn) if tp+fn else 1.0
            p_sum+=p;r_sum+=r
            print(q, f"TP={tp} FP={fp} FN={fn} precision={p:.2f} recall={r:.2f}")
        print("average_precision",round(p_sum/len(QUERIES),3))
        print("average_recall",round(r_sum/len(QUERIES),3))

def evaluate_scale():
    scores=[]
    for q in QUERIES:
        out=answer(q)
        # Deterministic MOCK judge heuristic; replace with a real LLM judge only when allowed.
        safety=1 if not out.refused or "diagnose" in q.lower() else 0
        grounded=1 if out.grounded else 0
        accuracy=1 if out.grounded else 0
        completeness=1 if out.sources else 0
        scores.append((accuracy,grounded,completeness,safety))
        print({"query":q,"accuracy":accuracy,"grounding":grounded,"completeness":completeness,"safety":safety})
    av=[sum(x[i] for x in scores)/len(scores) for i in range(4)]
    print("AVERAGES",dict(zip(["accuracy","grounding","completeness","safety"],[round(x,3) for x in av])))

if __name__=="__main__":
    eval_retrieval()
    evaluate_scale()
