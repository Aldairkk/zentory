from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Text
from datetime import datetime
from app.core.database import Base
import enum


class EstadoSolicitud(str, enum.Enum):
    PENDIENTE = "pendiente"
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    CANCELADA = "cancelada"


class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    bodega_id = Column(Integer, ForeignKey("bodegas.id"), nullable=False)
    tecnico_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    estado = Column(Enum(EstadoSolicitud), default=EstadoSolicitud.PENDIENTE)
    observaciones = Column(Text, nullable=True)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)
    fecha_aprobacion = Column(DateTime, nullable=True)
    aprobador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Solicitud {self.id} estado={self.estado}>"