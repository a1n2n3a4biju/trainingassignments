
import { useMemo, useState } from "react";
import Papa from "papaparse";
import {
  BrainCircuit, Upload, Clock, CheckCircle2, XCircle,
  MessageSquare, Zap, FileSpreadsheet, ChevronDown
} from "lucide-react";
import "./App.css";

const isModelId = (value = "") =>
  /\/|:free|gpt-|gemma|nemotron|llama/i.test(String(value));

const readableModel = (id = "") => {
  const names = {
    "nvidia/nemotron-3-ultra-550b-a55b:free": "NVIDIA Nemotron 3 Ultra",
    "google/gemma-4-26b-a4b-it:free": "Google Gemma 4 26B",
    "openai/gpt-oss-120b": "OpenAI GPT OSS 120B",
  };
  return names[id] || id;
};

function normalizeRow(row) {
  let question = String(row.question || "").trim();
  let model = String(row.model || "").trim();

  // Correct rows where model and question values were interchanged.
  if (isModelId(question) && !isModelId(model)) {
    [question, model] = [model, question];
  }

  return {
    timestamp: row.timestamp || "",
    question,
    model: readableModel(model),
    answer: row.answer || "",
    retrieved: row.retrieved_chunk_ids || "",
    distance: Number(row.best_distance) || 0,
    retrieval: Number(row.retrieval_seconds) || 0,
    generation: Number(row.generation_seconds) || 0,
    total: Number(row.total_seconds) || 0,
    promptTokens: Number(row.prompt_tokens) || 0,
    completionTokens: Number(row.completion_tokens) || 0,
    totalTokens: Number(row.total_tokens) || 0,
    feedback: row.feedback || "Not rated",
    status: row.status || (row.answer ? "Success" : "Failed"),
    error: row.error || "",
  };
}

