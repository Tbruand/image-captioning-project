import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { uploadImage } from "../api/upload";

export default function Upload() {
  const { token } = useAuth();
  const navigate = useNavigate();

  const [image, setImage] = useState(null);
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [redirecting, setRedirecting] = useState(false); // ✅ pour message de transition

  useEffect(() => {
    if (!token) {
      setRedirecting(true);
      setTimeout(() => {
        navigate("/");
      }, 2500); // ⏳ redirection après 2,5 sec
    }
  }, [token, navigate]);

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setImage(URL.createObjectURL(selected));
      setFile(selected);
    }
  };

  const handleSubmit = async () => {
    if (!file) {
      setError("Veuillez sélectionner une image.");
      return;
    }

    try {
      setLoading(true);
      const result = await uploadImage(file, token);
      navigate("/result", { state: { data: result, imagePreview: image } });
    } catch (err) {
      setError("Échec de l'envoi : " + err.message);
    } finally {
      setLoading(false);
    }
  };

  if (redirecting) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white px-4 text-center">
        <p className="text-xl text-gray-600">🔒 Accès non autorisé</p>
        <p className="text-sm text-gray-500 mt-2">Redirection vers la page de connexion...</p>
      </div>
    );
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white px-4">
      <h1 className="text-3xl font-semibold text-indigo-600 mb-4">Uploader une image</h1>

      <input
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="mb-4"
      />

      {image && (
        <img src={image} alt="Aperçu" className="w-64 h-auto rounded shadow mb-4" />
      )}

      {error && <p className="text-red-500 mb-3">{error}</p>}

      <button
        onClick={handleSubmit}
        className={`px-6 py-2 rounded text-white ${
          loading ? "bg-gray-400 cursor-not-allowed" : "bg-indigo-600 hover:bg-indigo-700"
        }`}
        disabled={loading}
      >
        {loading ? "Envoi en cours..." : "Envoyer à l'API"}
      </button>
    </div>
  );
}