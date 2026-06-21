import { useContext, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { LanguageContext } from "../context/LanguageContext";
import SummaryCard from "../Components/Analysis/SummaryCard";
import RiskBadge from "../Components/Analysis/RiskBadge";
import ClauseCard from "../Components/Analysis/ClauseCard";
import AdviceBox from "../Components/Analysis/AdviceBox";
import HighlightedText from "../Components/Analysis/HighlightedText";
import VoiceControl from "../Components/Audio/VoiceControl";

const copy = {
  en: {
    title: "Document analysis",
    missing: "No analysis result was found. Upload a document to begin.",
    risk: "Overall risk",
    clauses: "Priority clauses",
    highlights: "Risk signals",
    speak: "Speak summary",
    stop: "Stop",
    assistant: "Open AI assistant",
  },
  hi: {
    title: "दस्तावेज़ विश्लेषण",
    missing: "कोई विश्लेषण परिणाम नहीं मिला। शुरू करने के लिए दस्तावेज़ अपलोड करें।",
    risk: "कुल जोखिम",
    clauses: "प्राथमिक क्लॉज़",
    highlights: "जोखिम संकेत",
    speak: "सारांश सुनें",
    stop: "रोकें",
    assistant: "एआई असिस्टेंट खोलें",
  },
};

function getStoredAnalysis() {
  const result = localStorage.getItem("analysisResult");

  if (!result) {
    return null;
  }

  try {
    return JSON.parse(result)?.data ?? null;
  } catch {
    return null;
  }
}

function Result() {
  const { language } = useContext(LanguageContext);
  const [voiceLang, setVoiceLang] = useState("en");
  const [speechRate, setSpeechRate] = useState(1);
  const data = useMemo(() => getStoredAnalysis(), []);
  const t = copy[language];

  if (!data) {
    return (
      <div className="page">
        <div className="card empty-state">
          <h1 className="page-title">{t.title}</h1>
          <p>{t.missing}</p>
        </div>
      </div>
    );
  }

  const summaryText = language === "hi" ? data.summary_hi : data.summary_en;
  const riskLevel = data.analysis?.overall_risk || "Unknown";
  const clauses = data.analysis?.clauses || [];

  const speakText = () => {
    const speech = new SpeechSynthesisUtterance(summaryText);
    speech.rate = speechRate;

    const voices = window.speechSynthesis.getVoices();
    const selectedVoice = voices.find((voice) =>
      voice.lang.toLowerCase().includes(voiceLang),
    );

    if (selectedVoice) {
      speech.voice = selectedVoice;
    }

    window.speechSynthesis.speak(speech);
  };

  const stopSpeech = () => {
    window.speechSynthesis.cancel();
  };

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">Analysis output</span>
        <h1 className="page-title">{t.title}</h1>
        <p className="page-subtitle">{data.filename}</p>
      </div>

      <div className="result-layout">
        <div className="result-main">
          <SummaryCard summaryEn={data.summary_en} summaryHi={data.summary_hi} />

          <div className="card action-row">
            <button className="btn-primary" onClick={speakText}>
              {t.speak}
            </button>
            <button className="btn-secondary" onClick={stopSpeech}>
              {t.stop}
            </button>
            <Link className="btn-secondary" to="/chat">
              {t.assistant}
            </Link>
          </div>

          <div className="card">
            <div className="section-header">
              <h2>{t.clauses}</h2>
              <span className="section-count">{clauses.length} clauses reviewed</span>
            </div>

            <div className="clause-list">
              {clauses.map((clause, index) => (
                <ClauseCard
                  key={`${clause.clause_type}-${index}`}
                  titleEn={clause.clause_type || `Clause ${index + 1}`}
                  titleHi={clause.clause_type || `क्लॉज़ ${index + 1}`}
                  textEn={`Risk: ${clause.risk} • Confidence: ${clause.confidence ?? "N/A"}`}
                  textHi={`जोखिम: ${clause.risk} • विश्वास स्तर: ${clause.confidence ?? "N/A"}`}
                />
              ))}
            </div>
          </div>

          <div className="card">
            <h2>{t.highlights}</h2>
            <HighlightedText
              text={`Overall Risk Level: ${riskLevel}. Advice: ${data.advice}`}
              keywords={["Risk", "High", "Penalty", "Termination", "Advice"]}
            />
          </div>

          <AdviceBox adviceEn={data.advice} adviceHi={data.advice} />
        </div>

        <aside className="result-sidebar">
          <div className="card metric-card">
            <span className="section-kicker">{t.risk}</span>
            <RiskBadge level={riskLevel} />
          </div>

          <VoiceControl
            setVoiceLang={setVoiceLang}
            setSpeechRate={setSpeechRate}
          />
        </aside>
      </div>
    </div>
  );
}

export default Result;
