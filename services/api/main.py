from fastapi import FastAPI
from api_src.controllers.user_controller import user_router
from api_src.controllers.image_controller import image_router

app = FastAPI(
    title="API : Annotation Automatique des Images",
    description="API sécurisée avec authentification JWT pour gérer les utilisateurs, l'annotation des images et les prédictions.",
    version="1.0.0"
)

# Inclusion des routes
app.include_router(user_router, tags=["Utilisateur"])
app.include_router(image_router, tags=["Prédiction"])
