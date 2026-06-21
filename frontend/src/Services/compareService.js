import { apiRequest } from "./api";

export const compareDocuments = async (file1, file2) => {
  const formData = new FormData();
  formData.append("file1", file1);
  formData.append("file2", file2);

  return apiRequest("/compare/", "POST", formData, true);
};
