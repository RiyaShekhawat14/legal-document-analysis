import { useState } from "react";

export default function useSpeech() {
  const [speaking, setSpeaking] = useState(false);

  const speakText = (text) => {
    if (!text) return;

    const speech = new SpeechSynthesisUtterance(text);
    speech.lang = "en-US";

    window.speechSynthesis.speak(speech);
    setSpeaking(true);

    speech.onend = () => {
      setSpeaking(false);
    };
  };

  return { speakText, speaking };
}