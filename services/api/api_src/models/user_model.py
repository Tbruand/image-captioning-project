from pydantic import BaseModel
from typing import Optional

class AuthResult(BaseModel):
    success: bool
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    message: Optional[str] = None


class UserLoginResponse(BaseModel):
    access_token: str 
    token_type: str 
    message: str | None = None

