import { useState } from "react";

export default function useTranslation() {
  const [translatedText, setTranslatedText] = useState("");

  const translateText = async (text, language) => {
    const response = await fetch("http://127.0.0.1:8000/translate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        text: text,
        target_language: language,
      }),
    });

    const data = await response.json();
    setTranslatedText(data.translated_text);
  };

  return { translatedText, translateText };
}