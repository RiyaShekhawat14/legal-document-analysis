import {useState,createContext} from "react";

export const DocumentContext = createContext();

export function DocumentProvider({ children }) {
    const [document,setDocument] = useState(null);
    const [analysis,setAnalysis] = useState(null);

    
  /*
    document = {
      name,
      type,
      text
    }

    analysis = {
      summaryEn,
      summaryHi,
      riskLevel,
      clauses,
      advice
    }
  */

    return (
        <DocumentContext.Provider
          value={{
            document,setDocument,
            analysis,setAnalysis
          }} >
            {children}
          </DocumentContext.Provider>
    );
}