import { useContext } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { UserContext } from "../../context/UserContext";

function ProtectedRoute({ children }) {
  const { authReady, isAuthenticated } = useContext(UserContext);
  const location = useLocation();

  if (!authReady) {
    return (
      <div className="page">
        <div className="card empty-state">
          <h2>Restoring your session...</h2>
        </div>
      </div>
    );
  }

  if (!isAuthenticated) {
    return <Navigate to="/auth" replace state={{ from: location.pathname }} />;
  }

  return children;
}

export default ProtectedRoute;
