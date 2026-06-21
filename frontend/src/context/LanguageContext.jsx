/* eslint-disable react-refresh/only-export-components */
import { createContext, useState } from "react";

export const LanguageContext = createContext();

function LanguageProvider({ children }) {
    const [language, setLanguage] = useState("en");

    const changeLanguage = (lang) => {
        setLanguage(lang);
    };

    return (
        <LanguageContext.Provider 
        value={{ language, changeLanguage}}
        >
            {children}
        </LanguageContext.Provider>
    );
}

export default LanguageProvider;
