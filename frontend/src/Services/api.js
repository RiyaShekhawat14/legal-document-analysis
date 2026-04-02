const API_BASE_URL = "http://127.0.0.1:8000";

export const apiRequest = async (endpoint, method = "GET", data = null, isFile = false) => {
  let options = {
    method,
    headers: {}
  };

  if (data && !isFile) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(data);
  }

  if (data && isFile) {
    options.body = data;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
  return response.json();
};