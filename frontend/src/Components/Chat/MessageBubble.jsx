function MessageBubble({ text, sender, isThinking = false }) {
  const renderText = () => {
    if (isThinking) {
      return (
        <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
          <span>Analyzing...</span>
          <div style={{ display: "flex", gap: "4px" }}>
            <span style={{
              animation: "pulse 1.5s ease-in-out infinite",
              animationDelay: "0s",
            }}>•</span>
            <span style={{
              animation: "pulse 1.5s ease-in-out infinite",
              animationDelay: "0.3s",
            }}>•</span>
            <span style={{
              animation: "pulse 1.5s ease-in-out infinite",
              animationDelay: "0.6s",
            }}>•</span>
          </div>
        </div>
      );
    }
    
    return text.split('\n').map((line, index) => (
      <div key={index}>
        {line}
      </div>
    ));
  };

  return (
    <div className={`message-bubble ${sender}`}>
      <p style={{ margin: 0 }}>
        {renderText()}
      </p>
      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 0.6; }
          50% { opacity: 1; }
        }
      `}</style>
    </div>
  );
}

export default MessageBubble;
