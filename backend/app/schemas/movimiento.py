from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal
from enum import Enum


class TipoMovimiento(str, Enum):
    ENTRADA = "entrada"
    INGRESO = "ingreso"
    SALIDA = "salida"
    TRANSFERENCIA = "transferencia"
    CONSUMO = "consumo"
    Egreso = "egreso"
    ENTREGA = "entrega"
    DEVOLUCION = "devolucion"


class MovimientoBase(BaseModel):
    tipo: TipoMovimiento
    producto_id: int
    cantidad: int = Field(..., gt=0)
    valor_unitario: Optional[float] = 0
    bodega_origen_id: Optional[int] = None
    bodega_destino_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    tecnico_id: Optional[int] = None
    solicitud_id: Optional[int] = None
    orden_id: Optional[int] = None
    iva: Optional[bool] = False
    serializado: Optional[bool] = False
    numero_serie: Optional[str] = None
    referencia: Optional[str] = None
    ubicacion: Optional[str] = None
    observaciones: Optional[str] = None
    estado_producto: Optional[str] = None
    motivo: Optional[str] = None
    consecutive: Optional[str] = None
    consecutive_item: Optional[str] = None
    asignar_a: Optional[str] = None
    usuario_asignado_id: Optional[int] = None


class MovimientoCreate(MovimientoBase):
    pass


class MovimientoUpdate(BaseModel):
    observaciones: Optional[str] = None


class MovimientoResponse(MovimientoBase):
    id: int
    consecutive: str
    consecutive_item: Optional[str] = None
    bodega_origen_id: Optional[int] = None
    bodega_destino_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    usuario_id: int
    valor_unitario: Optional[float] = 0
    iva: Optional[bool] = False
    serializado: Optional[bool] = False
    numero_serie: Optional[str] = None
    referencia: Optional[str] = None
    ubicacion: Optional[str] = None
    observaciones: Optional[str] = None
    asignar_a: Optional[str] = None
    usuario_asignado_id: Optional[int] = None
    fecha_movimiento: datetime
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class MovimientoListResponse(MovimientoBase):
    id: int
    consecutive: str
    consecutive_item: Optional[str] = None
    tipo: TipoMovimiento
    producto_id: int
    cantidad: int
    bodega_destino_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    valor_unitario: Optional[float] = 0
    iva: Optional[bool] = False
    serializado: Optional[bool] = False
    numero_serie: Optional[str] = None
    referencia: Optional[str] = None
    ubicacion: Optional[str] = None
    observaciones: Optional[str] = None
    asignar_a: Optional[str] = None
    usuario_asignado_id: Optional[int] = None
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class MovimientoListResponse(BaseModel):
    id: int
    consecutive: str
    tipo: TipoMovimiento
    producto_id: int
    cantidad: int
    bodega_destino_id: Optional[int] = None
    proveedor_id: Optional[int] = None
    valor_unitario: Optional[float] = 0
    iva: Optional[bool] = False
    serializado: Optional[bool] = False
    numero_serie: Optional[str] = None
    referencia: Optional[str] = None
    ubicacion: Optional[str] = None
    observaciones: Optional[str] = None
    fecha_creacion: datetime

    class Config:
        from_attributes = True