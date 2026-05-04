from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, Text, Enum
from datetime import datetime
from app.core.database import Base
import enum


class Proveedor(Base):
    __tablename__ = "proveedores"

    id = Column(Integer, primary_key=True, index=True)
    nit = Column(String(20), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    email = Column(String(100), nullable=True)
    telefono = Column(String(30), nullable=True)
    ciudad = Column(String(100), nullable=True)
    direccion = Column(String(500), nullable=True)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Proveedor {self.nit}: {self.nombre}>"