import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function Loader() {
  const { language } = useContext(LanguageContext);

  return (
    <div className="loader-container fade-in">
      
      <div className="spinner"></div>

      <p className="loader-text">
        {language === "en"
          ? "Analyzing your document, please wait..."
          : "आपके दस्तावेज़ का विश्लेषण किया जा रहा है, कृपया प्रतीक्षा करें..."}
      </p>

    </div>
  );
}

export default Loader;
