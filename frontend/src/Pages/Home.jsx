import { useContext } from "react";
import { LanguageContext } from "../context/LanguageContext";
import FileUpload from "../components/upload/FileUpload";

function Home() {
  const { language } = useContext(LanguageContext);

  return (
    <div className="container fade-in">

      <section className="home-hero">
        <h1 className="home-title">
          {language === "en"
            ? "Understand Legal Documents Easily"
            : "कानूनी दस्तावेज़ आसानी से समझें"}
        </h1>

        <p className="home-subtitle">
          {language === "en"
            ? "AI-powered summaries, hidden risks, and simple explanations in Hindi and English."
            : "एआई द्वारा सारांश, छुपे हुए जोखिम और आसान भाषा में समझाएं — हिंदी और अंग्रेज़ी में।"}
        </p>
      </section>

      {/* UPLOAD SECTION */}
      <section className="home-upload card slide-up">
        <FileUpload />
      </section>

    </div>
  );
}

export default Home;
