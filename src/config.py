from pathlib import Path
import os

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
KB_DIR = DATA_DIR / "knowledge_base"
RUNTIME_DIR = ROOT / "runtime"
CHROMA_DIR = RUNTIME_DIR / "chroma"

MOCK_LLM = os.getenv("MOCK_LLM", "true").lower() == "true"
os.environ.setdefault("CREWAI_DISABLE_TELEMETRY", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

RUNTIME_DIR.mkdir(exist_ok=True)
