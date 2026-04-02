import { useEffect, useState } from "react";

function History() {
  const [documents, setDocuments] = useState([]);

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    const response = await fetch("http://127.0.0.1:8000/documents/");
    const data = await response.json();
    setDocuments(data);
  };

  const deleteDocument = async (id) => {
    await fetch(`http://127.0.0.1:8000/documents/${id}`, {
      method: "DELETE",
    });

    fetchDocuments();
  };

  return (
    <div className="container">
      <h1>Document History</h1>

      {documents.map((doc) => (
        <div className="card" key={doc.id}>
          <p><b>File:</b> {doc.filename}</p>
          <p><b>Uploaded:</b> {doc.uploaded_at}</p>

          <button onClick={() => deleteDocument(doc.id)}>
            Delete
          </button>
        </div>
      ))}
    </div>
  );
}

export default History;