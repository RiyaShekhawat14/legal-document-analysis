import { useState } from "react";

export default function useUpload() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const uploadDocument = async (file) => {
    if (!file) return;

    setLoading(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/analyze/analyze-risk",
        {
          method: "POST",
          body: formData,
        }
      );

      const result = await response.json();
      localStorage.setItem("analysisResult", JSON.stringify(result));

      setLoading(false);
      return result;
    } catch (err) {
      setError(err);
      setLoading(false);
    }
  };

  return { uploadDocument, loading, error };
}