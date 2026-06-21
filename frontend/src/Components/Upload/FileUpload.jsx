import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { uploadDocument } from "../../Services/documentService";
import { DocumentContext } from "../../context/DocumentContext";
import { LanguageContext } from "../../context/LanguageContext";
import Loader from "../Common/Loader";

function FileUpload() {
  const { language } = useContext(LanguageContext);
  const { setDocument, setAnalysis } = useContext(DocumentContext);
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (event) => {
    const file = event.target.files?.[0];

    if (!file) {
      return;
    }

    setError("");
    setSelectedFile(file);
    setDocument({
      name: file.name,
      type: file.type,
      file,
    });
  };

  const handleAnalyzeClick = async () => {
    if (!selectedFile) {
      setError("Select a document before starting analysis.");
      return;
    }

    setLoading(true);
    setError("");

    try {
      const result = await uploadDocument(selectedFile);
      localStorage.setItem("analysisResult", JSON.stringify(result));
      setAnalysis(result.data);
      navigate("/result");
    } catch (err) {
      setError(err.message || "Error analyzing document.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-card">
      <div className="upload-card-header">
        <span className="section-kicker">Analyze now</span>
        <h2>
          {language === "en"
            ? "Upload a legal document"
            : "कानूनी दस्तावेज़ अपलोड करें"}
        </h2>
        <p>
          {language === "en"
            ? "Supports PDF and TXT files for risk analysis, summary, translation, and chat indexing."
            : "जोखिम विश्लेषण, सारांश, अनुवाद और चैट इंडेक्सिंग के लिए PDF और TXT फाइलें समर्थित हैं।"}
        </p>
      </div>

      <label className="upload-dropzone">
        <input type="file" accept=".pdf,.txt" onChange={handleFileChange} />
        <span>{selectedFile ? selectedFile.name : "Choose file or drag it here"}</span>
        <small>PDF, TXT</small>
      </label>

      <button className="btn-primary" onClick={handleAnalyzeClick} disabled={loading}>
        {loading
          ? "Analyzing..."
          : language === "en"
            ? "Analyze document"
            : "दस्तावेज़ विश्लेषण करें"}
      </button>

      {error ? <p className="status-error">{error}</p> : null}
      {loading ? <Loader /> : null}
    </div>
  );
}

export default FileUpload;
