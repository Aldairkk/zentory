from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class RolUsuario(str, Enum):
    ADMIN = "admin"
    OPERADOR = "operador"
    GERENCIA = "gerencia"
    TECNICO = "tecnico"
    EMPLEADO = "empleado"


class UsuarioBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    cargo: Optional[str] = None
    rol: RolUsuario = RolUsuario.EMPLEADO


class UsuarioCreate(UsuarioBase):
    password: str = Field(..., min_length=6)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    email: Optional[EmailStr] = None
    cargo: Optional[str] = None
    rol: Optional[RolUsuario] = None
    estado: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class UsuarioListResponse(UsuarioBase):
    id: int
    estado: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True