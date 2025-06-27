import { useLocation, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import { sendFeedback } from "../api/feedback";

export default function Result() {
  const { token } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();
  
  const data = location.state?.data;
  const imagePreview = location.state?.imagePreview;
  
  const [redirecting, setRedirecting] = useState(false);
  const [feedbackMsg, setFeedbackMsg] = useState("");
  const [feedbackSent, setFeedbackSent] = useState(false);
  
  // 🔐 Redirection douce si non connecté
  useEffect(() => {
    if (!token) {
      setRedirecting(true);
      setTimeout(() => {
        navigate("/");
      }, 2500);
    }
  }, [token, navigate]);
  
  const handleFeedback = async (score) => {
    try {
      await sendFeedback(data.id_image, score, token);
      setFeedbackMsg("✅ Feedback enregistré !");
      setFeedbackSent(true);
    } catch (err) {
      console.error(err);
      setFeedbackMsg("❌ Erreur lors de l'envoi du feedback.");
    }
  };
  
  const labels = {
    1: "❌ Mauvais",
    2: "😐 Moyen",
    3: "👍 Bien",
    4: "🌟 Excellent"
  };
  
  if (redirecting) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white px-4 text-center">
      <p className="text-xl text-gray-600">🔒 Accès non autorisé</p>
      <p className="text-sm text-gray-500 mt-2">Redirection vers la page de connexion...</p>
      </div>
    );
  }
  
  if (!data || !imagePreview) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-white px-4 text-center">
      <p className="text-xl text-gray-600">Aucun résultat disponible.</p>
      <p className="text-sm text-gray-500 mt-2">Redirection en cours...</p>
      </div>
    );
  }
  
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-white px-4 text-center">
    <h1 className="text-3xl font-semibold text-indigo-600 mb-6">Résultat</h1>
    
    <img
    src={imagePreview}
    alt="Image envoyée"
    className="w-64 h-auto rounded shadow mb-6"
    />
    
    <p className="text-xl text-gray-800 mb-2">
    <span className="font-semibold text-indigo-600">🧠 Légende générée :</span><br />
    {data.resultat_pred}
    </p>
    
    <div className="mt-6">
    <p className="text-md font-medium text-gray-700 mb-2">Notez cette légende :</p>
    <div className="flex gap-3 justify-center flex-wrap">
    {[1, 2, 3, 4].map((score) => (
      <button
      key={score}
      onClick={() => handleFeedback(score)}
      disabled={feedbackSent}
      className={`px-4 py-2 rounded font-semibold ${
        feedbackSent
        ? "bg-gray-300 text-gray-600 cursor-not-allowed"
        : "bg-indigo-100 hover:bg-indigo-300 text-indigo-800"
      }`}
      >
      {labels[score]}
      </button>
    ))}
    </div>
    {feedbackMsg && <p className="mt-3 text-sm text-gray-600">{feedbackMsg}</p>}
    <div className="mt-6">
    <button
    onClick={() => navigate("/upload")}
    className="bg-green-500 hover:bg-green-600 text-white font-semibold px-6 py-2 rounded"
    >
    📤 Nouvelle image
    </button>
    </div>
    </div>
    </div>
  );
}