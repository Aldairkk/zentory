from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class TipoProducto(str, Enum):
    SERIALIZADO = "serializado"
    NO_SERIALIZADO = "no_serializado"


class EstadoProducto(str, Enum):
    NUEVO = "nuevo"
    USADO = "usado"
    DAÑADO = "dañado"


class ProductoBase(BaseModel):
    codigo: str = Field(..., min_length=1, max_length=30)
    nombre: str = Field(..., min_length=1, max_length=200)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    serializado: bool = False
    precio: float = Field(default=0, ge=0)
    unidad_medida: str = Field(default="und")
    cantidad_minima: int = Field(default=0, ge=0)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    codigo: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    serializado: Optional[bool] = None
    precio: Optional[float] = None
    unidad_medida: Optional[str] = None
    cantidad_minima: Optional[int] = None
    estado: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: int
    estado: bool
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True