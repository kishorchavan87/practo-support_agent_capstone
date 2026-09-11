import json,time,uuid,logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from src.models import AskRequest, AddDocumentRequest, AgentResponse
from src.service import answer
from src.config import KB_DIR

app=FastAPI(title="Practo Domain Support Agent")

class JsonlFormatter(logging.Formatter):
    def format(self, record):
        return json.dumps({"trace_id":getattr(record,"trace_id","-"),"message":record.getMessage(),"time":time.time()})

handler=logging.FileHandler("runtime/app.jsonl",encoding="utf-8")
handler.setFormatter(JsonlFormatter())
logger=logging.getLogger("practo")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

@app.post("/ask",response_model=AgentResponse)
def ask(req: AskRequest):
    trace=str(uuid.uuid4()); start=time.perf_counter()
    result=answer(req.query,req.session_id)
    logger.info(json.dumps({"endpoint":"/ask","request":req.query,"duration_ms":round((time.perf_counter()-start)*1000,2)}),extra={"trace_id":trace})
    return result

@app.post("/add-document")
def add_document(req:AddDocumentRequest):
    p=KB_DIR/(req.document_id+".md")
    p.write_text(req.text,encoding="utf-8")
    return {"ok":True,"document_id":req.document_id}

@app.websocket("/ws/{session_id}")
async def websocket_chat(ws:WebSocket,session_id:str):
    await ws.accept()
    try:
        while True:
            query=await ws.receive_text()
            result=answer(query,session_id)
            await ws.send_json(result.model_dump())
    except WebSocketDisconnect:
        # Client disconnect is expected; do not terminate the server.
        return
