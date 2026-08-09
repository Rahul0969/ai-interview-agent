import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;
const MAX_QUESTIONS = 8;

function App() {
  const [candidateName, setCandidateName] = useState("");
  const [candidateId, setCandidateId] = useState("");

  const [question, setQuestion] = useState("");
  const [questionNumber, setQuestionNumber] = useState(0);

  const [sessionId, setSessionId] = useState("");

  const [answer, setAnswer] = useState("");
  const [evaluation, setEvaluation] = useState(null);

  const [done, setDone] = useState(false);
  const [feedback, setFeedback] = useState(null);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");


  const startInterview = async () => {
    setError("");

    if (!candidateName.trim() || !candidateId.trim()) {
      setError("Please enter your name and candidate ID.");
      return;
    }

    setLoading(true);

    const newSessionId = `session-${Date.now()}`;

    try {
      const response = await fetch(`${API_URL}/api/interview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sessionId: newSessionId,
          candidate: {
            id: candidateId.trim(),
            name: candidateName.trim(),
          },
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to start interview."
        );
      }

      setSessionId(newSessionId);
      setQuestion(data.reply);
      setQuestionNumber(data.questionNumber);
      setDone(false);
      setFeedback(null);
      setEvaluation(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    setError("");

    if (!answer.trim()) {
      setError("Please enter your answer.");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/interview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sessionId: sessionId,
          message: answer.trim(),
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Failed to submit answer."
        );
      }

      setEvaluation(data.evaluation || null);
      setAnswer("");

      // Interview completed
      if (data.done) {
        setDone(true);
        setFeedback(data.feedback || null);
      } else {
        // Continue to next question
        setQuestion(data.reply);
        setQuestionNumber(data.questionNumber);
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (!question && !done) {
    return (
      <div className="app">
        <main className="landing">

          <div className="badge">
            AI-POWERED INTERVIEW
          </div>

          <h1>
            Your Personal
            <span> AI Interviewer</span>
          </h1>

          <p className="description">
            Practice technical interviews with an adaptive
            AI interviewer that evaluates your answers and
            adjusts questions based on your performance.
          </p>

          <div className="candidate-card">

            <h2>Start Your Interview</h2>

            <label htmlFor="candidateName">
              Candidate Name
            </label>

            <input
              id="candidateName"
              type="text"
              placeholder="Enter your name"
              value={candidateName}
              onChange={(e) =>
                setCandidateName(e.target.value)
              }
            />

            <label htmlFor="candidateId">
              Candidate ID
            </label>

            <input
              id="candidateId"
              type="text"
              placeholder="Enter your candidate ID"
              value={candidateId}
              onChange={(e) =>
                setCandidateId(e.target.value)
              }
            />

            {error && (
              <p className="error">
                {error}
              </p>
            )}

            <button
              onClick={startInterview}
              disabled={loading}
            >
              {loading
                ? "Starting..."
                : "Start Interview →"}
            </button>

          </div>

          <div className="features">

            <div>
              <strong>Adaptive</strong>
              <span>
                Questions adjust to your performance
              </span>
            </div>

            <div>
              <strong>Technical</strong>
              <span>
                Focused on real-world technical skills
              </span>
            </div>

            <div>
              <strong>AI Evaluated</strong>
              <span>
                Get detailed feedback on your answers
              </span>
            </div>

          </div>

        </main>
      </div>
    );
  }

  // -----------------------------------------
  // FINAL FEEDBACK
  // -----------------------------------------

  if (done) {
    return (
      <div className="app">
        <main className="landing">

          <div className="feedback-card">

            <div className="badge">
              INTERVIEW COMPLETED
            </div>

            <h1>
              Interview <span>Complete</span>
            </h1>

            {feedback ? (
              <>
                <div className="feedback-section">
                  <h2>Overall Assessment</h2>

                  <p>
                    {feedback.summary}
                  </p>
                </div>

                <div className="feedback-section">
                  <h2>Strengths</h2>

                  <ul>
                    {feedback.strengths?.map(
                      (item, index) => (
                        <li key={index}>
                          {item}
                        </li>
                      )
                    )}
                  </ul>
                </div>

                <div className="feedback-section">
                  <h2>Areas to Improve</h2>

                  <ul>
                    {feedback.gaps?.map(
                      (item, index) => (
                        <li key={index}>
                          {item}
                        </li>
                      )
                    )}
                  </ul>
                </div>

                <div className="feedback-section">
                  <h2>Recommended Next Steps</h2>

                  <ul>
                    {feedback.next?.map(
                      (item, index) => (
                        <li key={index}>
                          {item}
                        </li>
                      )
                    )}
                  </ul>
                </div>
              </>
            ) : (
              <p>
                Final feedback is unavailable.
              </p>
            )}

          </div>

        </main>
      </div>
    );
  }

  
  return (
    <div className="app">
      <main className="landing">

        <div className="interview-card">

          <div className="interview-header">

            <span>
              AI INTERVIEWER
            </span>

            <span>
              Question {questionNumber}
            </span>

          </div>

          {/* Progress */}

          <div className="progress-container">

            <div className="progress-text">
              Question {questionNumber} of{" "}
              {MAX_QUESTIONS}
            </div>

            <div className="progress-bar">

              <div
                className="progress-fill"
                style={{
                  width: `${
                    (questionNumber / MAX_QUESTIONS) * 100
                  }%`,
                }}
              />

            </div>

          </div>

          <h2>
            Interview Question
          </h2>

          <p className="question">
            {question}
          </p>

          <textarea
            className="answer-box"
            placeholder="Type your answer here..."
            value={answer}
            onChange={(e) =>
              setAnswer(e.target.value)
            }
            rows="8"
          />

          {error && (
            <p className="error">
              {error}
            </p>
          )}

          <button
            className="submit-answer"
            onClick={submitAnswer}
            disabled={loading}
          >
            {loading
              ? "Evaluating..."
              : "Submit Answer →"}
          </button>

          {/* Previous evaluation */}

          {evaluation && (
            <div className="evaluation">

              <h3>
                Previous Answer Evaluation
              </h3>

              <p>
                <strong>Score:</strong>{" "}
                {evaluation.score}/5
              </p>

              <p>
                <strong>Depth:</strong>{" "}
                {evaluation.depth}
              </p>

            </div>
          )}

          <p className="session">
            Session: {sessionId}
          </p>

        </div>

      </main>
    </div>
  );
}

export default App;