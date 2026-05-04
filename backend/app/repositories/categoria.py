from sqlalchemy.orm import Session
from app.models.categoria import Categoria
from app.core.exceptions import NotFoundException, DuplicateException
from typing import Optional, List


class CategoriaRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(Categoria.id == id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Categoria]:
        return self.db.query(Categoria).filter(Categoria.codigo == codigo).first()

    def get_all(self, skip: int = 0, limit: int = 100, estado: Optional[bool] = None) -> List[Categoria]:
        query = self.db.query(Categoria)
        if estado is not None:
            query = query.filter(Categoria.estado == estado)
        return query.offset(skip).limit(limit).all()

    def create(self, codigo: str, nombre: str, descripcion: Optional[str] = None) -> Categoria:
        existing = self.get_by_codigo(codigo)
        if existing:
            raise DuplicateException(f"El código {codigo} ya está registrado")
        
        categoria = Categoria(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion
        )
        self.db.add(categoria)
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def update(self, id: int, **kwargs) -> Categoria:
        categoria = self.get_by_id(id)
        if not categoria:
            raise NotFoundException(f"Categoría con id {id} no encontrada")
        
        if "codigo" in kwargs:
            nuevo_codigo = kwargs["codigo"]
            existing = self.get_by_codigo(nuevo_codigo)
            if existing and existing.id != id:
                raise DuplicateException(f"El código {nuevo_codigo} ya está registrado")
        
        for key, value in kwargs.items():
            if value is not None and hasattr(categoria, key):
                setattr(categoria, key, value)
        
        self.db.commit()
        self.db.refresh(categoria)
        return categoria

    def delete(self, id: int):
        categoria = self.get_by_id(id)
        if not categoria:
            raise NotFoundException(f"Categoría con id {id} no encontrada")
        
        categoria.estado = False
        self.db.commit()