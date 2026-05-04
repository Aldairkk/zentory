from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException, NotFoundException
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate, UsuarioResponse
from app.models import Usuario, RolUsuario
from app.services.usuario import UsuarioService
from app.services.auth import AuthService

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization or not authorization.startswith("Bearer "):
        raise UnauthorizedException("Token requerido")
    
    token = authorization.replace("Bearer ", "")
    try:
        from app.core.security import decode_token
        payload = decode_token(token)
        usuario_id = int(payload.get("sub"))
        service = UsuarioService(db)
        usuario = service.get_by_id(usuario_id)
        if not usuario:
            raise UnauthorizedException("Usuario no encontrado")
        return usuario
    except Exception as e:
        raise UnauthorizedException("Token inválido")


def require_admin(usuario: Usuario = Depends(get_current_user)):
    if usuario.rol != RolUsuario.ADMIN:
        raise UnauthorizedException("Solo administradores")
    return usuario


@router.post("/", response_model=UsuarioResponse, dependencies=[Depends(require_admin)])
def create_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    try:
        service = UsuarioService(db)
        return service.create(data)
    except AppException as e:
        raise e


@router.get("/", response_model=List[UsuarioResponse])
def list_usuarios(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), 
               usuario: Usuario = Depends(get_current_user)):
    service = UsuarioService(db)
    return service.get_all(skip, limit)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def get_usuario(usuario_id: int, db: Session = Depends(get_db), 
               usuario: Usuario = Depends(get_current_user)):
    service = UsuarioService(db)
    result = service.get_by_id(usuario_id)
    if not result:
        raise NotFoundException("Usuario no encontrado")
    return result


@router.put("/{usuario_id}", response_model=UsuarioResponse)
def update_usuario(usuario_id: int, data: UsuarioUpdate, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol != RolUsuario.ADMIN and usuario.id != usuario_id:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = UsuarioService(db)
        return service.update(usuario_id, data)
    except AppException as e:
        raise e


@router.delete("/{usuario_id}", dependencies=[Depends(require_admin)])
def delete_usuario(usuario_id: int, db: Session = Depends(get_db)):
    try:
        service = UsuarioService(db)
        service.delete(usuario_id)
        return {"message": "Usuario eliminado"}
    except AppException as e:
        raise e