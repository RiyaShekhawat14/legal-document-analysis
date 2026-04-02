import { useContext, useState } from "react";
import { useNavigate } from "react-router-dom";
import { DocumentContext } from "../../context/DocumentContext";
import { LanguageContext } from "../../context/LanguageContext";

function FileUpload() {
  const { language } = useContext(LanguageContext);
  const { setDocument } = useContext(DocumentContext);
  const navigate = useNavigate();

  const [selectedFile, setSelectedFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setSelectedFile(file);

    setDocument({
      name: file.name,
      type: file.type,
      file: file,
    });
  };

  const handleAnalyzeClick = async () => {
    if (!selectedFile) {
      alert("Please select a file first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", selectedFile);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze/analyze-risk",
        {
          method: "POST",
          body: formData,
        }
      );

      const result = await response.json();

      console.log("Backend Result:", result);

      // Save result for Result page
      localStorage.setItem("analysisResult", JSON.stringify(result));

      setLoading(false);
      navigate("/result");
    } catch (error) {
      console.error(error);
      setLoading(false);
      alert("Error analyzing document");
    }
  };

  return (
    <div className="upload-box">
      <p>
        {language === "en"
          ? "Select a legal document (PDF / DOC / TXT)"
          : "कानूनी दस्तावेज़ चुनें (PDF / DOC / TXT)"}
      </p>

      <input type="file" onChange={handleFileChange} />

      <button className="btn-primary mt-20" onClick={handleAnalyzeClick}>
        {loading
          ? "Analyzing..."
          : language === "en"
          ? "Analyze Document"
          : "दस्तावेज़ विश्लेषण करें"}
      </button>
    </div>
  );
}

export default FileUpload;