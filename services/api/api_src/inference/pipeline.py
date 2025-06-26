from PIL import Image
import io
import sys 
from pathlib import Path
project_root = Path(__file__).resolve().parents[4]  # <- remonte jusqu'à la racine
sys.path.append(str(project_root))

from src.inference.caption_generator import CaptionGenerator

class InferencePipeline:
    def __init__(self, decoder_path: str, tokenizer_path: str, device=None):
        # ✅ Charger ton CaptionGenerator
        self.captioner = CaptionGenerator(decoder_path, tokenizer_path, device)

    def preprocess(self, image_bytes: bytes):
        # ✅ Chargement image depuis les bytes reçus dans l'API
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        return image

    def predict(self, image_bytes: bytes):
        # 1. Chargement et prétraitement
        image = self.preprocess(image_bytes)

        # 2. Génération de la légende
        caption, confidences = self.captioner.generate(image)

        # 3. Retour de la légende + score moyen
        return {
            "caption": caption,
            "confidence_mean": round(sum(confidences) / len(confidences), 4),
            "tokens": [
                {"word": w, "confidence": round(c, 4)}
                for w, c in zip(caption.split(), confidences)
            ]
        }