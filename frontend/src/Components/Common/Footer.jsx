import { use, useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function Footer () {
    const {language} = useContext(LanguageContext);

    return (
        <footer className="footer" > 
        <p className="footer-text">
        {language === "en"
          ? "⚠️ Disclaimer: This tool provides AI-assisted analysis and is not a substitute for legal advice."
          : "⚠️ अस्वीकरण: यह टूल एआई आधारित विश्लेषण प्रदान करता है और कानूनी सलाह का विकल्प नहीं है।"}
        </p>
        <p className="footer-text">
            © 2026 Legal Easy AI

        </p>
        

        
        </footer>

        
   );
}

export default Footer;
