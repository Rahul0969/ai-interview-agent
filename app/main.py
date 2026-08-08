from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title = "AI Interview Agent")

class InterviewRequest(BaseModel):
    sessionId : str
    candidate : Optional[dict] = None
    message : Optional[str] = None

@app.get("/")
def root():
    return {"message": "AI Interview Agent is running"}

@app.post("/api/interview")
def interview(request : InterviewRequest):
    if request.candidate is not None:
        return {
            "reply": "Welcome. Let's bring your interview.",
            "done": False
        }
    return {
        "reply": "Thank you for your answer.Let's continue further.",
        "done": False
    }