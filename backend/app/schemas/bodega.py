from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class BodegaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=20)
    nombre: str = Field(..., min_length=1, max_length=150)
    ciudad: Optional[str] = None
    direccion: Optional[str] = None


class BodegaCreate(BodegaBase):
    pass


class BodegaUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[bool] = None


class BodegaResponse(BodegaBase):
    id: int
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class BodegaListResponse(BodegaBase):
    id: int
    estado: bool

    class Config:
        from_attributes = True