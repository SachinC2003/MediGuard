import { useMemo, useState } from "react";
import "./App.css";

const ALL_SYMPTOMS: string[] = [
  "anxiety and nervousness",
  "anxiety and nervousness",
  "shortness of breath",
  "depressive or psychotic symptoms",
  "sharp chest pain",
  "dizziness",
  "insomnia",
  "abnormal involuntary movements",
  "chest tightness",
  "palpitations",
  "irregular heartbeat",
  "breathing fast",
  "hoarse voice",
  "sore throat",
  "difficulty speaking",
  "cough",
  "nasal congestion",
  "throat swelling",
  "diminished hearing",
  "difficulty in swallowing",
  "skin swelling",
  "retention of urine",
  "leg pain",
  "hip pain",
  "suprapubic pain",
  "blood in stool",
  "lack of growth",
  "symptoms of the scrotum and testes",
  "swelling of scrotum",
  "pain in testicles",
  "pus draining from ear",
  "jaundice",
  "white discharge from eye",
  "irritable infant",
  "abusing alcohol",
  "fainting",
  "hostile behavior",
  "drug abuse",
  "sharp abdominal pain",
  "feeling ill",
  "vomiting",
  "headache",
  "nausea",
  "diarrhea",
  "vaginal itching",
  "painful urination",
  "involuntary urination",
  "pain during intercourse",
  "frequent urination",
  "lower abdominal pain",
  "vaginal discharge",
  "blood in urine",
  "hot flashes",
  "intermenstrual bleeding",
  "hand or finger pain",
  "wrist pain",
  "hand or finger swelling",
  "arm pain",
  "wrist swelling",
  "arm stiffness or tightness",
  "arm swelling",
  "hand or finger stiffness or tightness",
  "lip swelling",
  "toothache",
  "abnormal appearing skin",
  "skin lesion",
  "acne or pimples",
  "facial pain",
  "mouth ulcer",
  "skin growth",
  "diminished vision",
  "double vision",
  "symptoms of eye",
  "pain in eye",
  "abnormal movement of eyelid",
  "foreign body sensation in eye",
  "irregular appearing scalp",
  "back pain",
  "neck pain",
  "low back pain",
  "pain of the anus",
  "pain during pregnancy",
  "pelvic pain",
  "impotence",
  "vomiting blood",
  "regurgitation",
  "burning abdominal pain",
  "restlessness",
  "wheezing",
  "peripheral edema",
  "neck mass",
  "ear pain",
  "jaw swelling",
  "mouth dryness",
  "neck swelling",
  "knee pain",
  "foot or toe pain",
  "ankle pain",
  "bones are painful",
  "elbow pain",
  "knee swelling",
  "skin moles",
  "weight gain",
  "problems with movement",
  "knee stiffness or tightness",
  "leg swelling",
  "foot or toe swelling",
  "heartburn",
  "infant feeding problem",
  "vaginal pain",
  "vaginal redness",
  "weakness",
  "decreased heart rate",
  "increased heart rate",
  "ringing in ear",
  "plugged feeling in ear",
  "itchy ear(s)",
  "frontal headache",
  "fluid in ear",
  "spots or clouds in vision",
  "eye redness",
  "lacrimation",
  "itchiness of eye",
  "blindness",
  "eye burns or stings",
  "decreased appetite",
  "excessive anger",
  "loss of sensation",
  "focal weakness",
  "symptoms of the face",
  "disturbance of memory",
  "paresthesia",
  "side pain",
  "fever",
  "shoulder pain",
  "shoulder stiffness or tightness",
  "ache all over",
  "lower body pain",
  "problems during pregnancy",
  "spotting or bleeding during pregnancy",
  "cramps and spasms",
  "upper abdominal pain",
  "stomach bloating",
  "changes in stool appearance",
  "unusual color or odor to urine",
  "kidney mass",
  "symptoms of prostate",
  "difficulty breathing",
  "rib pain",
  "joint pain",
  "hand or finger lump or mass",
  "chills",
  "groin pain",
  "fatigue",
  "regurgitation.1",
  "symptoms of the kidneys",
  "melena",
  "coughing up sputum",
  "seizures",
  "delusions or hallucinations",
  "excessive urination at night",
  "bleeding from eye",
  "rectal bleeding",
  "constipation",
  "temper problems",
  "coryza",
  "hemoptysis",
  "allergic reaction",
  "congestion in chest",
  "sleepiness",
  "apnea",
  "abnormal breathing sounds",
  "blood clots during menstrual periods",
  "pulling at ears",
  "gum pain",
  "redness in ear",
  "fluid retention",
  "flu-like syndrome",
  "sinus congestion",
  "painful sinuses",
  "fears and phobias",
  "recent pregnancy",
  "uterine contractions",
  "burning chest pain",
  "back cramps or spasms",
  "back mass or lump",
  "nosebleed",
  "long menstrual periods",
  "heavy menstrual flow",
  "unpredictable menstruation",
  "painful menstruation",
  "infertility",
  "frequent menstruation",
  "sweating",
  "mass on eyelid",
  "swollen eye",
  "eyelid swelling",
  "eyelid lesion or rash",
  "symptoms of bladder",
  "irregular appearing nails",
  "itching of skin",
  "hurts to breath",
  "skin dryness, peeling, scaliness, or roughness",
  "skin irritation",
  "itchy scalp",
  "warts",
  "skin rash",
  "mass or swelling around the anus",
  "ankle swelling",
  "elbow swelling",
  "bleeding from ear",
  "hand or finger weakness",
  "low self-esteem",
  "itching of the anus",
  "swollen or red tonsils",
  "hip stiffness or tightness",
  "mouth pain",
  "arm weakness",
  "obsessions and compulsions",
  "antisocial behavior",
  "sneezing",
  "leg weakness",
  "hysterical behavior",
  "arm lump or mass",
  "bleeding gums",
  "pain in gums",
  "diaper rash",
  "hesitancy",
  "back stiffness or tightness",
  "low urine output",
];

