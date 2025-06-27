from pydantic import BaseModel

class FeedbackRequest(BaseModel):
    id_image: int
    feedback: int  # par exemple 1 à 4, la note donnée par l'utilisateur
