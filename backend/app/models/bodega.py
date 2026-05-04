from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from datetime import datetime
from app.core.database import Base


class Bodega(Base):
    __tablename__ = "bodegas"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(20), unique=True, nullable=False, index=True)
    nombre = Column(String(150), nullable=False)
    ciudad = Column(String(100), nullable=True)
    direccion = Column(String(500), nullable=True)
    es_principal = Column(Boolean, default=False)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Bodega {self.codigo}: {self.nombre}>"