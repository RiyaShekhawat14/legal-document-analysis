import { apiRequest } from "./api";

export const uploadDocument = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  return await apiRequest(
    "/analyze/analyze-risk",
    "POST",
    formData,
    true
  );
};