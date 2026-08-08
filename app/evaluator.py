import json

from app.llm_service import client


def evaluate_answer(question, answer, candidate_profile):
    prompt = f"""
You are a strict but fair technical interview evaluator.

Candidate profile:
{candidate_profile}

Question:
{question}

Candidate answer:
{answer}

Evaluate the candidate's answer.

Return ONLY valid JSON in exactly this format:

{{
    "score": 1,
    "depth": "basic",
    "day" : 1,
    "topic": "",
    "strengths": [],
    "gaps": [],
    "recommendation": "probe_deeper"
}}

Rules:
- score must be an integer from 1 to 5.
- depth must be one of: "basic", "medium", "advanced".
- strengths must contain concise technical strengths.
- gaps must contain concepts the candidate should explain better.
- recommendation must be one of:
  "probe_deeper",
  "change_topic",
  "simplify"
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config = {
            "response_mime_type":"application/json"
        }
    )

    return json.loads(response.text)


def generate_next_question(
    candidate_profile,
    curriculum,
    previous_question,
    answer,
    evaluation,
    covered_days
):
    prompt = f"""
You are an adaptive technical interviewer.

Candidate profile:
{candidate_profile}

Curriculum:
{curriculum}

Previous question:
{previous_question}

Candidate answer:
{answer}

Evaluation:
{evaluation}

Already covered curriculum days:
{covered_days}

Important:
- The interview must cover at least 4 different curriculum days.
- If fewer than 4 days have been covered, prefer an uncovered curriculum day.
- Once 4 different days are covered, you may use the best topic for adaptive follow-up.
- The next question must still be relevant to the candidate's previous answer.
- Ask exactly ONE technical question.
- Do not repeat the previous question.
- Do not provide the answer.

Ask the next best interview question.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()

def generate_final_feedback(candidate_profile, history):
    prompt = f"""
You are a technical interview evaluator.

Candidate profile:
{candidate_profile}

Complete interview history:
{history}

Generate a structured final assessment.

Return ONLY valid JSON in exactly this format:

{{
    "overall_score": 1,
    "strengths": [],
    "knowledge_gaps": [],
    "topics_assessed": [],
    "recommendation": ""
}}

Rules:
- overall_score must be an integer from 1 to 5.
- strengths must contain the candidate's strongest technical areas.
- knowledge_gaps must contain important areas where the candidate needs improvement.
- topics_assessed must list the curriculum topics covered during the interview.
- recommendation must provide a concise overall technical assessment.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)