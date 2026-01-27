import LanguageToggle from "./LanguageToggle";

function Navbar() {
    return (
        <nav 
        styles ={{
                padding:"15px 20px",
                backgroundColor: "#ffffff",
                borderBottom: "1px solid #e5e7eb",
                marginBottom: "20px",
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
            }}
            >
             <h2>Legal Easy AI</h2>

             <LanguageToggle />
            
        </nav>

        
    
    );
}

export default Navbar;