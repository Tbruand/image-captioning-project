from passlib.context import CryptContext

# On définit le contexte de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pour hasher un mot de passe
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Pour vérifier un mot de passe en clair vs un mot de passe hashé
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
