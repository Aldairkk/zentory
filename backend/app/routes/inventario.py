from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException
from app.schemas.inventario import InventarioCreate, InventarioUpdate, InventarioResponse
from app.models.usuario import Usuario, RolUsuario
from app.models.inventario import EstadoProducto
from app.services.inventario import InventarioService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/inventario", tags=["Inventario"])


@router.post("/ingreso", response_model=InventarioResponse)
def crear_ingreso(data: InventarioCreate, db: Session = Depends(get_db),
                usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = InventarioService(db)
        return service.crear_ingreso(data, usuario.id)
    except AppException as e:
        raise e


@router.get("/", response_model=List[InventarioResponse])
def list_inventario(bodega_id: Optional[int] = None, skip: int = 0, limit: int = 100,
                db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    service = InventarioService(db)
    return service.get_all(skip, limit, bodega_id)


@router.get("/producto/{producto_id}")
def get_inventario_producto(producto_id: int, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    service = InventarioService(db)
    return service.get_by_producto(producto_id)


@router.get("/bodega/{bodega_id}")
def get_inventario_bodega(bodega_id: int, db: Session = Depends(get_db),
                       usuario: Usuario = Depends(get_current_user)):
    service = InventarioService(db)
    return service.get_by_bodega(bodega_id)


@router.get("/resumen")
def get_resumen_inventario(bodega_id: Optional[int] = None, db: Session = Depends(get_db),
                        usuario: Usuario = Depends(get_current_user)):
    service = InventarioService(db)
    return service.get_resumen_inventario(bodega_id)


@router.get("/stock/{producto_id}")
def get_stock_producto(producto_id: int, db: Session = Depends(get_db),
                       usuario: Usuario = Depends(get_current_user)):
    service = InventarioService(db)
    stock = service.get_stock_total(producto_id)
    return {"producto_id": producto_id, "stock_total": stock}