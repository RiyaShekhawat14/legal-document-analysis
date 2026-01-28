import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function VoiceControl() {
  const { language } = useContext(LanguageContext);

  return (
    <div className="voice-control card slide-up">

      <h3>
        🎙 {language === "en" ? "Voice Settings" : "आवाज़ सेटिंग्स"}
      </h3>

      {/* Voice Language */}
      <div className="voice-row">
        <label>
          {language === "en" ? "Voice Language:" : "आवाज़ की भाषा:"}
        </label>
        <select>
          <option>{language === "en" ? "English" : "अंग्रेज़ी"}</option>
          <option>{language === "en" ? "Hindi" : "हिंदी"}</option>
        </select>
      </div>

      {/* Voice Speed */}
      <div className="voice-row">
        <label>
          {language === "en" ? "Speech Speed:" : "बोलने की गति:"}
        </label>
        <select>
          <option>0.8x</option>
          <option>1x</option>
          <option>1.2x</option>
        </select>
      </div>

    </div>
  );
}

export default VoiceControl;
