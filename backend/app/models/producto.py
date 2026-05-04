from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class TipoProducto(str, enum.Enum):
    SERIALIZADO = "serializado"
    NO_SERIALIZADO = "no_serializado"


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(30), unique=True, nullable=False, index=True)
    nombre = Column(String(200), nullable=False)
    descripcion = Column(String(500), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    tipo = Column(Enum(TipoProducto), default=TipoProducto.NO_SERIALIZADO)
    serializado = Column(Boolean, default=False)
    precio = Column(Float, default=0)
    unidad_medida = Column(String(20), default="und")
    cantidad_minima = Column(Integer, default=0)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    categoria = relationship("Categoria", backref="productos")
    proveedor = relationship("Proveedor", backref="productos")

    def __repr__(self):
        return f"<Producto {self.codigo}: {self.nombre}>"