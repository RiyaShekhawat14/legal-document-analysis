import { useState } from "react";

export default function useRisk() {
  const [riskData] = useState(() => {
    const result = localStorage.getItem("analysisResult");

    if (!result) {
      return null;
    }

    try {
      const parsed = JSON.parse(result);
      return parsed.data.analysis;
    } catch {
      return null;
    }
  });

  return riskData;
}
