import { useContext, useEffect, useState } from "react";
import { LanguageContext } from "../context/LanguageContext";

import SummaryCard from "../components/Analysis/SummaryCard";
import RiskBadge from "../components/Analysis/RiskBadge";
import ClauseCard from "../components/Analysis/ClauseCard";
import AdviceBox from "../components/Analysis/AdviceBox";
import HighlightedText from "../components/Analysis/HighlightedText";

import VoiceControl from "../components/Audio/VoiceControl";

function Result() {
  const { language } = useContext(LanguageContext);

  const [summaryEn, setSummaryEn] = useState("");
  const [summaryHi, setSummaryHi] = useState("");
  const [advice, setAdvice] = useState("");
  const [riskLevel, setRiskLevel] = useState("");
  const [clauses, setClauses] = useState([]);

  const [voiceLang, setVoiceLang] = useState("en");
  const [speechRate, setSpeechRate] = useState(1);

  useEffect(() => {
    const result = localStorage.getItem("analysisResult");

    if (result) {
      const parsed = JSON.parse(result);
      const data = parsed.data;

      setSummaryEn(data.summary_en);
      setSummaryHi(data.summary_hi);
      setAdvice(data.advice);
      setRiskLevel(data.analysis.overall_risk);
      setClauses(data.analysis.clauses);
    }
  }, []);

  // Speak function
  const speakText = () => {
    const text = language === "hi" ? summaryHi : summaryEn;

    const speech = new SpeechSynthesisUtterance(text);

    const voices = window.speechSynthesis.getVoices();
    let selectedVoice = null;

    if (voiceLang === "hi") {
      selectedVoice = voices.find(v => v.lang.includes("hi"));
    } else {
      selectedVoice = voices.find(v => v.lang.includes("en"));
    }

    if (selectedVoice) {
      speech.voice = selectedVoice;
    }

    speech.rate = speechRate;

    window.speechSynthesis.speak(speech);
  };

  const stopSpeech = () => {
    window.speechSynthesis.cancel();
  };

  return (
    <div className="container fade-in">
      <h1 className="page-title">
        {language === "en" ? "Document Analysis" : "दस्तावेज़ विश्लेषण"}
      </h1>

      {/* SUMMARY */}
      <SummaryCard
        summaryEn={summaryEn}
        summaryHi={summaryHi}
      />

      <button onClick={speakText}>🔊 Speak</button>
      <button onClick={stopSpeech}>⏹ Stop</button>

      {/* VOICE SETTINGS */}
      <VoiceControl
        setVoiceLang={setVoiceLang}
        setSpeechRate={setSpeechRate}
      />

      {/* RISK */}
      <div className="card risk-card">
        <h2>{language === "en" ? "Risk Level" : "जोखिम स्तर"}</h2>
        <RiskBadge level={riskLevel} />
      </div>

      {/* CLAUSES */}
      <div className="card">
        <h2>
          {language === "en"
            ? "Important Clauses"
            : "महत्वपूर्ण शर्तें"}
        </h2>

        {clauses.map((clause, index) => (
          <ClauseCard
            key={index}
            titleEn={`Clause ${index + 1}`}
            titleHi={`शर्त ${index + 1}`}
            textEn={`Risk Level: ${clause.risk}`}
            textHi={`जोखिम स्तर: ${clause.risk}`}
          />
        ))}
      </div>

      {/* HIGHLIGHT */}
      <div className="card">
        <h2>
          {language === "en"
            ? "Highlighted Risks"
            : "हाइलाइट किए गए जोखिम"}
        </h2>

        <HighlightedText
          text={`Overall Risk Level: ${riskLevel}`}
          keywords={["Risk", "High", "Penalty", "Termination"]}
        />
      </div>

      {/* ADVICE */}
      <AdviceBox adviceEn={advice} adviceHi={advice} />
    </div>
  );
}

export default Result;