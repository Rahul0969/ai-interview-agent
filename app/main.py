from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.candidate_engine import build_candidate_profile
from app.curriculum_engine import get_topics
from app.llm_service import generate_first_question
from app.evaluator import (
    evaluate_answer,
    generate_next_question,
    generate_final_feedback
)

app = FastAPI(title="AI Interview Agent")

sessions = {}

MAX_QUESTIONS = 8
MIN_CURRICULUM_DAYS = 4

class InterviewRequest(BaseModel):
    sessionId: str
    candidate: Optional[dict] = None
    message: Optional[str] = None

@app.get("/")
def root():
    return {
        "message": "AI Interview Agent is running"
    }

@app.post("/api/interview")
def interview(request: InterviewRequest):

    session_id = request.sessionId

    if not session_id:
        raise HTTPException(
            status_code=400,
            detail="sessionId is required."
        )

    if request.candidate is not None:

        candidate_id = request.candidate.get("id")

        if not candidate_id:
            raise HTTPException(
                status_code=400,
                detail="Candidate ID is required."
            )

        candidate_profile = build_candidate_profile(candidate_id)

        if candidate_profile is None:
            raise HTTPException(
                status_code=404,
                detail=f"Candidate '{candidate_id}' not found."
            )

        curriculum = get_topics()

        if not curriculum:
            raise HTTPException(
                status_code=500,
                detail="Curriculum is empty or unavailable."
            )

        question = generate_first_question(
            candidate_profile,
            curriculum
        )

        sessions[session_id] = {
            "candidate": request.candidate,
            "profile": candidate_profile,
            "curriculum": curriculum,
            "history": [],
            "current_question": question,
            "question_count": 1,
            "covered_days": []
        }

        return {
            "reply": question,
            "done": False,
            "questionNumber": 1
        }


    if session_id not in sessions:
        return {
            "reply": "Session not found. Please start a new interview.",
            "done": False
        }

    session = sessions[session_id]

    if request.message is not None:

        answer = request.message.strip()

        if not answer:
            raise HTTPException(
                status_code=400,
                detail="Answer cannot be empty."
            )

        question = session["current_question"]

        evaluation = evaluate_answer(
            question,
            answer,
            session["profile"]
        )

        session["history"].append({
            "question": question,
            "answer": answer,
            "evaluation": evaluation
        })

        # Track curriculum day
        day = evaluation.get("day")

        if day is not None and day not in session["covered_days"]:
            session["covered_days"].append(day)

        if session["question_count"] >= MAX_QUESTIONS:

            final_feedback = generate_final_feedback(
                session["profile"],
                session["history"]
            )

            return {
                "reply": "Interview completed.",
                "done": True,
                "feedback": final_feedback,
                "questionCount": session["question_count"],
                "coveredDays": session["covered_days"]
            }

        next_question = generate_next_question(
            session["profile"],
            session["curriculum"],
            question,
            answer,
            evaluation,
            session["covered_days"]
        )

        session["current_question"] = next_question
        session["question_count"] += 1

        return {
            "reply": next_question,
            "evaluation": evaluation,
            "done": False,
            "questionNumber": session["question_count"],
            "coveredDays": session["covered_days"]
        }

    return {
        "reply": session["current_question"],
        "done": False,
        "questionNumber": session["question_count"]
    }