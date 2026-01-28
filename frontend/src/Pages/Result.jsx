import { useContext } from "react";
import { LanguageContext } from "../context/LanguageContext";
import AudioPlayer from "../Components/Audio/AudioPlayer";
import VoiceControl from "../Components/Audio/VoiceControls";
import ChatBox from "../Components/Chat/ChatBox";
import MessageBubble from "../Components/Chat/MessageBubble";

function Result() {
  const { language } = useContext(LanguageContext);

  const summaryEn =
    "This contract is between two parties for a rental agreement of 11 months.";
  const summaryHi =
    "यह अनुबंध 11 महीनों के किराये के समझौते के लिए दो पक्षों के बीच है।";

  const riskLevel = "High";

  const clauses = [
    {
      titleEn: "Termination Clause",
      titleHi: "समाप्ति शर्त",
      textEn:
        "If the tenant leaves before 6 months, a penalty of 2 months rent applies.",
      textHi:
        "यदि किरायेदार 6 महीने से पहले छोड़ता है, तो 2 महीने के किराये का जुर्माना लगेगा।",
    },
    {
      titleEn: "Notice Period",
      titleHi: "नोटिस अवधि",
      textEn: "A notice period of 60 days is mandatory.",
      textHi: "60 दिनों का नोटिस देना अनिवार्य है।",
    },
  ];

  return (
    <div className="container fade-in">

      <h1 className="page-title">
        {language === "en" ? "Analysis Result" : "विश्लेषण परिणाम"}
      </h1>

      {/* Summary Card */}
      
      <div className="card">
        <h2>{language === "en" ? "Summary" : "सारांश"}</h2>

        <p>{language === "en" ? summaryEn : summaryHi}</p>

        {/* AUDIO UI */}
        <AudioPlayer />
        <VoiceControl />
       </div>

      {/* Risk Card */}
      <div className="card risk-card">
        <h2>{language === "en" ? "Risk Level" : "जोखिम स्तर"}</h2>
        <span className="risk-high">
          {language === "en" ? "High Risk" : "उच्च जोखिम"}
        </span>
      </div>

      {/* Clauses */}
      <div className="card">
        <h2>
          {language === "en"
            ? "Important Clauses"
            : "महत्वपूर्ण शर्तें"}
        </h2>

        {clauses.map((clause, index) => (
          <div key={index} className="clause-card slide-up">
            <h3>
              {language === "en" ? clause.titleEn : clause.titleHi}
            </h3>
            <p>
              {language === "en" ? clause.textEn : clause.textHi}
            </p>
          </div>
        ))}
      </div>

        <div className="card">
        <h2>
          {language === "en"
            ? "Ask Questions About This Document"
            : "इस दस्तावेज़ के बारे में प्रश्न पूछें"}
        </h2>

        <div className="chat-area">
          <MessageBubble 
            sender="ai"
            text={
              language === "en"
                ? "You can ask me anything about this document."
                : "आप इस दस्तावेज़ के बारे में कुछ भी पूछ सकते हैं।"
            }
          />
        </div>

        < ChatBox />  
      </div>   

    </div>
  );
}

export default Result;
