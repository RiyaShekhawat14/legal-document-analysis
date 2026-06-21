/* eslint-disable react-refresh/only-export-components */
import { createContext, useEffect, useState } from "react";
import { fetchCurrentUser } from "../Services/authService";

export const UserContext = createContext();

function readStoredUser() {
  try {
    const raw = localStorage.getItem("auth_user");
    return raw ? JSON.parse(raw) : null;
  } catch {
    return null;
  }
}

export function UserProvider({ children }) {
  const [user, setUser] = useState(() => readStoredUser());
  const [token, setToken] = useState(() => localStorage.getItem("auth_token"));
  const [authReady, setAuthReady] = useState(false);

  const persistSession = (nextUser, nextToken) => {
    setUser(nextUser);
    setToken(nextToken);

    if (nextToken) {
      localStorage.setItem("auth_token", nextToken);
    } else {
      localStorage.removeItem("auth_token");
    }

    if (nextUser) {
      localStorage.setItem("auth_user", JSON.stringify(nextUser));
    } else {
      localStorage.removeItem("auth_user");
    }
  };

  const login = (payload) => {
    persistSession(payload.user, payload.access_token);
  };

  const logout = () => {
    persistSession(null, null);
  };

  useEffect(() => {
    let active = true;

    const restoreSession = async () => {
      if (!token) {
        setAuthReady(true);
        return;
      }

      try {
        const profile = await fetchCurrentUser();
        if (active) {
          persistSession(profile, token);
        }
      } catch {
        if (active) {
          persistSession(null, null);
        }
      } finally {
        if (active) {
          setAuthReady(true);
        }
      }
    };

    restoreSession();

    return () => {
      active = false;
    };
  }, [token]);

  return (
    <UserContext.Provider
      value={{
        user,
        token,
        authReady,
        isAuthenticated: Boolean(user && token),
        setUser,
        login,
        logout,
      }}
    >
      {children}
    </UserContext.Provider>
  );
}
