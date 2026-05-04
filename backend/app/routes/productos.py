from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from app.models.usuario import Usuario, RolUsuario
from app.services.producto import ProductoService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoResponse)
def create_producto(data: ProductoCreate, db: Session = Depends(get_db), 
                usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = ProductoService(db)
        return service.create(data)
    except AppException as e:
        raise e


@router.get("/", response_model=List[ProductoResponse])
def list_productos(skip: int = 0, limit: int = 100, estado: bool = True,
               db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    service = ProductoService(db)
    return service.get_all(skip, limit, estado)


@router.get("/{producto_id}", response_model=ProductoResponse)
def get_producto(producto_id: int, db: Session = Depends(get_db),
              usuario: Usuario = Depends(get_current_user)):
    service = ProductoService(db)
    result = service.get_by_id(producto_id)
    if not result:
        raise AppException("Producto no encontrado")
    return result


@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(producto_id: int, data: ProductoUpdate, db: Session = Depends(get_db),
                  usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = ProductoService(db)
        return service.update(producto_id, data)
    except AppException as e:
        raise e


@router.delete("/{producto_id}")
def delete_producto(producto_id: int, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol != RolUsuario.ADMIN:
        raise UnauthorizedException("Solo administradores pueden eliminar")
    
    try:
        service = ProductoService(db)
        service.delete(producto_id)
        return {"message": "Producto eliminado"}
    except AppException as e:
        raise e