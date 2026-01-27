import { useState } from "react";

function LanguageToggle() {
    const [language , setLanguage] = useState("en");

    const handleLanguageChange = (lang) => {
        setLanguage(lang);
        console.log("Selected Language: ", lang);

    };

    return (
        <div style = {{ marginBottom: "20px" }}>
            <button onClick={() => handleLanguageChange("en")}
                className={language === "en" ? "btn-primary" : ""}>
            English
            </button>
            <button onClick ={()=>handleLanguageChange("hi")}
            style={{ marginLeft: "10px" }}
            className={language === "hi" ? "btn-primary" : ""}>
                Hindi
            </button>



        </div>
    );

}

export default LanguageToggle;