function App() {
  const [records, setRecords] = useState([]);
  const [selectedQuestion, setSelectedQuestion] = useState("all");
  const [selectedModel, setSelectedModel] = useState("all");
  const [fileName, setFileName] = useState("");

  const handleUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    Papa.parse(file, {
      header: true,
      skipEmptyLines: true,
      complete: (result) => {
        const cleaned = result.data
          .map(normalizeRow)
          .filter((r) => r.question && r.model);

        setRecords(cleaned);
        setFileName(file.name);
        setSelectedQuestion("all");
        setSelectedModel("all");
      },
      error: (error) => alert("Could not read CSV: " + error.message),
    });
  };

  const questions = useMemo(
    () => [...new Set(records.map((r) => r.question))],
    [records]
  );

  const models = useMemo(
    () => [...new Set(records.map((r) => r.model))],
    [records]
  );

  const filtered = records.filter((r) =>
    (selectedQuestion === "all" || r.question === selectedQuestion) &&
    (selectedModel === "all" || r.model === selectedModel)
  );

  const successful = filtered.filter(
    (r) => r.status.toLowerCase() === "success"
  );

  const failed = filtered.filter(
    (r) => r.status.toLowerCase() === "failed"
  );

  const average = (items, field) =>
    items.length
      ? items.reduce((sum, r) => sum + r[field], 0) / items.length
      : 0;

  const comparison = models.map((model) => {
    const items = filtered.filter(
      (r) => r.model === model && r.status.toLowerCase() === "success"
    );

    return {
      model,
      count: items.length,
      avgTime: average(items, "total"),
      avgTokens: average(items, "totalTokens"),
      correct: items.filter((r) => r.feedback === "Correct").length,
      incorrect: items.filter((r) => r.feedback === "Incorrect").length,
      accuracy: items.length
        ? (items.filter((r) => r.feedback === "Correct").length / items.length) * 100
        : 0,
    };
  });

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><BrainCircuit /></div>
          <div>
            <h2>RAG<span>Metrics</span></h2>
            <p>Model comparison platform</p>
          </div>
        </div>

        <div className="side-label">WORKSPACE</div>
        <div className="side-link active">
          <FileSpreadsheet size={18} /> Comparison Dashboard
        </div>

        <div className="side-info">
          <div className="status-dot" />
          <span>Local CSV analysis</span>
        </div>
      </aside>

      <main className="main">
        <header className="topbar">
          <div>
            <h1>Model Comparison</h1>
            <p>Analyze and compare your RAG model performance.</p>
          </div>

          <label className="upload-btn">
            <Upload size={17} />
            Upload CSV
            <input
              type="file"
              accept=".csv"
              onChange={handleUpload}
              hidden
            />
          </label>
        </header>

        <section className="file-banner">
          <div className="file-icon"><FileSpreadsheet /></div>
          <div>
            <strong>{fileName || "No CSV file uploaded"}</strong>
            <p>
              {records.length
                ? `${records.length} model responses loaded successfully`
                : "Upload your rag_feedback.csv file to view the results."}
            </p>
          </div>
          <div className="file-status">
            {records.length ? "Loaded" : "Waiting for file"}
          </div>
        </section>

        <section className="stats-grid">
          <Stat icon={<MessageSquare />} label="Total Responses" value={filtered.length} />
          <Stat icon={<BrainCircuit />} label="Models Compared" value={models.length} />
          <Stat icon={<CheckCircle2 />} label="Successful" value={successful.length} />
          <Stat icon={<XCircle />} label="Failed" value={failed.length} />
        </section>

        <section className="filters">
          <div>
            <label>Filter by question</label>
            <select value={selectedQuestion} onChange={(e) => setSelectedQuestion(e.target.value)}>
              <option value="all">All questions</option>
              {questions.map((q) => <option key={q} value={q}>{q}</option>)}
            </select>
          </div>

          <div>
            <label>Filter by model</label>
            <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
              <option value="all">All models</option>
              {models.map((m) => <option key={m} value={m}>{m}</option>)}
            </select>
          </div>
        </section>

        <section className="section">
          <div className="section-heading">
            <div>
              <h2>Performance comparison</h2>
              <p>Compare response time, feedback and token consumption.</p>
            </div>
          </div>

          <div className="comparison-grid">
            {comparison.map((item) => (
              <div className="model-card" key={item.model}>
                <div className="model-heading">
                  <div className="model-avatar"><BrainCircuit /></div>
                  <div>
                    <h3>{item.model}</h3>
                    <span>{item.count} successful responses</span>
                  </div>
                </div>

                <div className="metric">
                  <span><Clock size={15} /> Average response time</span>
                  <strong>{item.avgTime.toFixed(2)} s</strong>
                </div>

                <div className="metric">
                  <span><Zap size={15} /> Average tokens</span>
                  <strong>{Math.round(item.avgTokens)}</strong>
                </div>

                <div className="metric">
                  <span><CheckCircle2 size={15} /> Correct feedback</span>
                  <strong>{item.correct}</strong>
                </div>

                <div className="accuracy">
                  <div className="accuracy-label">
                    <span>Correct feedback rate</span>
                    <strong>{item.accuracy.toFixed(1)}%</strong>
                  </div>
                  <div className="progress">
                    <div style={{ width: `${item.accuracy}%` }} />
                  </div>
                </div>
              </div>
            ))}
            {!comparison.length && <Empty />}
          </div>
        </section>

        <section className="section">
          <div className="section-heading">
            <div>
              <h2>Response comparison</h2>
              <p>Review the answers generated by each model.</p>
            </div>
          </div>

          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Question</th>
                  <th>Model</th>
                  <th>Answer</th>
                  <th>Time</th>
                  <th>Tokens</th>
                  <th>Feedback</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((r, i) => (
                  <tr key={i}>
                    <td className="question-cell">{r.question}</td>
                    <td><span className="model-tag">{r.model}</span></td>
                    <td className="answer-cell">{r.answer || r.error || "No answer returned"}</td>
                    <td>{r.total.toFixed(2)} s</td>
                    <td>{r.totalTokens}</td>
                    <td>
                      <span className={`feedback ${r.feedback.toLowerCase().replace(" ", "-")}`}>
                        {r.feedback}
                      </span>
                    </td>
                    <td>
                      <span className={`status ${r.status.toLowerCase()}`}>
                        {r.status}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {!filtered.length && <Empty />}
          </div>
        </section>

        <section className="section">
          <div className="section-heading">
            <div>
              <h2>Detailed response information</h2>
              <p>Retrieval time, generation time and source chunks.</p>
            </div>
          </div>

          <div className="detail-grid">
            {filtered.map((r, i) => (
              <div className="detail-card" key={i}>
                <h3>{r.model}</h3>
                <p className="detail-question">{r.question}</p>
                <div className="detail-numbers">
                  <span>Retrieval <b>{r.retrieval.toFixed(2)}s</b></span>
                  <span>Generation <b>{r.generation.toFixed(2)}s</b></span>
                  <span>Distance <b>{r.distance.toFixed(4)}</b></span>
                </div>
                <p className="sources">Sources: {r.retrieved || "Not available"}</p>
              </div>
            ))}
            {!filtered.length && <Empty />}
          </div>
        </section>

        <footer>RAGMetrics · Multi-Model Evaluation Dashboard</footer>
      </main>
    </div>
  );
}

function Stat({ icon, label, value }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div>
        <p>{label}</p>
        <h2>{value}</h2>
      </div>
    </div>
  );
}

function Empty() {
  return <div className="empty">Upload your CSV to see comparison results.</div>;
}

export default App;
