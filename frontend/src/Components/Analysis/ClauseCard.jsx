import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function ClauseCard({ titleEn, titleHi, textEn, textHi }) {
  const { language } = useContext(LanguageContext);

  return (
    <div className="clause-card slide-up">
      <h3>{language === "en" ? titleEn : titleHi}</h3>
      <p>{language === "en" ? textEn : textHi}</p>
    </div>
  );
}

export default ClauseCard;
