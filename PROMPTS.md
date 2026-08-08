# AI Usage Log

## AI Tools Used

- ChatGPT
- Google Gemini 3.6 Flash

## Purpose of AI Assistance

AI tools were used during development for:
- Understanding the hackathon requirements
- Designing the adaptive interview architecture
- Developing and debugging FastAPI components
- Designing prompts for technical answer evaluation
- Generating adaptive follow-up questions
- Designing structured final interview feedback
- Debugging API and JSON-related errors
- Improving project documentation

## Gemini 3.6 Flash

Gemini 3.6 Flash is used as the primary LLM in the application.

It is responsible for:
- Generating interview questions
- Evaluating candidate answers
- Identifying strengths and knowledge gaps
- Selecting adaptive follow-up questions
- Generating final structured interview feedback

## Development Process

AI-generated suggestions were reviewed, modified, integrated, and tested during development.

The application was tested locally using FastAPI and Swagger UI.

## Important Prompts

### Answer Evaluation

The model was instructed to evaluate a candidate's technical answer and return structured information including:

- Score
- Depth
- Curriculum day
- Topic
- Strengths
- Gaps
- Recommendation

### Adaptive Question Generation

The model was instructed to generate one follow-up technical question based on:

- Candidate profile
- Curriculum
- Previous question
- Candidate answer
- Evaluation
- Previously covered curriculum days

### Final Assessment

The model was instructed to generate structured feedback containing:

- Summary
- Strengths
- Knowledge gaps
- Next steps

## Human Verification

The generated code and AI responses were tested and adjusted during development to ensure that the application followed the hackathon requirements.