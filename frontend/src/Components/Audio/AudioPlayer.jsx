import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function AudioPlayer() {
  const { language } = useContext(LanguageContext);

  return (
    <button className="audio-mini">
      🔊 {language === "en" ? "Listen" : "सुनें"}
    </button>
  );
}

export default AudioPlayer;
