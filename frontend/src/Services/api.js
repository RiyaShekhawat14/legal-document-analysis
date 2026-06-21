const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL?.replace(/\/$/, "") ||
  "http://127.0.0.1:8000";

function getStoredToken() {
  return localStorage.getItem("auth_token");
}

export async function apiRequest(
  endpoint,
  method = "GET",
  data = null,
  isFile = false,
) {
  const options = {
    method,
    headers: {},
  };
  const token = getStoredToken();

  if (token) {
    options.headers.Authorization = `Bearer ${token}`;
  }

  if (data && !isFile) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(data);
  }

  if (data && isFile) {
    options.body = data;
  }

  let response;
  try {
    response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  } catch {
    throw new Error(
      `Cannot reach backend at ${API_BASE_URL}. Make sure the FastAPI server is running and CORS allows this frontend origin.`,
    );
  }

  const payload = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(payload.detail || payload.message || "Something went wrong.");
  }

  return payload;
}

export { API_BASE_URL };
