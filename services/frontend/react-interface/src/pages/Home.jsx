import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Home() {
  const { user, login } = useAuth();
  const navigate = useNavigate();

  const [identifiant, setIdentifiant] = useState("");
  const [mdp, setMdp] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async () => {
    const result = await login(identifiant, mdp);
    if (result.success) {
      navigate("/upload");
    } else {
      setError("Identifiant ou mot de passe incorrect");
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen px-4 bg-white">
      {!user ? (
        <>
          <h1 className="text-3xl font-bold text-indigo-600 mb-4">Connexion</h1>
          <input
            type="text"
            placeholder="Identifiant"
            value={identifiant}
            onChange={(e) => setIdentifiant(e.target.value)}
            className="border px-4 py-2 mb-3 w-full max-w-sm rounded"
          />
          <input
            type="password"
            placeholder="Mot de passe"
            value={mdp}
            onChange={(e) => setMdp(e.target.value)}
            className="border px-4 py-2 mb-3 w-full max-w-sm rounded"
          />
          {error && <p className="text-red-500">{error}</p>}
          <button
            onClick={handleLogin}
            className="bg-indigo-600 text-white px-6 py-2 rounded hover:bg-indigo-700"
          >
            Se connecter
          </button>
        </>
      ) : (
        <h1 className="text-2xl text-green-600">Bienvenue {user.name} 🎉</h1>
      )}
    </div>
  );
}