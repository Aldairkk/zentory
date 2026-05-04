from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CategoriaBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=30)
    nombre: str = Field(..., min_length=1, max_length=100)
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[bool] = None


class CategoriaResponse(CategoriaBase):
    id: int
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True