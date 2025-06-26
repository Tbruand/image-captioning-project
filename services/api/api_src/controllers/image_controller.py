from fastapi import APIRouter, HTTPException, Depends, Response, UploadFile, File
from typing import Optional
from api_src.models.image_model import ImagePredictionResponse, FeedbackRequest
from api_src.services.image_service import ImageService
from api_src.repositories.image_repository import ImageRepository
from api_src.repositories.user_repository import UserRepository
from api_src.services.user_service import UserService
from api_src.database.database import Database
from api_src.auth.dependencies import get_current_user

image_router = APIRouter()

def get_db():
    return Database()

def get_image_repository(db: Database = Depends(get_db)):
    return ImageRepository(db)

def get_user_repository(db: Database = Depends(get_db)):
    return UserRepository(db)

def get_image_service(image_repo: ImageRepository = Depends(get_image_repository)):
    return ImageService(image_repo)

def get_user_service(user_repo: UserRepository = Depends(get_user_repository)):
    return UserService(user_repo)


@image_router.post(
    "/upload_image",
    response_model=ImagePredictionResponse,
    summary="Upload d'une image et obtention d'une prédiction",
    description=(
        "Endpoint pour qu'un utilisateur authentifié puisse envoyer une image.\n"
        "Le serveur sauvegarde l'image, lance la prédiction, et renvoie le résultat.\n\n"
        "### Paramètres :\n"
        "- **file** : fichier image (UploadFile) envoyé dans la requête multipart/form-data.\n"
        "- **current_user** : utilisateur connecté (inféré via dépendance d'authentification).\n\n"
        "### Retourne :\n"
        "- **id_image** : identifiant unique de l'image en base.\n"
        "- **id_prediction** : identifiant de la prédiction associée.\n"
        "- **message** : message de confirmation.\n"
        "- **resultat_pred** : description/textuelle prédite pour l'image.\n"
        "- **confiance_pred** : confiance (score) de la prédiction."
    ),
    response_description="Informations de l'image et prédiction calculée"
)
async def upload_image(
    response: Response,
    file: UploadFile = File(..., description="Image à uploader"),
    current_user: dict = Depends(get_current_user),
    image_service: ImageService = Depends(get_image_service)
):
    # Anti-cache HTTP headers pour s'assurer que la réponse n'est pas mise en cache par le client
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    # Récupérer l'id de l'utilisateur connecté (inféré via token JWT ou session)
    id_user = current_user.get("id_user")
    if id_user is None:
        raise HTTPException(status_code=400, detail="Utilisateur introuvable")

    nom_fichier = file.filename  # nom original du fichier uploadé
    content = await file.read()  # contenu binaire de l'image

    # Appel du service qui sauvegarde l'image, effectue la prédiction et stocke les données en base
    # monitor_pred = 0 : pas encore de feedback utilisateur
    result = image_service.save_image_and_predict(
        nom_fichier=nom_fichier,
        id_user=id_user,
        file_bytes=content,
        monitor_pred=0
    )

    if not result["success"]:
        # En cas d'erreur d'insertion ou de prédiction, on retourne une erreur HTTP 400
        raise HTTPException(status_code=400, detail=result["message"])

    # Retourner un modèle Pydantic validé avec les infos pertinentes pour le client
    return ImagePredictionResponse(
        id_image=result["id_image"],
        id_prediction=result["id_prediction"],
        message="Image enregistrée et prédiction calculée",
        resultat_pred=result["resultat_pred"],
        confiance_pred=result["confiance_pred"]
    )


@image_router.post(
    "/send_feedback",
    summary="Envoi du feedback utilisateur sur une prédiction",
    description=(
        "Endpoint pour qu'un utilisateur authentifié puisse envoyer une note (1 à 4) "
        "sur la qualité ou la pertinence de la prédiction reçue.\n\n"
        "### Paramètres :\n"
        "- **feedback_data** : JSON contenant :\n"
        "  - **id_image** (int) : identifiant de l'image pour laquelle on donne un feedback\n"
        "  - **feedback** (int) : note de 1 (mauvais) à 4 (excellent)\n"
        "- **current_user** : utilisateur connecté (authentifié)\n\n"
        "### Comportement :\n"
        "- Met à jour la colonne `monitor_pred` dans la table `Prediction` pour la prédiction liée à l'image.\n"
        "- Retourne un message de succès ou une erreur si la mise à jour échoue."
    ),
    response_description="Confirmation de la sauvegarde du feedback"
)
def send_feedback(
    feedback_data: FeedbackRequest,
    current_user: dict = Depends(get_current_user),
    image_service: ImageService = Depends(get_image_service)
):
    # Récupérer l'id de l'utilisateur connecté
    id_user = current_user.get("id_user")
    if id_user is None:
        raise HTTPException(status_code=400, detail="Utilisateur introuvable")

    # Appeler la fonction du service pour sauvegarder le feedback
    result = image_service.save_feedback(
        id_image=feedback_data.id_image,
        id_user=id_user,
        monitor_pred=feedback_data.feedback
    )

    if not result["success"]:
        # Retourner une erreur HTTP si la sauvegarde échoue
        raise HTTPException(status_code=400, detail=result["message"])

    # Retourner un message de succès au client
    return {"success": True, "message": "Feedback enregistré avec succès"}


"""
NOTE IMPORTANTE POUR LE FRONTEND / CLIENT:

- Lors du POST /upload_image, la réponse contient `id_image` et `id_prediction`.
- Ces IDs doivent être conservés côté client (ex : dans l'état de l'application).
- Quand l'utilisateur donne son feedback (note 1-4), il faut envoyer un POST /send_feedback
  avec un JSON contenant `id_image` et `feedback` (la note donnée).
- Cela garantit que le feedback est associé à la bonne image et prédiction en base.

C'est la manière classique et propre de gérer la relation entre images, prédictions, et feedback utilisateur.
"""
