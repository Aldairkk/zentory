from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate, ProveedorResponse
from app.models.usuario import Usuario, RolUsuario
from app.services.proveedor import ProveedorService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/proveedores", tags=["Proveedores"])


@router.post("/", response_model=ProveedorResponse)
def create_proveedor(data: ProveedorCreate, db: Session = Depends(get_db), 
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = ProveedorService(db)
        return service.create(data)
    except AppException as e:
        raise e


@router.get("/", response_model=List[ProveedorResponse])
def list_proveedores(skip: int = 0, limit: int = 100, estado: bool = True,
                   db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    service = ProveedorService(db)
    return service.get_all(skip, limit, estado)


@router.get("/{proveedor_id}", response_model=ProveedorResponse)
def get_proveedor(proveedor_id: int, db: Session = Depends(get_db),
                usuario: Usuario = Depends(get_current_user)):
    service = ProveedorService(db)
    result = service.get_by_id(proveedor_id)
    if not result:
        raise AppException("Proveedor no encontrado")
    return result


@router.put("/{proveedor_id}", response_model=ProveedorResponse)
def update_proveedor(proveedor_id: int, data: ProveedorUpdate, db: Session = Depends(get_db),
                  usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = ProveedorService(db)
        return service.update(proveedor_id, data)
    except AppException as e:
        raise e


@router.delete("/{proveedor_id}")
def delete_proveedor(proveedor_id: int, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol != RolUsuario.ADMIN:
        raise UnauthorizedException("Solo administradores pueden eliminar")
    
    try:
        service = ProveedorService(db)
        service.delete(proveedor_id)
        return {"message": "Proveedor eliminado"}
    except AppException as e:
        raise e