from sqlalchemy.orm import Session
from app.repositories.producto import ProductoRepository
from app.schemas.producto import ProductoCreate, ProductoUpdate
from app.models.producto import Producto, TipoProducto


class ProductoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProductoRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_by_codigo(self, codigo: str):
        return self.repo.get_by_codigo(codigo)

    def get_all(self, skip: int = 0, limit: int = 100, estado: bool = True):
        return self.repo.get_all(skip, limit, estado)

    def get_by_tipo(self, tipo: TipoProducto, skip: int = 0, limit: int = 100):
        return self.repo.get_by_tipo(tipo, skip, limit)

    def create(self, data: ProductoCreate):
        return self.repo.create(
            codigo=data.codigo,
            nombre=data.nombre,
            descripcion=data.descripcion,
            categoria_id=data.categoria_id,
            proveedor_id=data.proveedor_id,
            serializado=data.serializado,
            precio=data.precio,
            unidad_medida=data.unidad_medida,
            cantidad_minima=data.cantidad_minima
        )

    def update(self, id: int, data: ProductoUpdate):
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int):
        return self.repo.delete(id)