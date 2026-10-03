"""Lightweight public research-demo API. No Databricks or private patient data."""
import os
import math
from collections import defaultdict, deque
from threading import Lock
from time import monotonic
from types import SimpleNamespace
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pulsecast.agent.gemini import GeminiClient
from pulsecast.agent.orchestrator import WearableAgent
from pulsecast.agent.schemas import AgentRequest, AgentResult

app = FastAPI(title="PulseCast Gemini demo API")
app.add_middleware(CORSMiddleware, allow_origins=[os.environ.get("PULSECAST_ALLOWED_ORIGINS", "https://davidvalenta-dev.github.io")], allow_methods=["POST", "GET"], allow_headers=["Content-Type"])
LABELS = [5.5,5.6,5.9,6.4,5.7,5.8,5.3,5.6,6.1,6,6,5.6,5.7,5.5,5.5,5.5]
requests_by_ip = defaultdict(deque)
lock = Lock()

def tools_for(subject, minute, audience):
    n = int(subject)
    def risk_at(t):
        return {"minute": t, "smoothed_probability": round(max(8,min(94,35+n%5*6+t*.36+math.sin(t/9+n)*7)))/100,
                "signal_confidence": (.34 if 42<=t<=48 else (94+n%4)/100), "data_status": "synthetic illustrative replay; not trained model output"}
    def summary(subject_id):
        return {"subject_id":subject,"hba1c":LABELS[n-1],"hba1c_source":"PhysioNet v1.1.3 demographics", "cgm_status":"not imported; independent validation unavailable", "wearable_data":"synthetic", "minute":minute, "heart_rate_bpm":round(69+n%9+minute*.12+math.sin(minute/8)*3),"rmssd_ms":round(54-n%8-minute*.14)}
    def tool(name, fn, properties):
        spec={"name":name,"description":name.replace('_',' '),"parameters":{"type":"object","properties":properties}}
        return SimpleNamespace(fn=fn,parameters=spec["parameters"],spec=lambda:spec)
    scoped={"subject_id":{"type":"string"}}
    tools={"get_current_risk":tool("get_current_risk",lambda subject_id:risk_at(minute),scoped),
           "get_risk_history":tool("get_risk_history",lambda subject_id,n=12:[risk_at(t) for t in range(max(0,minute-min(int(n),90)+1),minute+1)],{**scoped,"n":{"type":"integer"}}),
           "get_subject_summary":tool("get_subject_summary",summary,scoped)}
    if audience=="doctor":
        tools["compare_cohorts"]=tool("compare_cohorts",lambda top_k=10:{"status":"real wearable comparison unavailable; no trained model"},{"top_k":{"type":"integer"}})
    return tools

@app.get('/health')
def health():
    return {"status":"ok", "llm_configured":bool(os.environ.get("GEMINI_API_KEY")),"data_mode":"public labels / synthetic signals"}

@app.post('/agent', response_model=AgentResult)
def query(body:AgentRequest, request:Request):
    if body.subject_id not in {str(i).zfill(3) for i in range(1,17)}:
        raise HTTPException(400,"Unknown participant")
    if body.audience=='patient' and body.subject_id!='004':
        raise HTTPException(403,"Patient demo is assigned to participant 004")
    if len(body.question)>2000 or not body.question.strip():
        raise HTTPException(400,"Question must contain 1–2000 characters")
    now=monotonic()
    with lock:
        # Per-process bounded public-demo throttle, not a distributed production limiter.
        if len(requests_by_ip)>5000:
            requests_by_ip.clear()
        hits=requests_by_ip[request.client.host if request.client else 'unknown']
        while hits and hits[0]<now-60: hits.popleft()
        if len(hits)>=5: raise HTTPException(429,"Please wait a minute before asking again")
        hits.append(now)
    if not os.environ.get('GEMINI_API_KEY'):
        raise HTTPException(503,"Configure GEMINI_API_KEY in Render")
    try:
        agent=WearableAgent(GeminiClient(),tools_for(body.subject_id,body.minute,body.audience))
        return agent.run(body)
    except Exception:
        raise HTTPException(502,"LLM unavailable. Check model access and free-tier quota.") from None
