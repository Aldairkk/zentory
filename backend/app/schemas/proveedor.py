from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class ProveedorBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=255)
    nit: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    nombre: Optional[str] = None
    nit: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    ciudad: Optional[str] = None
    direccion: Optional[str] = None
    estado: Optional[bool] = None


class ProveedorResponse(ProveedorBase):
    id: int
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class ProveedorListResponse(ProveedorBase):
    id: int
    estado: bool

    class Config:
        from_attributes = True