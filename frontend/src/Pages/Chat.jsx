import { useState, useContext} from "react";
import { LanguageContext } from "../context/LanguageContext";
import MessageBubble from "../Components/Chat/MessageBubble";
import ChatBox from "../Components/Chat/ChatBox";



function Chat(){
  const { language } = useContext(LanguageContext);

  const [messages, setMessages] = useState([
    {
      sender:"ai",
      text:
      language === "en"
        ? "Hello! How can I assist you with your legal document today?"
        : "नमस्ते! मैं आज आपके कानूनी दस्तावेज़ में आपकी कैसे सहायता कर सकता हूँ?"
    },
  ]);

  const handleSend = (userText) => {
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: userText },
      
    ]);

    //fake ai reply(temp)
    setTimeout(() => {
      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text:
            language === "en"
              ? "I am analyzing your question. This will be AI-powered soon."
              : "मैं आपके प्रश्न का विश्लेषण कर रहा हूँ। जल्द ही यह एआई से जुड़ा होगा।",
        },
      ]);
    }, 800);
  };

  return (
    <div classNAme="container fade-in">
      <h1 className="page-title">
        {language ==="en"
          ? "Chat with LegalBot"
          : "लीगलबॉट से चैट करें"}
      </h1>
      <div className="chat-area card">
        {messages.map((msg, index) => (
          
            <MessageBubble 
            key={index}
            sender={msg.sender}
            text={msg.text}
            />  
        ))}
       
        
      </div>

      <ChatBox onSend={handleSend}/>


    </div>
  );



}

export default Chat;