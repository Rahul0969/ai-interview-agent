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
    evaluation
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

Based on the candidate's answer and evaluation, ask the ONE best
next interview question.

Rules:
- If the recommendation is "probe_deeper", ask a deeper follow-up
  about the identified gap.
- If the recommendation is "change_topic", move to another relevant
  curriculum topic.
- If the recommendation is "simplify", ask a simpler question that
  helps test the missing fundamental concept.
- Do not repeat the previous question.
- Ask exactly ONE question.
- Do not explain the answer.
- Keep it concise.
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()