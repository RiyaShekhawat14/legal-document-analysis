import { useState, useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function ChatBox({ onSend }) {
  const { language } = useContext(LanguageContext);
  const [text, setText] = useState("");

  const handleClick = () => {
    if (!text.trim()) return;
    onSend(text);
    setText("");
  };

  return (
    <div className="chat-input">

      <textarea
        rows="2"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder={
          language === "en"
            ? "Ask something about this document..."
            : "इस दस्तावेज़ के बारे में प्रश्न पूछें..."
        }
      />

      <button className="btn-primary" onClick={handleClick}>
        {language === "en" ? "Send" : "भेजें"}
      </button>

    </div>
  );
}

export default ChatBox;
