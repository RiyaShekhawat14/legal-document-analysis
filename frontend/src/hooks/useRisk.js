import { useEffect, useState } from "react";

export default function useRisk() {
  const [riskData, setRiskData] = useState(null);

  useEffect(() => {
    const result = localStorage.getItem("analysisResult");
    if (result) {
      const parsed = JSON.parse(result);
      setRiskData(parsed.data.analysis);
    }
  }, []);

  return riskData;
}