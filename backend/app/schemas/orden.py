from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class EstadoOrden(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class OrdenBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=50)
    descripcion: str = Field(..., min_length=1)
    tecnico_id: int


class OrdenCreate(OrdenBase):
    pass


class OrdenUpdate(BaseModel):
    descripcion: Optional[str] = None
    estado: Optional[EstadoOrden] = None
    observaciones: Optional[str] = None


class OrdenResponse(OrdenBase):
    id: int
    estado: EstadoOrden
    fecha_inicio: Optional[datetime]
    fecha_fin: Optional[datetime]
    observaciones: Optional[str]
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class OrdenListResponse(BaseModel):
    id: int
    codigo: str
    descripcion: str
    tecnico_id: int
    estado: EstadoOrden
    fecha_creacion: datetime

    class Config:
        from_attributes = True