import os

from dotenv import load_dotenv
from google import genai


load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


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
        model ="gemini-3.6-flash",
        contents = prompt
    )

    return response.text 