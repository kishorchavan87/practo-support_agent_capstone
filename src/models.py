from pydantic import BaseModel, Field
from typing import List, Optional

class AgentResponse(BaseModel):
    response_format: str = "practo_support_response"
    answer: str
    sources: List[str] = Field(default_factory=list)
    appointment_status: Optional[str] = None
    escalation_score: Optional[float] = None
    grounded: bool = True
    refused: bool = False
    reason: Optional[str] = None

class AskRequest(BaseModel):
    query: str
    session_id: str = "default"

class AddDocumentRequest(BaseModel):
    document_id: str
    text: str

class VerdictModel(BaseModel):
    approved: bool
    final_answer: str
    reason: str
