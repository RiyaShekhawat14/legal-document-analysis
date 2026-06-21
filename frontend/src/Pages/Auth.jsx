import { useContext, useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { loginUser, registerUser } from "../Services/authService";
import { UserContext } from "../context/UserContext";

function Auth() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login, isAuthenticated } = useContext(UserContext);
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const redirectTo = location.state?.from || "/";

  useEffect(() => {
    if (isAuthenticated) {
      navigate(redirectTo, { replace: true });
    }
  }, [isAuthenticated, navigate, redirectTo]);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const trimmedUsername = username.trim();
      const payload =
        mode === "login"
          ? await loginUser(trimmedUsername, password)
          : await registerUser(trimmedUsername, password);
      login(payload);
      navigate(redirectTo, { replace: true });
    } catch (requestError) {
      setError(requestError.message || "Unable to complete authentication.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page page-auth">
      <section className="auth-shell card">
        <div className="auth-copy">
          <span className="eyebrow">Secure workspace</span>
          <h1 className="page-title">Sign in to your legal review workspace</h1>
          <p className="page-subtitle">
            Authentication now protects uploads, history, compare, and document-grounded chat.
          </p>
        </div>

        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="auth-toggle">
            <button
              type="button"
              className={mode === "login" ? "auth-tab auth-tab-active" : "auth-tab"}
              onClick={() => setMode("login")}
            >
              Login
            </button>
            <button
              type="button"
              className={mode === "register" ? "auth-tab auth-tab-active" : "auth-tab"}
              onClick={() => setMode("register")}
            >
              Register
            </button>
          </div>

          <label className="auth-field">
            <span>Username</span>
            <input
              value={username}
              onChange={(event) => setUsername(event.target.value)}
              placeholder="legal-team"
              required
            />
          </label>

          <label className="auth-field">
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="At least 8 characters"
              required
            />
          </label>

          <button className="btn-primary" disabled={loading} type="submit">
            {loading ? "Please wait..." : mode === "login" ? "Login" : "Create account"}
          </button>

          {error ? <p className="status-error">{error}</p> : null}
        </form>
      </section>
    </div>
  );
}

export default Auth;
