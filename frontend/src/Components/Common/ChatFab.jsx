import { useContext } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { UserContext } from "../../context/UserContext";

function ChatFab() {
  const navigate = useNavigate();
  const location = useLocation();
  const { isAuthenticated } = useContext(UserContext);

  if (location.pathname === "/chat" || !isAuthenticated) {
    return null;
  }

  return (
    <button className="chat-fab" onClick={() => navigate("/chat")} type="button">
      AI Legal Assistant
    </button>
  );
}

export default ChatFab;
