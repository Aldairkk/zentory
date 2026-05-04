from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoSolicitud(str, Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    CANCELADA = "cancelada"


class SolicitudBase(BaseModel):
    producto_id: int
    bodega_id: int
    cantidad: int = Field(..., gt=0)
    observaciones: Optional[str] = None


class SolicitudCreate(SolicitudBase):
    tecnico_id: int


class SolicitudUpdate(BaseModel):
    estado: Optional[EstadoSolicitud] = None
    observaciones: Optional[str] = None
    aprobador_id: Optional[int] = None


class SolicitudResponse(SolicitudBase):
    id: int
    tecnico_id: int
    estado: EstadoSolicitud
    fecha_solicitud: datetime
    fecha_aprobacion: Optional[datetime]
    aprobador_id: Optional[int]
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class SolicitudListResponse(BaseModel):
    id: int
    producto_id: int
    bodega_id: int
    tecnico_id: int
    cantidad: int
    estado: EstadoSolicitud
    fecha_solicitud: datetime

    class Config:
        from_attributes = True