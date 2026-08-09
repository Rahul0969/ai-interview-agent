# AI Interview Agent

An AI-powered adaptive technical interview platform that conducts personalized interviews, evaluates candidate answers, and dynamically generates follow-up questions.

## Live Demo

Frontend:
https://ai-interview-agent-red-beta.vercel.app/

Backend:
https://ai-interview-agent-mqdd.onrender.com/

## Features

- AI-powered technical interviews
- Candidate-specific questions
- Adaptive question generation
- Automatic answer evaluation
- Curriculum-based topic coverage
- Technical scoring
- Strength and gap identification
- Final interview feedback
- REST API
- Responsive web interface

## Architecture

React + Vite
        |
        v
Vercel
        |
        v
FastAPI
        |
        v
Gemini API

## Tech Stack

### Frontend

- React
- Vite
- JavaScript
- CSS

### Backend

- Python
- FastAPI
- Pydantic

### AI

- Google Gemini API

### Deployment

- Vercel
- Render

### Development

- GitHub
- VS Code

## API

### Start Interview

POST:

`/api/interview`

Example request:

```json
{
  "sessionId": "phone-test-001",
  "candidate": {
    "id": "CAND-001",
    "name": "Sarah Johnson"
  }
}

### Run: 

```bash
Name: Sarah Johnson
Candidate ID: CAND-001