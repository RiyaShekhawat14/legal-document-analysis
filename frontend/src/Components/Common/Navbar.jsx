import { Link } from "react-router-dom";
import LanguageToggle from "./LanguageToggle";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">

        {/* Logo */}
        <div className="navbar-logo">
          <Link to="/">Legal Document AI</Link>
        </div>

        {/* Navigation Links */}
        <div className="navbar-links">
          <Link to="/">Home</Link>
          <Link to="/upload">Upload</Link>
          <Link to="/compare">Compare</Link>
          <Link to="/chat">Chat</Link>
          <Link to="/history">History</Link>
        </div>

        {/* Right controls */}
        <div className="navbar-actions">
          <LanguageToggle />
        </div>

      </div>
    </nav>
  );
}

export default Navbar;