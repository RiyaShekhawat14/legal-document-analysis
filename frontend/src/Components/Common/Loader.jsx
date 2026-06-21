import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function Loader() {
  const { language } = useContext(LanguageContext);

  return (
    <div className="loader-container fade-in">
      <div className="spinner" />
      <p className="loader-text">
        {language === "en"
          ? "Analyzing your document. This may take a moment."
          : "आपके दस्तावेज़ का विश्लेषण किया जा रहा है। इसमें थोड़ा समय लग सकता है।"}
      </p>
    </div>
  );
}

export default Loader;
