import {useContext} from "react";
import { LanguageContext } from "../../context/LanguageContext";

function AudioPlayer() {
    const {language} = useContext(LanguageContext);

    return (
        <div className="audio-player card fade-in">
            <h3>
                🔊 {language === "en" ? "Listen to Summary" : "सारांश सुनें"}
            </h3>
             <p className="audio-text">
                {language === "en"
                ? "Click play to hear the document summary in simple language."
                : "सरल भाषा में दस्तावेज़ का सारांश सुनने के लिए प्ले दबाएं।"}
            </p>
             <div className="audio-controls">
                <button className="btn-primary">▶ Play</button>
                <button>⏸ Pause</button>
                <button>⏹ Stop</button>
            </div>
        </div>
    );
}

export default AudioPlayer;
