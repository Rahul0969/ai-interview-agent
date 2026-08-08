from app.candidate_engine import build_candidate_profile
from app.curriculum_engine import get_topics
from app.llm_service import generate_first_question
from app.evaluator import evaluate_answer
from app.evaluator import evaluate_answer,generate_next_question
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
        curriculum = get_topics()

        question = generate_first_question(
            candidate_profile,
            curriculum
        )

        sessions[session_id] = {
            "candidate": request.candidate,
            "profile": candidate_profile,
            "curriculum": curriculum,
            "history" : [],
            "current_question": question
        }

        return {
            "reply": question,
            "done": False
        }
    
    if session_id not in sessions:
        return {
            "reply":"Session not found.Please start a new interview.",
            "done": False
        }

    if request.message:
        session = sessions[session_id]
        question = session["current_question"]

        evaluation = evaluate_answer(
            question,
            request.message,
            session["profile"]
        )

        next_question = generate_next_question(
            session["profile"],
            session["curriculum"],
            question,
            request.message,
            evaluation
        )

        session["history"].append({
            "role":"candidate",
            "message": request.message,
            "evaluation": evaluation
        })

        session["current_question"] = next_question

        return {
            "reply": next_question,
            "evaluation": evaluation,
            "done" : False
        }


    return {
        "reply": "Thank you for your answer.Let's continue further.",
        "done": False
    }