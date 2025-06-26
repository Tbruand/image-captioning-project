from api_src.repositories.image_repository import ImageRepository
from api_src.inference.pipeline import InferencePipeline
from PIL import Image
import io

class ImageService:
    def __init__(self, repo: ImageRepository):
        self.repo = repo
        self.pipeline = InferencePipeline(
            decoder_path="outputs/20250625_115742/decoder.pt",
            tokenizer_path="data/vocab/tokenizer.pkl"
        )

    def save_image_and_predict(self, nom_fichier, id_user, file_bytes, monitor_pred=0):
        id_image = self.repo.add_image(nom_fichier, id_user)
        if not id_image:
            return {"success": False, "message": "Erreur insertion image"}

        # 💡 Inférence réelle avec modèle
        resultat_pred, confiance_pred = self.run_inference(file_bytes)

        id_prediction = self.repo.add_prediction(resultat_pred, confiance_pred, id_image, monitor_pred=0)
        if not id_prediction:
            return {"success": False, "message": "Erreur insertion prédiction"}

        return {
            "success": True,
            "id_image": id_image,
            "id_prediction": id_prediction,
            "resultat_pred": resultat_pred,
            "confiance_pred": confiance_pred
        }

    def run_inference(self, file_bytes):
        try:
            result = self.pipeline.predict(file_bytes)  # 🧠 appel du vrai modèle
            return result["caption"], result["confidence_mean"]
        except Exception as e:
            print(f"[ERREUR INFÉRENCE] {e}")
            return "erreur", 0.0
    
        
    def save_feedback(self, id_image: int, id_user: int, monitor_pred: int) -> dict:
        # Appelle le repo pour mettre à jour la colonne monitor_pred dans Prediction
        updated = self.repo.update_monitor_pred(id_image, monitor_pred)
        if not updated:
            return {"success": False, "message": "Impossible de sauvegarder le feedback"}
        return {"success": True, "message": "Feedback sauvegardé"}
