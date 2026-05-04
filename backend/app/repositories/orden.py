from sqlalchemy.orm import Session
from app.models.orden import Orden, EstadoOrden
from app.core.exceptions import NotFoundException, DuplicateException
from typing import Optional, List
from datetime import datetime


class OrdenRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Orden]:
        return self.db.query(Orden).filter(Orden.id == id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Orden]:
        return self.db.query(Orden).filter(Orden.codigo == codigo).first()

    def get_all(self, skip: int = 0, limit: int = 100, estado: Optional[EstadoOrden] = None,
               tecnico_id: Optional[int] = None) -> List[Orden]:
        query = self.db.query(Orden)
        if estado:
            query = query.filter(Orden.estado == estado)
        if tecnico_id:
            query = query.filter(Orden.tecnico_id == tecnico_id)
        return query.order_by(Orden.fecha_creacion.desc()).offset(skip).limit(limit).all()

    def create(self, codigo: str, descripcion: str, tecnico_id: int) -> Orden:
        existing = self.get_by_codigo(codigo)
        if existing:
            raise DuplicateException(f"El código {codigo} ya está registrado")
        
        orden = Orden(
            codigo=codigo,
            descripcion=descripcion,
            tecnico_id=tecnico_id,
            estado=EstadoOrden.PENDIENTE
        )
        self.db.add(orden)
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def update(self, id: int, **kwargs) -> Orden:
        orden = self.get_by_id(id)
        if not orden:
            raise NotFoundException(f"Orden con id {id} no encontrada")
        
        for key, value in kwargs.items():
            if value is not None and hasattr(orden, key):
                setattr(orden, key, value)
        
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def iniciar(self, id: int) -> Orden:
        orden = self.get_by_id(id)
        if not orden:
            raise NotFoundException(f"Orden con id {id} no encontrada")
        
        orden.estado = EstadoOrden.EN_PROCESO
        orden.fecha_inicio = datetime.utcnow()
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def completar(self, id: int, observaciones: Optional[str] = None) -> Orden:
        orden = self.get_by_id(id)
        if not orden:
            raise NotFoundException(f"Orden con id {id} no encontrada")
        
        orden.estado = EstadoOrden.COMPLETADA
        orden.fecha_fin = datetime.utcnow()
        if observaciones:
            orden.observaciones = observaciones
        self.db.commit()
        self.db.refresh(orden)
        return orden

    def cancelar(self, id: int, observaciones: Optional[str] = None) -> Orden:
        orden = self.get_by_id(id)
        if not orden:
            raise NotFoundException(f"Orden con id {id} no encontrada")
        
        orden.estado = EstadoOrden.CANCELADA
        if observaciones:
            orden.observaciones = observaciones
        self.db.commit()
        self.db.refresh(orden)
        return orden