from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException
from app.schemas.orden import OrdenCreate, OrdenUpdate, OrdenResponse
from app.models.usuario import Usuario, RolUsuario
from app.models.orden import EstadoOrden
from app.services.orden import OrdenService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/ordenes", tags=["Ordenes"])


@router.post("/", response_model=OrdenResponse)
def crear_orden(data: OrdenCreate, db: Session = Depends(get_db),
               usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.TECNICO, RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = OrdenService(db)
        return service.create(data)
    except AppException as e:
        raise e


@router.get("/", response_model=List[OrdenResponse])
def list_ordenes(estado: Optional[EstadoOrden] = None, tecnico_id: Optional[int] = None,
                skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                usuario: Usuario = Depends(get_current_user)):
    service = OrdenService(db)
    return service.get_all(skip, limit, estado, tecnico_id)


@router.get("/{orden_id}", response_model=OrdenResponse)
def get_orden(orden_id: int, db: Session = Depends(get_db),
             usuario: Usuario = Depends(get_current_user)):
    service = OrdenService(db)
    result = service.get_by_id(orden_id)
    if not result:
        raise AppException("Orden no encontrada")
    return result


@router.put("/{orden_id}", response_model=OrdenResponse)
def update_orden(orden_id: int, data: OrdenUpdate, db: Session = Depends(get_db),
                usuario: Usuario = Depends(get_current_user)):
    try:
        service = OrdenService(db)
        return service.update(orden_id, data)
    except AppException as e:
        raise e


@router.put("/{orden_id}/iniciar", response_model=OrdenResponse)
def iniciar_orden(orden_id: int, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    try:
        service = OrdenService(db)
        return service.iniciar(orden_id)
    except AppException as e:
        raise e


@router.put("/{orden_id}/completar", response_model=OrdenResponse)
def completar_orden(orden_id: int, observaciones: str = None, db: Session = Depends(get_db),
                  usuario: Usuario = Depends(get_current_user)):
    try:
        service = OrdenService(db)
        return service.completar(orden_id, observaciones)
    except AppException as e:
        raise e


@router.put("/{orden_id}/cancelar", response_model=OrdenResponse)
def cancelar_orden(orden_id: int, observaciones: str = None, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = OrdenService(db)
        return service.cancelar(orden_id, observaciones)
    except AppException as e:
        raise e