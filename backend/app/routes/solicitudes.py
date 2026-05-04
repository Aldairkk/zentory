from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException
from app.schemas.solicitud import SolicitudCreate, SolicitudUpdate, SolicitudResponse
from app.models.usuario import Usuario, RolUsuario
from app.models.solicitud import EstadoSolicitud
from app.services.solicitud import SolicitudService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes"])


@router.post("/", response_model=SolicitudResponse)
def crear_solicitud(data: SolicitudCreate, db: Session = Depends(get_db),
                   usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.TECNICO, RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = SolicitudService(db)
        return service.crear(data, usuario.id)
    except AppException as e:
        raise e


@router.get("/", response_model=List[SolicitudResponse])
def list_solicitudes(estado: Optional[EstadoSolicitud] = None, tecnico_id: Optional[int] = None,
                  skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
                  usuario: Usuario = Depends(get_current_user)):
    service = SolicitudService(db)
    return service.get_all(skip, limit, estado, tecnico_id)


@router.get("/pendientes", response_model=List[SolicitudResponse])
def list_solicitudes_pendientes(skip: int = 0, limit: int = 100,
                             db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    service = SolicitudService(db)
    return service.get_pendientes(skip, limit)


@router.get("/{solicitud_id}", response_model=SolicitudResponse)
def get_solicitud(solicitud_id: int, db: Session = Depends(get_db),
                 usuario: Usuario = Depends(get_current_user)):
    service = SolicitudService(db)
    result = service.get_by_id(solicitud_id)
    if not result:
        raise AppException("Solicitud no encontrada")
    return result


@router.put("/{solicitud_id}/aprobar", response_model=SolicitudResponse)
def aprobar_solicitud(solicitud_id: int, db: Session = Depends(get_db),
                    usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = SolicitudService(db)
        return service.aprobar(solicitud_id, usuario.id)
    except AppException as e:
        raise e


@router.put("/{solicitud_id}/rechazar", response_model=SolicitudResponse)
def rechazar_solicitud(solicitud_id: int, db: Session = Depends(get_db),
                  usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = SolicitudService(db)
        return service.rechazar(solicitud_id, usuario.id)
    except AppException as e:
        raise e


@router.put("/{solicitud_id}/cancelar", response_model=SolicitudResponse)
def cancelar_solicitud(solicitud_id: int, db: Session = Depends(get_db),
                      usuario: Usuario = Depends(get_current_user)):
    try:
        service = SolicitudService(db)
        return service.cancelar(solicitud_id, usuario.id)
    except AppException as e:
        raise e