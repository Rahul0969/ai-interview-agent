import { useState } from "react";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL;

function App() {
  const [candidateName, setCandidateName] = useState("");
  const [candidateId, setCandidateId] = useState("");

  const [question, setQuestion] = useState("");
  const [questionNumber, setQuestionNumber] = useState(0);

  const [sessionId, setSessionId] = useState("");

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
        throw new Error(data.detail || "Failed to start interview.");
      }

      setSessionId(newSessionId);
      setQuestion(data.reply);
      setQuestionNumber(data.questionNumber);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <main className="landing">
        {!question ? (
          <>
            <div className="badge">AI-POWERED INTERVIEW</div>

            <h1>
              Your Personal
              <span> AI Interviewer</span>
            </h1>

            <p className="description">
              Practice technical interviews with an adaptive AI interviewer
              that evaluates your answers and adjusts questions based on your
              performance.
            </p>

            <div className="candidate-card">
              <h2>Start Your Interview</h2>

              <label htmlFor="candidateName">Candidate Name</label>

              <input
                id="candidateName"
                type="text"
                placeholder="Enter your name"
                value={candidateName}
                onChange={(e) => setCandidateName(e.target.value)}
              />

              <label htmlFor="candidateId">Candidate ID</label>

              <input
                id="candidateId"
                type="text"
                placeholder="Enter your candidate ID"
                value={candidateId}
                onChange={(e) => setCandidateId(e.target.value)}
              />

              {error && <p className="error">{error}</p>}

              <button onClick={startInterview} disabled={loading}>
                {loading ? "Starting..." : "Start Interview →"}
              </button>
            </div>
          </>
        ) : (
          <div className="interview-card">
            <div className="interview-header">
              <span>AI INTERVIEWER</span>
              <span>Question {questionNumber}</span>
            </div>

            <h2>Interview Question</h2>

            <p className="question">{question}</p>

            <p className="session">
              Session: {sessionId}
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
