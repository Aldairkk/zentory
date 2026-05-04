from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException
from app.schemas.bodega import BodegaCreate, BodegaUpdate, BodegaResponse
from app.models.usuario import Usuario, RolUsuario
from app.services.bodega import BodegaService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/bodegas", tags=["Bodegas"])


@router.post("/", response_model=BodegaResponse)
def create_bodega(data: BodegaCreate, db: Session = Depends(get_db), 
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = BodegaService(db)
        return service.create(data)
    except AppException as e:
        raise e


@router.get("/", response_model=List[BodegaResponse])
def list_bodegas(skip: int = 0, limit: int = 100, estado: Optional[bool] = None,
                db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    service = BodegaService(db)
    return service.get_all(skip, limit, estado)


@router.get("/{bodega_id}", response_model=BodegaResponse)
def get_bodega(bodega_id: int, db: Session = Depends(get_db),
              usuario: Usuario = Depends(get_current_user)):
    service = BodegaService(db)
    result = service.get_by_id(bodega_id)
    if not result:
        raise AppException("Bodega no encontrada")
    return result


@router.put("/{bodega_id}", response_model=BodegaResponse)
def update_bodega(bodega_id: int, data: BodegaUpdate, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = BodegaService(db)
        return service.update(bodega_id, data)
    except AppException as e:
        raise e


@router.delete("/{bodega_id}")
def delete_bodega(bodega_id: int, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol != RolUsuario.ADMIN:
        raise UnauthorizedException("Solo administradores pueden eliminar")
    
    try:
        service = BodegaService(db)
        service.delete(bodega_id)
        return {"message": "Bodega eliminada"}
    except AppException as e:
        raise e