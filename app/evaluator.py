import json
from app.llm_service import client, MODEL_NAME

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
    "day": 1,
    "topic": "",
    "strengths": [],
    "gaps": [],
    "recommendation": "probe_deeper"
}}

Rules:
- score must be an integer from 1 to 5.
- depth must be one of: "basic", "medium", "advanced".
- day must be an integer representing the curriculum day.
- topic must contain the main technical topic being evaluated.
- strengths must contain concise technical strengths.
- gaps must contain concepts the candidate should explain better.
- recommendation must be one of:
  "probe_deeper",
  "change_topic",
  "simplify"
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty evaluation.")

    try:
        evaluation = json.loads(response.text)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Gemini returned invalid evaluation JSON: {response.text}"
        ) from error

    return evaluation


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

Rules:
- The interview should cover at least 4 different curriculum days.
- If fewer than 4 days have been covered, choose an uncovered curriculum day.
- Once 4 different days are covered, choose the best topic based on the candidate's performance.
- The next question must be relevant to the candidate's previous answer.
- Ask exactly ONE technical question.
- Do not repeat the previous question.
- Do not provide the answer.
- Keep the question concise.

Ask the next best interview question.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty question.")

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
    "summary": "",
    "strengths": [],
    "gaps": [],
    "next": []
}}

Rules:
- summary must be a concise overall assessment of the candidate.
- strengths must contain concise, actionable technical strengths.
- gaps must contain concise, actionable technical weaknesses or missing knowledge.
- next must contain concise recommendations for what the candidate should learn or improve next.
- strengths, gaps, and next must all be arrays of strings.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    if not response.text:
        raise RuntimeError("Gemini returned empty final feedback.")

    try:
        feedback = json.loads(response.text)
    except json.JSONDecodeError as error:
        raise RuntimeError(
            f"Gemini returned invalid feedback JSON: {response.text}"
        ) from error

    return feedback