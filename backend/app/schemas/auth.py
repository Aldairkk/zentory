from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    usuario_id: int
    email: str
    nombre: str
    rol: str


class TokenData(BaseModel):
    usuario_id: Optional[int] = None
    email: Optional[str] = None
    rol: Optional[str] = None