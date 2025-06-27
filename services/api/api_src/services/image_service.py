from api_src.repositories.image_repository import ImageRepository
from api_src.inference.pipeline import InferencePipeline
from PIL import Image
import io

class ImageService:
    def __init__(self, image_repository: ImageRepository):
        self.image_repository = image_repository 
        self.pipeline = InferencePipeline(
            decoder_path="outputs/20250625_115742/decoder.pt",
            tokenizer_path="data/vocab/tokenizer.pkl"
        )

    def save_image_and_predict(
        self,
        nom_fichier: str,
        id_user: int,
        file_bytes: bytes,
        monitor_pred: int,
        translate: bool = False  # 👈 Ajout ici
    ) -> dict:
        try:
            image = Image.open(io.BytesIO(file_bytes)).convert("RGB")

            # 📸 Génération de la légende (avec ou sans traduction)
            caption, confidences = self.pipeline.captioner.generate(image, translate=translate)

            # 💾 Enregistrement (inchangé)
            image_id, prediction_id = self.image_repository.save_prediction(
                user_id=id_user,
                filename=nom_fichier,
                caption=caption,
                confidences=confidences,
                monitor_pred=monitor_pred
            )

            return {
                "success": True,
                "id_image": image_id,
                "id_prediction": prediction_id,
                "resultat_pred": caption,
                "confiance_pred": confidences
            }

        except Exception as e:
            return {"success": False, "message": str(e)}

    def run_inference(self, file_bytes):
        try:
            result = self.pipeline.predict(file_bytes)  # 🧠 appel du vrai modèle
            return result["caption"], result["confidence_mean"]
        except Exception as e:
            return "erreur", 0.0
    
        
    def save_feedback(self, id_image: int, id_user: int, monitor_pred: int) -> dict:
        # Appelle le repo pour mettre à jour la colonne monitor_pred dans Prediction
        updated = self.image_repository.update_monitor_pred(id_image, monitor_pred)
        if not updated:
            return {"success": False, "message": "Impossible de sauvegarder le feedback"}
        return {"success": True, "message": "Feedback sauvegardé"}
