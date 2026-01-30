import { useNavigate } from "react-router-dom";

function ChatFab() {
  const navigate = useNavigate();

  return (
    <button className="chat-fab" onClick={() => navigate("/chat")}>
      💬 Ask AI
    </button>
  );
}

export default ChatFab;
