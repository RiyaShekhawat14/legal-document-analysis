import { useState } from "react";
import { askQuestion } from "../../services/chatService";

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input) return;

    // User message
    const userMessage = { sender: "user", text: input };
    setMessages(prev => [...prev, userMessage]);

    // Call RAG backend
    const answer = await askQuestion(input);

    // Bot message
    const botMessage = { sender: "bot", text: answer };
    setMessages(prev => [...prev, botMessage]);

    setInput("");
  };

  return (
    <div className="chat-container">
      <div className="chat-messages">
        {messages.map((msg, index) => (
          <div
            key={index}
            className={
              msg.sender === "user"
                ? "message user-message"
                : "message bot-message"
            }
          >
            {msg.text}
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about the document..."
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
}

export default ChatBox;