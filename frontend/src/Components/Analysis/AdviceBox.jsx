import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function AdviceBox({ adviceEn, adviceHi }) {
  const { language } = useContext(LanguageContext);

  return (
    <div className="advice-box">
      <span className="section-kicker">Recommended next step</span>
      <h3>{language === "en" ? "Advice" : "सुझाव"}</h3>
      <p>{language === "en" ? adviceEn : adviceHi}</p>
    </div>
  );
}

export default AdviceBox;
