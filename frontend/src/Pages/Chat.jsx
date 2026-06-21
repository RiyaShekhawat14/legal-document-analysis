import { useContext, useEffect, useMemo, useState } from "react";
import ChatBox from "../Components/Chat/ChatBox";
import MessageBubble from "../Components/Chat/MessageBubble";
import { getAssistantStatus } from "../Services/chatService";
import { LanguageContext } from "../context/LanguageContext";

const suggestions = {
  en: [
    "What is typically in a termination clause?",
    "What payment terms are standard?",
    "How do liability limitations work?",
    "What's a force majeure clause?",
  ],
  hi: [
    "समाप्ति खंड में आमतौर पर क्या होता है?",
    "मानक भुगतान शर्तें क्या हैं?",
    "दायित्व सीमाएं कैसे काम करती हैं?",
    "बल पूर्वज खंड क्या है?",
  ],
};

function Chat() {
  const { language } = useContext(LanguageContext);
  const [draft, setDraft] = useState("");
  const [status, setStatus] = useState(null);
  const [statusError, setStatusError] = useState("");
  const [loadingStatus, setLoadingStatus] = useState(true);
  const [messages, setMessages] = useState(() => [
    {
      sender: "ai",
      text:
        language === "en"
          ? "Welcome! I can help you understand legal contracts and clauses. Ask me questions about:\n\n• General legal concepts (e.g., what is a termination clause?)\n• Your uploaded documents\n• Clause templates and examples\n• Risk factors in contracts\n\nYou don't need to upload a document to get started!"
          : "स्वागत है! मैं आपको कानूनी अनुबंधों और खंडों को समझने में मदद कर सकता हूं। मुझसे पूछें:\n\n• सामान्य कानूनी अवधारणाओं के बारे में\n• आपके अपलोड किए गए दस्तावेज़ों के बारे में\n• खंड टेम्पलेट और उदाहरण\n• अनुबंधों में जोखिम कारक\n\nशुरू करने के लिए आपको दस्तावेज़ अपलोड करने की आवश्यकता नहीं है!",
    },
  ]);

  const loadStatus = async () => {
    setLoadingStatus(true);
    setStatusError("");

    try {
      const data = await getAssistantStatus();
      setStatus(data);
    } catch (error) {
      setStatusError(error.message || "Unable to load assistant status.");
    } finally {
      setLoadingStatus(false);
    }
  };

  useEffect(() => {
    loadStatus();
  }, []);

  const starters = useMemo(() => suggestions[language], [language]);
  const addSuggestion = (text) => setDraft(text);

  const documentReady = Boolean(status?.document?.document_loaded);

  return (
    <div className="page">
      <div className="page-header">
        <span className="eyebrow">AI Legal Assistant</span>
        <h1 className="page-title">Legal Assistant</h1>
        <p className="page-subtitle">
          Get instant answers about legal concepts, contract clauses, and risk assessment. 
          Works with or without uploaded documents.
        </p>
      </div>

      {documentReady && (
        <section className="assistant-status-grid">
          <article className="card assistant-status-card">
            <span className="section-kicker">Current Document</span>
            <h2>{status?.document?.filename || "Document"} is loaded</h2>
            <p>
              Your document has been processed and indexed with {status?.document?.chunk_count || 0} content chunks.
              I can now answer questions specific to this document.
            </p>
            <div className="status-pill-row">
              <span className="status-pill">
                Chunks: {status?.document?.chunk_count || 0}
              </span>
            </div>
          </article>
        </section>
      )}

      {statusError ? <div className="card status-error">{statusError}</div> : null}

      <section className="card chat-page-shell">
        <div className="chat-starters">
          {starters.map((item) => (
            <button
              key={item}
              className="chip-button"
              onClick={() => addSuggestion(item)}
              type="button"
            >
              {item}
            </button>
          ))}
        </div>

        <div className="chat-history">
          {messages.map((message, index) => (
            <MessageBubble
              key={`${message.sender}-${index}`}
              sender={message.sender}
              text={message.text}
              isThinking={message.isThinking}
            />
          ))}
        </div>

        <ChatBox
          draft={draft}
          setDraft={setDraft}
          messages={messages}
          setMessages={setMessages}
          disabled={loadingStatus}
        />
      </section>
    </div>
  );
}

export default Chat;
