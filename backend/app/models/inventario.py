from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class EstadoProducto(str, enum.Enum):
    NUEVO = "nuevo"
    USADO = "usado"
    DAÑADO = "dañado"


class Inventario(Base):
    __tablename__ = "inventarios"

    id = Column(Integer, primary_key=True, index=True)
    consecutive = Column(String(50), nullable=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    bodega_id = Column(Integer, ForeignKey("bodegas.id"), nullable=False)
    cantidad = Column(Numeric(12, 3), default=0)
    stock_minimo = Column(Integer, default=0)
    valor_unitario = Column(Numeric(14, 2), default=0)
    valor_total = Column(Numeric(14, 2), default=0)
    numero_serie = Column(String(100), nullable=True)
    estado_producto = Column(Enum(EstadoProducto), default=EstadoProducto.NUEVO)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    producto = relationship("Producto", backref="inventarios")
    bodega = relationship("Bodega", backref="inventarios")

    def __repr__(self):
        return f"<Inventario prod={self.producto_id} bodega={self.bodega_id}>"