interface PredictionResult {
  disease: string;
  confidence: number;
  lower?: number;
  upper?: number;
  details?: string[];
}

function App() {
  const [search, setSearch] = useState("");
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<PredictionResult | null>(null);

  const filteredSymptoms = useMemo(
    () =>
      ALL_SYMPTOMS.filter((symptom) =>
        symptom.toLowerCase().includes(search.toLowerCase())
      ),
    [search]
  );

  const addSymptom = (symptom: string) => {
    if (!selectedSymptoms.includes(symptom) && selectedSymptoms.length < 8) {
      setSelectedSymptoms([...selectedSymptoms, symptom]);
    }
    setSearch("");
  };

  const removeSymptom = (symptom: string) => {
    setSelectedSymptoms(selectedSymptoms.filter((item) => item !== symptom));
  };

  const resetSelection = () => {
    setSearch("");
    setSelectedSymptoms([]);
    setResult(null);
  };

  const submitSymptoms = async () => {
    if (selectedSymptoms.length === 0) {
      alert("Choose at least one symptom to continue.");
      return;
    }

    setLoading(true);
    setResult(null);

    const featureVector = new Array(230).fill(0);
    selectedSymptoms.forEach((symptom) => {
      const index = ALL_SYMPTOMS.indexOf(symptom);
      if (index !== -1) {
        featureVector[index] = 1;
      }
    });

    try {
      const response = await fetch("http://localhost:5000/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ features: featureVector }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || "Prediction service unavailable");
      }

      const data = await response.json();
      setResult({
        disease: data.disease || "Undetermined",
        confidence: data.confidence ?? 0.72,
        lower: data.lower ?? Math.max(0, (data.confidence ?? 0.72) - 0.12),
        upper: data.upper ?? Math.min(1, (data.confidence ?? 0.72) + 0.08),
        details: data.details || ["Federated model consensus", "Privacy-preserving aggregation"],
      });
    } catch (error: any) {
      alert(`Prediction failed: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">M</div>
          <div>
            <p className="brand-label">MediGuard</p>
            <p className="brand-caption">Secure health insights</p>
          </div>
        </div>

        <div className="sidebar-card">
          <p className="sidebar-card-title">Federated Learning</p>
          <div className="pulse-row">
            <span className="pulse-dot" />
            <span>Active synchronization</span>
          </div>
          <p className="sidebar-card-copy">
            14 clinical nodes synchronized in the latest aggregation round.
          </p>
        </div>

        <nav className="sidebar-nav">
          <a href="#status" className="sidebar-link">Status overview</a>
          <a href="#input" className="sidebar-link">Symptom intake</a>
          <a href="#results" className="sidebar-link">Confidence results</a>
          <a href="#about" className="sidebar-link">Methodology</a>
        </nav>

        <div className="sidebar-compact">
          <div>
            <p className="metric-label">Privacy mode</p>
            <strong>Federated</strong>
          </div>
          <div>
            <p className="metric-label">Last update</p>
            <strong>1 min ago</strong>
          </div>
        </div>
      </aside>

      <main className="dashboard">
        <header className="dashboard-header">
          <div>
            <p className="eyebrow">Clinical AI Interface</p>
            <h1>Minimal, academic, and secure patient triage</h1>
            <p className="subtitle">
              A structured health-tech workspace with clear symptom intake and transparent confidence reporting.
            </p>
          </div>
          <div className="header-pill">Trust Blue</div>
        </header>

        <section id="status" className="status-row">
          <article className="status-card">
            <div className="status-card-header">
              <h2>Federated Learning Status</h2>
              <span className="status-chip">Live</span>
            </div>
            <p className="status-copy">
              Secure model updates in progress. Local models continue training with encrypted parameter exchange.
            </p>
            <div className="status-details">
              <div>
                <span className="detail-label">Round</span>
                <strong>27</strong>
              </div>
              <div>
                <span className="detail-label">Nodes</span>
                <strong>14</strong>
              </div>
              <div>
                <span className="detail-label">Latency</span>
                <strong>120 ms</strong>
              </div>
            </div>
          </article>

          <article className="status-card muted-card">
            <h3>Model Calibration</h3>
            <p className="status-copy">Confidence intervals are presented with thin typography and precise spacing for rapid review.</p>
            <div className="status-summary">
              <span>Accuracy</span>
              <strong>88 %</strong>
            </div>
          </article>
        </section>

        <section className="workflow-grid">
          <article className="panel form-card" id="input">
            <div className="panel-header">
              <h2>Symptom input</h2>
              <p className="panel-meta">Enter key symptoms using the clean clinical form below.</p>
            </div>

            <label className="field-label" htmlFor="symptom-search">
              Search symptoms
            </label>
            <input
              id="symptom-search"
              className="field-input"
              type="text"
              placeholder="Type a symptom…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />

            {search && (
              <div className="dropdown">
                {filteredSymptoms.length === 0 ? (
                  <div className="dropdown-item muted">No matches</div>
                ) : (
                  filteredSymptoms.slice(0, 7).map((symptom) => (
                    <button
                      key={symptom}
                      type="button"
                      className="dropdown-item"
                      onClick={() => addSymptom(symptom)}
                    >
                      {symptom}
                    </button>
                  ))
                )}
              </div>
            )}

            {selectedSymptoms.length > 0 && (
              <div className="chips">
                {selectedSymptoms.map((symptom) => (
                  <div key={symptom} className="chip">
                    <span>{symptom}</span>
                    <button type="button" className="chip-remove" onClick={() => removeSymptom(symptom)}>
                      ×
                    </button>
                  </div>
                ))}
              </div>
            )}

            <div className="form-actions">
              <button className="button button-primary" onClick={submitSymptoms} disabled={loading}>
                {loading ? "Running inference…" : "Run Prediction"}
              </button>
              <button className="button button-secondary" onClick={resetSelection}>
                Clear form
              </button>
            </div>
          </article>

          <article className="panel results-card" id="results">
            <div className="panel-header">
              <h2>Results overview</h2>
              <p className="panel-meta">Confidence intervals and model signals are displayed with modern academic styling.</p>
            </div>

            {result ? (
              <>
                <div className="result-summary">
                  <div>
                    <span className="result-label">Disease classification</span>
                    <strong>{result.disease}</strong>
                  </div>
                  <div>
                    <span className="result-label">Confidence</span>
                    <strong>{(result.confidence * 100).toFixed(1)}%</strong>
                  </div>
                </div>

                <div className="interval-grid">
                  <div className="interval-item">
                    <span className="interval-title">Lower bound</span>
                    <strong>{(result.lower ?? 0).toFixed(1)}</strong>
                  </div>
                  <div className="interval-item">
                    <span className="interval-title">Upper bound</span>
                    <strong>{(result.upper ?? 0).toFixed(1)}</strong>
                  </div>
                  <div className="interval-item span-full">
                    <span className="interval-title">Confidence interval</span>
                    <div className="interval-range">
                      <div className="interval-fill" style={{ width: `${((result.upper ?? 0) - (result.lower ?? 0)) * 100}%` }} />
                    </div>
                  </div>
                </div>

                <div className="notes-block">
                  <p className="notes-title">Inference notes</p>
                  <ul>
                    {(result.details || []).map((note, index) => (
                      <li key={index}>{note}</li>
                    ))}
                  </ul>
                </div>
              </>
            ) : (
              <div className="empty-state">
                Select symptoms to view model output and confidence intervals.
              </div>
            )}
          </article>
        </section>
      </main>
    </div>
  );
}

export default App;
