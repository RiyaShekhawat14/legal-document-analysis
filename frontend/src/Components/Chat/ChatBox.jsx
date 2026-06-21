import { useEffect, useState } from "react";
import { askQuestion } from "../../Services/chatService";

function ChatBox({ draft, setDraft, messages, setMessages, disabled = false }) {
  const [input, setInput] = useState(draft || "");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setInput(draft || "");
  }, [draft]);

  const sendMessage = async () => {
    const value = input.trim();

    if (!value || loading || disabled) {
      return;
    }

    const nextMessages = [...messages, { sender: "user", text: value }];
    setMessages(nextMessages);
    setInput("");
    setDraft("");
    setLoading(true);

    // Add thinking indicator
    const thinkingMessage = { sender: "ai", text: "Thinking...", isThinking: true };
    setMessages([...nextMessages, thinkingMessage]);

    try {
      const startTime = Date.now();
      const result = await askQuestion(value, messages);
      const elapsedTime = Date.now() - startTime;
      
      // Ensure minimum response time for natural feel (1.5 seconds)
      const minTime = 1500;
      if (elapsedTime < minTime) {
        await new Promise(resolve => setTimeout(resolve, minTime - elapsedTime));
      }

      setMessages([
        ...nextMessages,
        { sender: "ai", text: result.answer, mode: result.mode, isThinking: false },
      ]);
    } catch (error) {
      setMessages([
        ...nextMessages,
        {
          sender: "ai",
          text: error.message || "I couldn't answer that right now.",
          isThinking: false,
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-input-shell">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask about the document or get legal advice..."
        disabled={disabled || loading}
        onKeyDown={(event) => {
          if (event.key === "Enter") {
            sendMessage();
          }
        }}
      />
      <button
        className="btn-primary"
        onClick={sendMessage}
        type="button"
        disabled={disabled || loading}
      >
        {loading ? "Analyzing..." : "Send"}
      </button>
    </div>
  );
}

export default ChatBox;
