from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text, Float
from datetime import datetime
from app.core.database import Base
import enum


class EstadoOrden(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"


class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=False, index=True)
    tipo = Column(String(20), default="trabajo")  # 'compra' or 'trabajo'
    descripcion = Column(Text, nullable=True)
    proveedor_id = Column(Integer, ForeignKey("proveedores.id"), nullable=True)
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_orden = Column(DateTime, nullable=True)
    fecha_inicio = Column(DateTime, nullable=True)
    fecha_fin = Column(DateTime, nullable=True)
    total = Column(Float, default=0)
    estado = Column(Enum(EstadoOrden), default=EstadoOrden.PENDIENTE)
    observaciones = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Orden {self.codigo} estado={self.estado}>"