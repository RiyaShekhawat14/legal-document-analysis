import { useState } from "react";

function Compare() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [result, setResult] = useState(null);

  const handleCompare = async () => {
    if (!file1 || !file2) {
      alert("Please select both documents");
      return;
    }

    const formData = new FormData();
    formData.append("file1", file1);
    formData.append("file2", file2);

    const response = await fetch("http://127.0.0.1:8000/compare", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="container">
      <h1>Compare Documents</h1>

      <input type="file" onChange={(e) => setFile1(e.target.files[0])} />
      <input type="file" onChange={(e) => setFile2(e.target.files[0])} />

      <button onClick={handleCompare}>Compare</button>

      {result && (
        <div className="card">
          <h2>Comparison Result</h2>

          <h3>Document 1</h3>
          <p>Risk: {result.document1.risk}</p>
          <p>Summary: {result.document1.summary}</p>

          <h3>Document 2</h3>
          <p>Risk: {result.document2.risk}</p>
          <p>Summary: {result.document2.summary}</p>
        </div>
      )}
    </div>
  );
}

export default Compare;