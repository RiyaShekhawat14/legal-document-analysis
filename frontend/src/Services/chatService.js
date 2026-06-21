import { apiRequest } from "./api";

export async function getAssistantStatus() {
  return apiRequest("/chat/status");
}

export async function askQuestion(question, messages = []) {
  const history = messages
    .filter((message) => message.sender === "user" || message.sender === "ai")
    .slice(-6)
    .map((message) => ({
      role: message.sender === "ai" ? "assistant" : "user",
      content: message.text,
    }));

  return apiRequest("/chat/ask", "POST", {
    message: question,
    history,
  });
}
