# AI Interview Agent

An adaptive AI-powered technical interview agent that conducts conversational interviews, evaluates candidate responses, and dynamically generates follow-up questions based on performance.

## Features

- Conversational technical interview
- Adaptive follow-up questions
- Candidate session management
- Response evaluation using Gemini 3.6 Flash
- Curriculum-day tracking
- Context maintained throughout the interview
- Minimum 8-question interview flow
- Coverage across multiple curriculum days
- Structured final candidate feedback
- FastAPI REST API
- Interactive Swagger API documentation

## How It Works

```text
Candidate
   ↓
FastAPI /api/interview
   ↓
Interview Session
   ↓
Question Generation
   ↓
Candidate Response
   ↓
AI Evaluation
   ↓
Adaptive Follow-up
   ↓
Curriculum Tracking
   ↓
Final Structured Feedback
```

## Tech Stack
- Python
- FastAPI
- Gemini 3.6 Flash
- Pydantic

## How to Run

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables
GEMINI_API_KEY=your_api_key_here