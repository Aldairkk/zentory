from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class EstadoProducto(str, Enum):
    NUEVO = "nuevo"
    USADO = "usado"
    DAÑADO = "dañado"


class InventarioBase(BaseModel):
    producto_id: int
    bodega_id: int
    consecutive: Optional[str] = None
    cantidad: Decimal = Field(..., ge=0)
    valor_unitario: Decimal = Field(..., ge=0)
    estado_producto: EstadoProducto = EstadoProducto.NUEVO
    numero_serie: Optional[str] = None


class InventarioCreate(BaseModel):
    producto_id: int
    bodega_id: int
    consecutive: Optional[str] = None
    cantidad: Decimal = Field(..., ge=0)
    valor_unitario: Decimal = Field(..., ge=0)
    estado_producto: EstadoProducto = EstadoProducto.NUEVO
    numero_serie: Optional[str] = None


class InventarioUpdate(BaseModel):
    consecutive: Optional[str] = None
    cantidad: Optional[Decimal] = Field(default=None, ge=0)
    valor_unitario: Optional[Decimal] = Field(default=None, ge=0)
    estado_producto: Optional[EstadoProducto] = None
    numero_serie: Optional[str] = None


class InventarioResponse(InventarioBase):
    id: int
    valor_total: Decimal
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class InventarioListResponse(BaseModel):
    id: int
    producto_id: int
    bodega_id: int
    cantidad: Decimal
    valor_unitario: Decimal
    valor_total: Decimal
    estado_producto: EstadoProducto

    class Config:
        from_attributes = True


class InventarioDetalleResponse(BaseModel):
    producto_codigo: str
    producto_nombre: str
    bodega_codigo: str
    bodega_nombre: str
    cantidad: Decimal
    valor_unitario: Decimal
    valor_total: Decimal
    estado_producto: EstadoProducto

    class Config:
        from_attributes = True