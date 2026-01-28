import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function ChatBox() {
  const { language } = useContext(LanguageContext);

  return (
    <div className="chat-input">

      <textarea
        rows="2"
        placeholder={
          language === "en"
            ? "Ask something about this document..."
            : "इस दस्तावेज़ के बारे में प्रश्न पूछें..."
        }
      ></textarea>

      <button className="btn-primary">
        {language === "en" ? "Send" : "भेजें"}
      </button>

    </div>
  );
}

export default ChatBox;
