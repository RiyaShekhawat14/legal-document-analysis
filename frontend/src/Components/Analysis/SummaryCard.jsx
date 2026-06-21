import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function SummaryCard({ summaryEn, summaryHi }) {
  const { language } = useContext(LanguageContext);

  return (
    <div className="card">
      <div className="section-header">
        <div>
          <span className="section-kicker">Executive summary</span>
          <h2>{language === "en" ? "Summary" : "सारांश"}</h2>
        </div>
      </div>

      <p className="summary-text">{language === "en" ? summaryEn : summaryHi}</p>
    </div>
  );
}

export default SummaryCard;
