import { useContext } from "react";
import { Link } from "react-router-dom";
import FileUpload from "../Components/Upload/FileUpload";
import { LanguageContext } from "../context/LanguageContext";
import { UserContext } from "../context/UserContext";

const copy = {
  en: {
    eyebrow: "Launch-ready legal review",
    title: "Turn dense contracts into clear, actionable decisions.",
    subtitle:
      "Upload a PDF or text document to get a plain-language summary, clause-level risk review, bilingual output, and AI-assisted follow-up support.",
    features: [
      "Risk scoring across important clauses",
      "English and Hindi summaries for faster review",
      "Ask questions about the uploaded document",
    ],
    trustTitle: "Built for real review workflows",
    trustText:
      "Use it as a first-pass review layer before legal sign-off, procurement approval, or internal sharing.",
  },
  hi: {
    eyebrow: "लॉन्च के लिए तैयार लीगल रिव्यू",
    title: "जटिल कानूनी दस्तावेज़ों को स्पष्ट और उपयोगी निर्णयों में बदलें।",
    subtitle:
      "PDF या टेक्स्ट दस्तावेज़ अपलोड करें और सरल सारांश, क्लॉज़-स्तरीय जोखिम विश्लेषण, द्विभाषी आउटपुट और एआई-सहायता प्राप्त प्रश्नोत्तर पाएं।",
    features: [
      "महत्वपूर्ण क्लॉज़ का जोखिम स्कोर",
      "तेज़ समझ के लिए अंग्रेज़ी और हिंदी सारांश",
      "अपलोड किए गए दस्तावेज़ पर सवाल पूछें",
    ],
    trustTitle: "वास्तविक समीक्षा वर्कफ़्लो के लिए तैयार",
    trustText:
      "इसे कानूनी अनुमोदन, खरीद समीक्षा या आंतरिक साझा करने से पहले एक पहले-पास विश्लेषण परत की तरह उपयोग करें।",
  },
};

function Home() {
  const { language } = useContext(LanguageContext);
  const { isAuthenticated } = useContext(UserContext);
  const t = copy[language];

  return (
    <div className="page page-home">
      <section className="hero">
        <div className="hero-copy">
          <span className="eyebrow">{t.eyebrow}</span>
          <h1 className="hero-title">{t.title}</h1>
          <p className="hero-subtitle">{t.subtitle}</p>

          <div className="hero-feature-list">
            {t.features.map((feature) => (
              <span key={feature} className="feature-pill">
                {feature}
              </span>
            ))}
          </div>
        </div>

        <div className="hero-panel">
          {isAuthenticated ? (
            <FileUpload />
          ) : (
            <div className="upload-card">
              <div className="upload-card-header">
                <span className="section-kicker">Authentication required</span>
                <h2>Sign in before uploading documents</h2>
                <p>
                  Your uploads, document history, and RAG chat are now tied to your account.
                </p>
              </div>
              <Link className="btn-primary auth-link-button" to="/auth">
                Login or register
              </Link>
            </div>
          )}
        </div>
      </section>

      <section className="insight-grid">
        <article className="spotlight-card">
          <span className="spotlight-stat">3 core modes</span>
          <h2>Analyze, compare, and ask follow-up questions.</h2>
          <p>
            The product now centers around the workflows users actually need
            before signing: understand the document, compare versions, and dig
            into the risky parts.
          </p>
        </article>

        <article className="info-card">
          <h3>{t.trustTitle}</h3>
          <p>{t.trustText}</p>
        </article>
      </section>
    </div>
  );
}

export default Home;
