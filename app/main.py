from app.candidate_engine import build_candidate_profile
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title = "AI Interview Agent")

class InterviewRequest(BaseModel):
    sessionId : str
    candidate : Optional[dict] = None
    message : Optional[str] = None

#temporary storage for session
sessions = {}

@app.get("/")
def root():
    return {"message": "AI Interview Agent is running"}

@app.post("/api/interview")
def interview(request : InterviewRequest):

    session_id = request.sessionId

    if request.candidate is not None:

        candidate_id = request.candidate.get("id")
        candidate_profile = build_candidate_profile(candidate_id)

        sessions[session_id] = {
            "candidate": request.candidate,
            "history" : []
        }

        return {
            "reply": "Welcome. Let's bring your interview.",
            "done": False
        }
    
    if session_id not in sessions:
        return {
            "reply":"Session not found.Please start a new interview.",
            "done": False
        }

    if request.message:
        sessions[session_id]["history"].append({
            "role":"candidate",
            "message": request.message
        })
    return {
        "reply": "Thank you for your answer.Let's continue further.",
        "done": False
    }