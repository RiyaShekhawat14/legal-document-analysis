import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function LanguageToggle() {
  const { language, changeLanguage } = useContext(LanguageContext);

  return (
    <div className="language-toggle" role="group" aria-label="Language toggle">
      <button
        type="button"
        onClick={() => changeLanguage("en")}
        className={language === "en" ? "lang-active" : ""}
      >
        EN
      </button>
      <button
        type="button"
        onClick={() => changeLanguage("hi")}
        className={language === "hi" ? "lang-active" : ""}
      >
        HI
      </button>
    </div>
  );
}

export default LanguageToggle;
