import { createContext, useContext, useState, useEffect } from "react";

const AuthContext = createContext();

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(null);

  // ✅ Au chargement, on récupère le token stocké
  useEffect(() => {
    const savedToken = localStorage.getItem("token");
    const savedUser = localStorage.getItem("user");

    if (savedToken && savedUser) {
      setToken(savedToken);
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const login = async (identifiant, mdp) => {
    try {
      const formData = new URLSearchParams();
      formData.append("username", identifiant);
      formData.append("password", mdp);

      const response = await fetch("http://localhost:8000/login", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData.toString(),
      });

      if (!response.ok) throw new Error("Connexion échouée");

      const data = await response.json();
      const userData = { name: identifiant };

      setUser(userData);
      setToken(data.access_token);

      // ✅ Sauvegarde dans localStorage
      localStorage.setItem("token", data.access_token);
      localStorage.setItem("user", JSON.stringify(userData));

      return { success: true };
    } catch (err) {
      console.error("Erreur :", err.message);
      return { success: false, message: err.message };
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  return useContext(AuthContext);
}