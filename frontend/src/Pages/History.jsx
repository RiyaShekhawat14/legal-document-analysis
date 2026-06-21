import { useEffect, useState } from "react";
import { deleteDocumentById, getDocuments } from "../Services/documentService";

function History() {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadDocuments = async () => {
      try {
        const data = await getDocuments();
        setDocuments(data);
      } catch (err) {
        setError(err.message || "Unable to load document history.");
      } finally {
        setLoading(false);
      }
    };

    loadDocuments();
  }, []);

  const handleDelete = async (id) => {
    try {
      await deleteDocumentById(id);
      setDocuments((prev) => prev.filter((doc) => doc.id !== id));
    } catch (err) {
      setError(err.message || "Unable to delete the document.");
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Repository</span>
        <h1 className="page-title">Analysis history</h1>
        <p className="page-subtitle">
          Keep track of uploaded legal documents and clean out older runs when
          needed.
        </p>
      </div>

      {loading ? <div className="card">Loading document history...</div> : null}
      {error ? <div className="card status-error">{error}</div> : null}

      {!loading && !documents.length ? (
        <div className="card empty-state">
          <h2>No documents yet</h2>
          <p>Your analyzed files will appear here after the first run.</p>
        </div>
      ) : null}

      <div className="history-list">
        {documents.map((doc) => (
          <article className="card history-card" key={doc.id}>
            <div>
              <span className="section-kicker">Document #{doc.id}</span>
              <h2>{doc.filename}</h2>
              <p>
                Uploaded on{" "}
                {doc.uploaded_at
                  ? new Date(doc.uploaded_at).toLocaleString()
                  : "Unknown date"}
              </p>
              <p>Overall risk: {doc.overall_risk || "Unknown"}</p>
            </div>

            <button className="btn-secondary" onClick={() => handleDelete(doc.id)}>
              Delete
            </button>
          </article>
        ))}
      </div>
    </div>
  );
}

export default History;
