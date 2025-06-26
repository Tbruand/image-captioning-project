from api_src.repositories.user_repository import UserRepository
from api_src.models.user_model import AuthResult
from api_src.auth.security import verify_password
from api_src.auth.jwt_manager import create_access_token 

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def authenticate(self, nom_user: str, mdp_user: str) -> AuthResult:
        hashed_password = self.user_repository.get_password_hash_by_username(nom_user)
        if not hashed_password:
            return AuthResult(success=False, message="Utilisateur ou mot de passe incorrect")

        if verify_password(mdp_user, hashed_password):
            id_user = self.get_id_by_username(nom_user)
            if id_user is None:
                return AuthResult(success=False, message="Utilisateur introuvable")

            access_token = create_access_token(data={"sub": nom_user, "id_user": id_user})
            return AuthResult(success=True, access_token=access_token, token_type="bearer")

        else:
            return AuthResult(success=False, message="Utilisateur ou mot de passe incorrect")
    def get_id_by_username(self, nom_user: str) -> int | None:
        return self.user_repository.get_id_by_username(nom_user)