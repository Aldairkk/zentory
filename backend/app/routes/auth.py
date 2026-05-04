from fastapi import APIRouter, Depends, Header
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.exceptions import AppException
from app.schemas.auth import LoginRequest, LoginResponse
from app.services.auth import AuthService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    try:
        service = AuthService(db)
        return service.login(request)
    except AppException as e:
        raise e


@router.get("/me")
def get_me(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    usuario = get_current_user(authorization, db)
    return {
        "usuario_id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
        "apellido": usuario.apellido,
        "rol": usuario.rol.value,
        "cargo": usuario.cargo
    }


@router.post("/logout")
def logout():
    return {"message": "Logout exitoso"}