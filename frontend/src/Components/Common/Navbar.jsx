import LanguageToggle from "./LanguageToggle";

function Navbar() {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        
       
        <div className="navbar-logo">
          Legal Document AI
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
