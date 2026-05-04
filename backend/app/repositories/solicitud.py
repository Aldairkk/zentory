from sqlalchemy.orm import Session
from app.models.solicitud import Solicitud, EstadoSolicitud
from app.core.exceptions import NotFoundException
from typing import Optional, List
from datetime import datetime


class SolicitudRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Solicitud]:
        return self.db.query(Solicitud).filter(Solicitud.id == id).first()

    def get_all(self, skip: int = 0, limit: int = 100, estado: Optional[EstadoSolicitud] = None,
               tecnico_id: Optional[int] = None) -> List[Solicitud]:
        query = self.db.query(Solicitud)
        if estado:
            query = query.filter(Solicitud.estado == estado)
        if tecnico_id:
            query = query.filter(Solicitud.tecnico_id == tecnico_id)
        return query.order_by(Solicitud.fecha_solicitud.desc()).offset(skip).limit(limit).all()

    def get_pendientes(self, skip: int = 0, limit: int = 100) -> List[Solicitud]:
        return self.db.query(Solicitud).filter(
            Solicitud.estado == EstadoSolicitud.PENDIENTE
        ).order_by(Solicitud.fecha_solicitud.desc()).offset(skip).limit(limit).all()

    def create(self, producto_id: int, bodega_id: int, tecnico_id: int, cantidad: int,
            observaciones: Optional[str] = None) -> Solicitud:
        solicitud = Solicitud(
            producto_id=producto_id,
            bodega_id=bodega_id,
            tecnico_id=tecnico_id,
            cantidad=cantidad,
            observaciones=observaciones,
            estado=EstadoSolicitud.PENDIENTE
        )
        self.db.add(solicitud)
        self.db.commit()
        self.db.refresh(solicitud)
        return solicitud

    def aprobar(self, id: int, aprobador_id: int) -> Solicitud:
        solicitud = self.get_by_id(id)
        if not solicitud:
            raise NotFoundException(f"Solicitud con id {id} no encontrada")
        
        if solicitud.estado != EstadoSolicitud.PENDIENTE:
            raise NotFoundException(f"La solicitud ya no está pendiente")
        
        solicitud.estado = EstadoSolicitud.APROBADA
        solicitud.fecha_aprobacion = datetime.utcnow()
        solicitud.aprobador_id = aprobador_id
        self.db.commit()
        self.db.refresh(solicitud)
        return solicitud

    def rechazar(self, id: int, aprobador_id: int) -> Solicitud:
        solicitud = self.get_by_id(id)
        if not solicitud:
            raise NotFoundException(f"Solicitud con id {id} no encontrada")
        
        if solicitud.estado != EstadoSolicitud.PENDIENTE:
            raise NotFoundException(f"La solicitud ya no está pendiente")
        
        solicitud.estado = EstadoSolicitud.RECHAZADA
        solicitud.fecha_aprobacion = datetime.utcnow()
        solicitud.aprobador_id = aprobador_id
        self.db.commit()
        self.db.refresh(solicitud)
        return solicitud

    def cancelar(self, id: int) -> Solicitud:
        solicitud = self.get_by_id(id)
        if not solicitud:
            raise NotFoundException(f"Solicitud con id {id} no encontrada")
        
        if solicitud.estado != EstadoSolicitud.PENDIENTE:
            raise NotFoundException(f"No se puede cancelar una solicitud procesada")
        
        solicitud.estado = EstadoSolicitud.CANCELADA
        self.db.commit()
        self.db.refresh(solicitud)
        return solicitud