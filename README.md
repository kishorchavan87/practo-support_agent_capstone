# Practo Domain Support Agent — Healthcare Track

This repository implements the four-part capstone described in the supplied brief.

## Important
The capstone brief explicitly states that AI assistants and code-generation tools are prohibited for the submitted work. This package is therefore provided as a **learning/reference scaffold**, not as a submission to represent as wholly your own work. Review, rewrite, test, and validate every component against your course rules before using it.

## Architecture
- Deterministic appointment dataset
- 12-policy knowledge base
- Sentence and fixed-overlap chunking
- Local SentenceTransformers embeddings
- Two ChromaDB collections
- Grounded MOCK_LLM generation
- CrewAI Retrieval/Lookup/Composer crew
- Session memory
- Pydantic structured responses
- PII and prompt-injection guardrails
- FastAPI HTTP + WebSocket API
- JSONL structured logging
- 15-query evaluation
- AutoGen review stage
- Governance/budget/caching demonstrations

## Dataset design choices
- Seed: 20260912
- Records: 50
- Categories: the five required categories, sampled with equal weights
- Statuses: the five required statuses, sampled with equal weights
- Consultation fee: INR 500–2500, selected in INR 100 increments
- follow_up_required: weight 0.20
- days_since_created: uniform integer 0–30

The generator validates all assignment constraints rather than hand-editing records.

## Zero-key mode
Set:
CREWAI_DISABLE_TELEMETRY=true
MOCK_LLM=true

The default demonstration path is deterministic and does not require an API key. SentenceTransformers and ChromaDB run locally.

## Windows setup
1. Install Python 3.11.
2. Open PowerShell in this directory.
3. Create a virtual environment:
   `py -3.11 -m venv .venv`
4. Activate:
   `.venv\Scripts\Activate.ps1`
5. Install:
   `pip install -r requirements.txt`
6. Run the complete local demo:
   `python run_demo.py`
7. Start FastAPI:
   `uvicorn src.api.main:app --reload`

API:
- POST /ask
- POST /add-document
- WS /ws/{session_id}

Swagger:
http://127.0.0.1:8000/docs

## Linux/macOS
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python run_demo.py
uvicorn src.api.main:app --reload

## Suggested commands
python -m src.dataset
python scripts/build_index.py
python scripts/run_evaluation.py
python run_demo.py

Generated runtime files are written under runtime/ and are ignored by git.

## Governance notes
The example system classifies itself as High risk because it operates in a healthcare/patient-support context and can process appointment information. It does not diagnose or make clinical treatment decisions.

## Acceptance checklist
See `docs/acceptance_checklist.md`.
