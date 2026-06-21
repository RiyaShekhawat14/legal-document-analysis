import { useContext } from "react";
import { NavLink } from "react-router-dom";
import { UserContext } from "../../context/UserContext";
import LanguageToggle from "./LanguageToggle";

const navItems = [
  { to: "/", label: "Home" },
  { to: "/compare", label: "Compare" },
  { to: "/chat", label: "Chat" },
  { to: "/history", label: "History" },
];

function Navbar() {
  const { user, isAuthenticated, logout } = useContext(UserContext);

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <NavLink className="navbar-logo" to="/">
          <span className="logo-mark">LA</span>
          <div>
            <strong>Legal Easy AI</strong>
            <span>Legal document analyzer</span>
          </div>
        </NavLink>

        <div className="navbar-links">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              className={({ isActive }) =>
                `nav-link${isActive ? " nav-link-active" : ""}`
              }
            >
              {item.label}
            </NavLink>
          ))}
        </div>

        <div className="navbar-actions">
          {isAuthenticated ? (
            <>
              <span className="user-chip">{user?.username}</span>
              <button className="btn-secondary" type="button" onClick={logout}>
                Logout
              </button>
            </>
          ) : (
            <NavLink className="btn-secondary" to="/auth">
              Login
            </NavLink>
          )}
          <LanguageToggle />
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
