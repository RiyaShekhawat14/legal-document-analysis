import { useContext } from "react";
import { LanguageContext } from "../context/LanguageContext";
import ChatBox from "../Components/Chat/ChatBox";
import MessageBubble from "../Components/Chat/MessageBubble";

function Chat() {
  const { language } = useContext(LanguageContext);

  return (
    <div className="container fade-in">

      <h1 className="page-title">
        {language === "en"
          ? "Ask Questions about the Document"
          : "दस्तावेज़ के बारे में प्रश्न पूछें"}
      </h1>

      {/* Messages area */}
      <div className="chat-area card">

        <MessageBubble
          sender="ai"
          text={
            language === "en"
              ? "Hi! Ask me anything about this document."
              : "नमस्ते! इस दस्तावेज़ के बारे में कुछ भी पूछें।"
          }
        />

       <MessageBubble 
       sender="user"
          text={
            language === "en"
              ? "What is the notice period?"
              : "नोटिस अवधि क्या है?"
          } />

      </div>

      {/* Input */}
      <ChatBox/>

    </div>
  );
}

export default Chat;
