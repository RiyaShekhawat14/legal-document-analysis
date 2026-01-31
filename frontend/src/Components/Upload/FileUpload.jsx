import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import { DocumentContext } from "../../context/DocumentContext";

import { LanguageContext } from "../../context/LanguageContext";

function FileUpload() {
  const { language } = useContext(LanguageContext);
  const {setDocument} = useContext(DocumentContext);
  const navigate = useNavigate();

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    setDocument({
      name: file.name,
      type: file.type,
      file: file,
    });
    };

  const handleAnalyzeClick = () => {
    // Abhi sirf navigation
    navigate("/result");
  };

  return (
    <div className="upload-box">

      <p>
        {language === "en"
          ? "Select a legal document (PDF / DOC / TXT)"
          : "कानूनी दस्तावेज़ चुनें (PDF / DOC / TXT)"}
      </p>

      <input
        type="file"
        onChange={handleFileChange}
      />

      <button className="btn-primary mt-20" onClick={handleAnalyzeClick}>
        {language === "en" ? "Analyze Document" : "दस्तावेज़ विश्लेषण करें"}
      </button>

    </div>
  );
}

export default FileUpload;
