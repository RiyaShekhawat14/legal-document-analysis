import { useContext } from "react";
import { LanguageContext } from "../context/LanguageContext";



 import SummaryCard from "../components/Analysis/SummaryCard";
 import RiskBadge from "../components/Analysis/RiskBadge";
 import ClauseCard from "../components/Analysis/ClauseCard";
 import AdviceBox from "../components/Analysis/AdviceBox";
import HighlightedText from "../components/Analysis/HighlightedText";

import AudioPlayer from "../components/Audio/AudioPlayer";
import VoiceControl from "../Components/Audio/VoiceControl";

 
function Result() {
  const { language } = useContext(LanguageContext);

  /* ===== Dummy Analysis Data (AI later) ===== */
  const summaryEn =
    "This contract is a rental agreement for 11 months between the landlord and tenant.";
  const summaryHi =
    "यह अनुबंध मकान मालिक और किरायेदार के बीच 11 महीनों का किराया समझौता है।";

  const riskLevel = "High";

  const clauses = [
    {
      titleEn: "Termination Clause",
      titleHi: "समाप्ति शर्त",
      textEn:
        "Early termination will attract a penalty of two months rent.",
      textHi:
        "समय से पहले समाप्ति पर दो महीने के किराये का जुर्माना लगेगा।",
    },
    {
      titleEn: "Notice Period",
      titleHi: "नोटिस अवधि",
      textEn:
        "A mandatory notice period of 60 days must be served by either party.",
      textHi:
        "किसी भी पक्ष को 60 दिनों का अनिवार्य नोटिस देना होगा।",
    },
  ];

  return (
    <div className="container fade-in">

      {/* PAGE TITLE */}
      <h1 className="page-title">
        {language === "en" ? "Document Analysis" : "दस्तावेज़ विश्लेषण"}
      </h1>

      {/* ================= SUMMARY ================= */}
      <SummaryCard
        summaryEn={summaryEn}
        summaryHi={summaryHi}
      />

      {/* ================= AUDIO ================= */}
      <AudioPlayer />
      <VoiceControl/>

      {/* ================= RISK ================= */}
      <div className="card risk-card">
        <h2>{language === "en" ? "Risk Level" : "जोखिम स्तर"}</h2>
        <RiskBadge level={riskLevel} />
      </div>

      {/* ================= IMPORTANT CLAUSES ================= */}
      <div className="card">
        <h2>
          {language === "en"
            ? "Important Clauses"
            : "महत्वपूर्ण शर्तें"}
        </h2>

        {clauses.map((clause, index) => (
          <ClauseCard
            key={index}
            titleEn={clause.titleEn}
            titleHi={clause.titleHi}
            textEn={clause.textEn}
            textHi={clause.textHi}
          />
        ))}
      </div>

      {/* ================= HIGHLIGHTED RISK TEXT ================= */}
      <div className="card">
        <h2>
          {language === "en"
            ? "Highlighted Risks"
            : "हाइलाइट किए गए जोखिम"}
        </h2>

        <HighlightedText
          text="Early termination will attract a penalty of two months rent."
          keywords={["termination", "penalty"]}
        />
      </div>

      {/* ================= AI ADVICE ================= */}
      <AdviceBox
        adviceEn="You should negotiate the penalty clause before signing the contract."
        adviceHi="अनुबंध पर हस्ताक्षर करने से पहले जुर्माने की शर्त पर बातचीत करें।"
      />

     
    </div>
  );
}

export default Result;
