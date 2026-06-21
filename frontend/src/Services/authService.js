import { API_BASE_URL, apiRequest } from "./api";

async function submitAuthForm(endpoint, username, password) {
  let response;
  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
      cache: "no-store",
    });
  } catch {
    throw new Error(
      `Cannot reach backend at ${API_BASE_URL}. Make sure the FastAPI server is running and CORS allows this frontend origin.`,
    );
  }

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.detail || payload.message || "Unable to complete authentication.");
  }

  return payload;
}

export function registerUser(username, password) {
  return submitAuthForm("/auth/register", username, password);
}

export function loginUser(username, password) {
  return submitAuthForm("/auth/login", username, password);
}

export function fetchCurrentUser() {
  return apiRequest("/auth/me");
}
