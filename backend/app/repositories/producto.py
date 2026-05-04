from sqlalchemy.orm import Session
from app.models.producto import Producto, TipoProducto
from app.core.exceptions import NotFoundException, DuplicateException
from typing import Optional, List


class ProductoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Producto]:
        return self.db.query(Producto).filter(Producto.id == id).first()

    def get_by_codigo(self, codigo: str) -> Optional[Producto]:
        return self.db.query(Producto).filter(Producto.codigo == codigo).first()

    def get_all(self, skip: int = 0, limit: int = 100, estado: Optional[bool] = None) -> List[Producto]:
        query = self.db.query(Producto)
        if estado is not None:
            query = query.filter(Producto.estado == estado)
        return query.offset(skip).limit(limit).all()

    def get_by_tipo(self, tipo: TipoProducto, skip: int = 0, limit: int = 100) -> List[Producto]:
        return self.db.query(Producto).filter(Producto.tipo == tipo).offset(skip).limit(limit).all()

    def create(self, codigo: str, nombre: str, descripcion: Optional[str] = None, 
               categoria_id: Optional[int] = None, proveedor_id: Optional[int] = None,
               serializado: bool = False, precio: float = 0, unidad_medida: str = "und", 
               cantidad_minima: int = 0) -> Producto:
        existing = self.get_by_codigo(codigo)
        if existing:
            raise DuplicateException(f"El código {codigo} ya está registrado")
        
        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            descripcion=descripcion,
            categoria_id=categoria_id,
            proveedor_id=proveedor_id,
            serializado=serializado,
            precio=precio,
            unidad_medida=unidad_medida,
            cantidad_minima=cantidad_minima,
            tipo=TipoProducto.SERIALIZADO if serializado else TipoProducto.NO_SERIALIZADO
        )
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def update(self, id: int, **kwargs) -> Producto:
        producto = self.get_by_id(id)
        if not producto:
            raise NotFoundException(f"Producto con id {id} no encontrado")
        
        if "codigo" in kwargs:
            nuevo_codigo = kwargs["codigo"]
            existing = self.get_by_codigo(nuevo_codigo)
            if existing and existing.id != id:
                raise DuplicateException(f"El código {nuevo_codigo} ya está registrado")
        
        if "serializado" in kwargs and kwargs["serializado"] is not None:
            kwargs["tipo"] = TipoProducto.SERIALIZADO if kwargs["serializado"] else TipoProducto.NO_SERIALIZADO
        
        for key, value in kwargs.items():
            if value is not None and hasattr(producto, key):
                setattr(producto, key, value)
        
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def delete(self, id: int):
        producto = self.get_by_id(id)
        if not producto:
            raise NotFoundException(f"Producto con id {id} no encontrado")
        
        producto.estado = False
        self.db.commit()