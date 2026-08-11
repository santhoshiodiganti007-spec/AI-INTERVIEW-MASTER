import React, { createContext, useContext, useState, useEffect } from "react";
import { fetchApi, setAuthToken, getAuthToken } from "../utils/api";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadUser() {
      const token = getAuthToken();
      if (token) {
        try {
          const prof = await fetchApi("/auth/me/profile");
          setProfile(prof);
          setUser({ id: prof.user_id, token });
        } catch (err) {
          console.error("Auth load error:", err);
          setAuthToken(null);
          setUser(null);
        }
      }
      setLoading(false);
    }
    loadUser();
  }, []);

  const login = async (email, password) => {
    const data = await fetchApi("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    setAuthToken(data.access_token);
    setUser({ id: data.user_id, email: data.email, full_name: data.full_name, token: data.access_token });
    const prof = await fetchApi("/auth/me/profile");
    setProfile(prof);
    return data;
  };

  const register = async (email, password, full_name, target_role) => {
    const data = await fetchApi("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, full_name, target_role }),
    });
    setAuthToken(data.access_token);
    setUser({ id: data.user_id, email: data.email, full_name: data.full_name, token: data.access_token });
    const prof = await fetchApi("/auth/me/profile");
    setProfile(prof);
    return data;
  };

  const logout = () => {
    setAuthToken(null);
    setUser(null);
    setProfile(null);
  };

  return (
    <AuthContext.Provider value={{ user, profile, setProfile, loading, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}
