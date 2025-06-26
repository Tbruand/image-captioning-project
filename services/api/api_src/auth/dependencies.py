from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()  # Charge les variables d'environnement depuis .env

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# scopes={} pour dire qu’il n’y a pas de scopes obligatoires
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", scopes={})

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        id_user: int = payload.get("id_user")  

        if username is None or id_user is None:
            raise credentials_exception
        
        # Retourner un dict avec username et id_user
        return {"username": username, "id_user": id_user}
    
    except JWTError:
        raise credentials_exception