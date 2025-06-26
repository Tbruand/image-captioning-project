from pydantic import BaseModel
from typing import Optional

class ImagePredictionRequest(BaseModel):
    nom_fichier: str
    resultat_pred: str
    confiance_pred: float

class ImagePredictionResponse(BaseModel):
    id_image: int
    id_prediction: Optional[int] = None
    message: str
    resultat_pred: Optional[str] = None
    confiance_pred: Optional[float] = None

class FeedbackRequest(BaseModel):
    id_image: int
    feedback: int  # par exemple 1 à 4, la note donnée par l'utilisateur

