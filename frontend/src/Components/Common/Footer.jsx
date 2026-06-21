import { useContext } from "react";
import { LanguageContext } from "../../context/LanguageContext";

function Footer() {
  const { language } = useContext(LanguageContext);

  return (
    <footer className="footer">
      <div className="footer-inner">
        <div>
          <h3>Legal Easy AI</h3>
          <p className="footer-text">
            {language === "en"
              ? "AI-assisted contract review for faster understanding, safer decisions, and clearer follow-up questions."
              : "तेज़ समझ, सुरक्षित निर्णय और बेहतर फॉलो-अप प्रश्नों के लिए एआई-सहायता प्राप्त कॉन्ट्रैक्ट समीक्षा।"}
          </p>
        </div>

        <p className="footer-text">
          {language === "en"
            ? "Disclaimer: This tool supports legal review, but it does not replace qualified legal advice."
            : "अस्वीकरण: यह टूल कानूनी समीक्षा में सहायता करता है, लेकिन योग्य कानूनी सलाह का विकल्प नहीं है।"}
        </p>
      </div>
      <p className="footer-copy">© 2026 Legal Easy AI</p>
    </footer>
  );
}

export default Footer;
