from fastapi import FastAPI
import sys
from pathlib import Path

# Ajout du chemin 'services/api/' au PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parent))

from api_src.controllers.user_controller import user_router
from api_src.controllers.image_controller import image_router
from fastapi.middleware.cors import CORSMiddleware  # ✅

app = FastAPI(
    title="API : Annotation Automatique des Images",
    description="API sécurisée avec authentification JWT pour gérer les utilisateurs, l'annotation des images et les prédictions.",
    version="1.0.0"
)

# ✅ CORS pour autoriser le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(user_router, tags=["Utilisateur"])
app.include_router(image_router, tags=["Prédiction"])