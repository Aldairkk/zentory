from sqlalchemy import Column, Integer, String, Boolean, Enum, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base
import enum


class RolUsuario(str, enum.Enum):
    ADMIN = "admin"
    OPERADOR = "operador"
    GERENCIA = "gerencia"
    TECNICO = "tecnico"
    EMPLEADO = "empleado"
    SEMIADMIN = "semiadmin"
    SUPERVISOR = "supervisor"


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    cargo = Column(String(100), nullable=True)
    rol = Column(Enum(RolUsuario), nullable=False, default=RolUsuario.TECNICO)
    estado = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    fecha_actualizacion = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Usuario {self.email} rol={self.rol}>"