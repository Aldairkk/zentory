from sqlalchemy.orm import Session
from app.models.bodega import Bodega
from app.models.inventario import Inventario
from app.core.exceptions import NotFoundException, DuplicateException
from typing import Optional, List


class BodegaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Bodega]:
        return self.db.query(Bodega).filter(Bodega.id == id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Bodega]:
        return self.db.query(Bodega).filter(Bodega.codigo == codigo).first()

    def get_all(self, skip: int = 0, limit: int = 100, estado: Optional[bool] = None) -> List[Bodega]:
        query = self.db.query(Bodega)
        if estado is not None:
            query = query.filter(Bodega.estado == estado)
        return query.offset(skip).limit(limit).all()

    def tiene_items(self, bodega_id: int) -> bool:
        from sqlalchemy import func
        total = self.db.query(func.sum(Inventario.cantidad)).filter(
            Inventario.bodega_id == bodega_id
        ).scalar()
        return total and total > 0

    def create(self, codigo: str, nombre: str, ciudad: Optional[str] = None, direccion: Optional[str] = None) -> Bodega:
        existing = self.get_by_codigo(codigo)
        if existing:
            raise DuplicateException(f"El código {codigo} ya está registrado")
        
        bodega = Bodega(
            codigo=codigo,
            nombre=nombre,
            ciudad=ciudad,
            direccion=direccion
        )
        self.db.add(bodega)
        self.db.commit()
        self.db.refresh(bodega)
        return bodega

    def update(self, id: int, **kwargs) -> Bodega:
        bodega = self.get_by_id(id)
        if not bodega:
            raise NotFoundException(f"Bodega con id {id} no encontrada")
        
        if "codigo" in kwargs:
            nuevo_codigo = kwargs["codigo"]
            existing = self.get_by_codigo(nuevo_codigo)
            if existing and existing.id != id:
                raise DuplicateException(f"El código {nuevo_codigo} ya está registrado")
        
        for key, value in kwargs.items():
            if value is not None and hasattr(bodega, key):
                setattr(bodega, key, value)
        
        self.db.commit()
        self.db.refresh(bodega)
        return bodega

    def delete(self, id: int):
        bodega = self.get_by_id(id)
        if not bodega:
            raise NotFoundException(f"Bodega con id {id} no encontrada")
        
        if self.tiene_items(id):
            raise Exception("No se puede eliminar una bodega que contiene items. Primero debe mover o eliminar el inventario.")
        
        bodega.estado = False
        self.db.commit()