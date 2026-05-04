from sqlalchemy.orm import Session
from app.models.proveedor import Proveedor
from app.core.exceptions import NotFoundException, DuplicateException
from typing import Optional, List


class ProveedorRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Proveedor]:
        return self.db.query(Proveedor).filter(Proveedor.id == id).first()

    def get_by_nit(self, nit: str) -> Optional[Proveedor]:
        return self.db.query(Proveedor).filter(Proveedor.nit == nit).first()

    def get_all(self, skip: int = 0, limit: int = 100, estado: Optional[bool] = None) -> List[Proveedor]:
        query = self.db.query(Proveedor)
        if estado is not None:
            query = query.filter(Proveedor.estado == estado)
        return query.offset(skip).limit(limit).all()

    def create(self, nombre: str, nit: Optional[str] = None, email: Optional[str] = None, 
               telefono: Optional[str] = None, ciudad: Optional[str] = None,
               direccion: Optional[str] = None) -> Proveedor:
        if nit:
            existing = self.get_by_nit(nit)
            if existing:
                raise DuplicateException(f"El NIT {nit} ya está registrado")
        
        proveedor = Proveedor(
            nombre=nombre,
            nit=nit,
            email=email,
            telefono=telefono,
            ciudad=ciudad,
            direccion=direccion
        )
        self.db.add(proveedor)
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def update(self, id: int, **kwargs) -> Proveedor:
        proveedor = self.get_by_id(id)
        if not proveedor:
            raise NotFoundException(f"Proveedor con id {id} no encontrado")
        
        if "nit" in kwargs and kwargs["nit"]:
            existing = self.get_by_nit(kwargs["nit"])
            if existing and existing.id != id:
                raise DuplicateException(f"El NIT {kwargs['nit']} ya está registrado")
        
        for key, value in kwargs.items():
            if value is not None and hasattr(proveedor, key):
                setattr(proveedor, key, value)
        
        self.db.commit()
        self.db.refresh(proveedor)
        return proveedor

    def delete(self, id: int):
        proveedor = self.get_by_id(id)
        if not proveedor:
            raise NotFoundException(f"Proveedor con id {id} no encontrado")
        
        proveedor.estado = False
        self.db.commit()