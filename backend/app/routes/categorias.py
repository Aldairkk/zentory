from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from app.models.usuario import Usuario, RolUsuario
from app.services.categoria import CategoriaService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/categorias", tags=["Categorías"])


@router.post("/", response_model=CategoriaResponse)
def create_categoria(data: CategoriaCreate, db: Session = Depends(get_db), 
                usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = CategoriaService(db)
        return service.create(data)
    except AppException as e:
        raise e


@router.get("/", response_model=List[CategoriaResponse])
def list_categorias(skip: int = 0, limit: int = 100, estado: bool = True,
               db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    service = CategoriaService(db)
    return service.get_all(skip, limit, estado)


@router.get("/{categoria_id}", response_model=CategoriaResponse)
def get_categoria(categoria_id: int, db: Session = Depends(get_db),
              usuario: Usuario = Depends(get_current_user)):
    service = CategoriaService(db)
    result = service.get_by_id(categoria_id)
    if not result:
        raise AppException("Categoría no encontrada")
    return result


@router.put("/{categoria_id}", response_model=CategoriaResponse)
def update_categoria(categoria_id: int, data: CategoriaUpdate, db: Session = Depends(get_db),
                  usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = CategoriaService(db)
        return service.update(categoria_id, data)
    except AppException as e:
        raise e


@router.delete("/{categoria_id}")
def delete_categoria(categoria_id: int, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol != RolUsuario.ADMIN:
        raise UnauthorizedException("Solo administradores pueden eliminar")
    
    try:
        service = CategoriaService(db)
        service.delete(categoria_id)
        return {"message": "Categoría eliminada"}
    except AppException as e:
        raise e