import { useMemo, useState } from "react";
import { compareDocuments } from "../Services/compareService";
import RiskBadge from "../Components/Analysis/RiskBadge";
import Loader from "../Components/Common/Loader";

function Compare() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const ready = useMemo(() => Boolean(file1 && file2), [file1, file2]);

  const handleCompare = async () => {
    if (!ready) {
      setError("Select both documents before comparing.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const data = await compareDocuments(file1, file2);
      setResult(data);
    } catch (err) {
      setError(err.message || "Unable to compare documents.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Version review</span>
        <h1 className="page-title">Compare two legal documents</h1>
        <p className="page-subtitle">
          Review summaries and risk levels side by side before approving a new
          draft.
        </p>
      </div>

      <section className="card compare-intake">
        <label className="upload-field">
          <span>Primary document</span>
          <input type="file" onChange={(e) => setFile1(e.target.files?.[0] || null)} />
          <strong>{file1?.name || "Choose file"}</strong>
        </label>

        <label className="upload-field">
          <span>Comparison document</span>
          <input type="file" onChange={(e) => setFile2(e.target.files?.[0] || null)} />
          <strong>{file2?.name || "Choose file"}</strong>
        </label>

        <button className="btn-primary" onClick={handleCompare} disabled={loading}>
          {loading ? "Comparing..." : "Compare documents"}
        </button>

        {error ? <p className="status-error">{error}</p> : null}
      </section>

      {loading ? <Loader /> : null}

      {result ? (
        <section className="compare-results">
          {["document1", "document2"].map((key, index) => {
            const doc = result[key];
            return (
              <article className="card compare-card" key={key}>
                <div className="compare-card-header">
                  <div>
                    <span className="section-kicker">Document {index + 1}</span>
                    <h2>{index === 0 ? file1?.name : file2?.name}</h2>
                  </div>
                  <RiskBadge level={doc.risk} />
                </div>

                <p>{doc.summary}</p>

                <div className="clause-list">
                  {doc.clauses?.slice(0, 4).map((clause, clauseIndex) => (
                    <div className="clause-card" key={`${key}-${clauseIndex}`}>
                      <div className="clause-card-header">
                        <h3>{clause.clause_type || `Clause ${clauseIndex + 1}`}</h3>
                        <RiskBadge level={clause.risk} compact />
                      </div>
                      <p>Confidence: {clause.confidence ?? "N/A"}</p>
                    </div>
                  ))}
                </div>
              </article>
            );
          })}
        </section>
      ) : null}
    </div>
  );
}

export default Compare;
