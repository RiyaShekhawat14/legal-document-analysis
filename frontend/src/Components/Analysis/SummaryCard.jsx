
import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";
import AudioPlayer from "../Audio/AudioPlayer";

function SummaryCard({ summaryEn, summaryHi }) {
  const { language } = useContext(LanguageContext);

  return (
    <div className="card fade-in">
      <div className="summary-header">
        <h2>{language === "en" ? "Summary" : "सारांश"}</h2>
        <AudioPlayer/>
      </div>

      <p>{language === "en" ? summaryEn : summaryHi}</p>
    </div>
  );
}

export default SummaryCard;
