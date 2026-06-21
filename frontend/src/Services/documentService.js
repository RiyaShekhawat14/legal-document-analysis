import { apiRequest } from "./api";

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return apiRequest("/analyze/analyze-risk", "POST", formData, true);
};

export const getDocuments = async () => apiRequest("/documents/");

export const deleteDocumentById = async (id) =>
  apiRequest(`/documents/${id}`, "DELETE");
