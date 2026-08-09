import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not configured.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-3.6-flash"

def generate_first_question(candidate_profile, curriculum):

    prompt = f"""
You are an AI technical interviewer.

Candidate profile:
{candidate_profile}

Available curriculum:
{curriculum}

Start the interview by asking ONE technical question.

Requirements:
- Make the question relevant to the candidate's background.
- Use a topic from the curriculum.
- Do not ask multiple questions.
- Do not provide the answer.
- Keep the question concise.
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")

    return response.text.strip()