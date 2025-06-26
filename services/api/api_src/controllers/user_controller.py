from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from api_src.models.user_model import UserLoginResponse
from api_src.services.user_service import UserService
from api_src.repositories.user_repository import UserRepository
from api_src.database.database import Database

user_router = APIRouter()

def get_user_service():
    db = Database()
    user_repository = UserRepository(db)
    return UserService(user_repository)

@user_router.post(
    "/login",
    response_model=UserLoginResponse,
    summary="Authentification utilisateur et génération d'un token JWT",
    description=(
        "Permet à un utilisateur de se connecter en fournissant son nom d'utilisateur "
        "et son mot de passe via un formulaire (application/x-www-form-urlencoded).\n\n"
        "### Paramètres :\n"
        "- **username** : nom d'utilisateur (champ formulaire obligatoire)\n"
        "- **password** : mot de passe (champ formulaire obligatoire)\n\n"
        "### Réponse en cas de succès :\n"
        "- **access_token** : token JWT à utiliser pour accéder aux endpoints protégés\n"
        "- **token_type** : type du token (généralement 'bearer')\n"
        "- **message** : message de confirmation\n\n"
        "### En cas d'échec :\n"
        "- Retourne une erreur 400 avec un message d'erreur (ex: mauvais identifiants)."
    ),
    response_description="Token JWT d'accès et message de confirmation"
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    user_service: UserService = Depends(get_user_service)
):
    """
    Authentifie un utilisateur avec son username et mot de passe.

    Utilise OAuth2PasswordRequestForm qui attend des données en `application/x-www-form-urlencoded`
    avec les champs `username` et `password`.

    Retourne un token JWT si authentification réussie.
    """
    nom_user = form_data.username
    mdp_user = form_data.password
    result = user_service.authenticate(nom_user, mdp_user)
    
    if result.success:
        return UserLoginResponse(
            access_token=result.access_token,
            token_type=result.token_type,
            message="Connexion réussie"
        )
    else:
        raise HTTPException(status_code=400, detail=result.message)
