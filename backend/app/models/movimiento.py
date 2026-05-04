from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, Boolean, Float
from datetime import datetime
from app.core.database import Base
import enum


class TipoMovimiento(str, enum.Enum):
    ENTRADA = "entrada"
    INGRESO = "ingreso"
    SALIDA = "salida"
    TRANSFERENCIA = "transferencia"
    CONSUMO = "consumo"
    EGRESO = "egreso"
    ENTREGA = "entrega"
    DEVOLUCION = "devolucion"


class Movimiento(Base):
    __tablename__ = "movimientos"

    id = Column(Integer, primary_key=True, index=True)
    consecutive = Column(String(30), nullable=False, index=True)
    consecutive_item = Column(String(30), nullable=True)
    tipo = Column(Enum(TipoMovimiento), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, nullable=False, default=0)
    bodega_origen_id = Column(Integer, ForeignKey("bodegas.id"), nullable=True)
    bodega_destino_id = Column(Integer, ForeignKey("bodegas.id"), nullable=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    usuario_asignado_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    asignar_a = Column(String(100), nullable=True)
    solicitud_id = Column(Integer, nullable=True)
    orden_id = Column(Integer, nullable=True)
    valor_unitario = Column(Float, default=0)
    iva = Column(Boolean, default=False)
    serializado = Column(Boolean, default=False)
    numero_serie = Column(String(500), nullable=True)
    referencia = Column(String(100), nullable=True)
    ubicacion = Column(String(100), nullable=True)
    observaciones = Column(Text, nullable=True)
    motivo = Column(String(255), nullable=True)
    estado_producto = Column(String(50), nullable=True)
    fecha_movimiento = Column(DateTime, default=datetime.utcnow)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Movimiento {self.consecutive} tipo={self.tipo}>"