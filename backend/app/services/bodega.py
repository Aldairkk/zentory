from sqlalchemy.orm import Session
from app.repositories.bodega import BodegaRepository
from app.schemas.bodega import BodegaCreate, BodegaUpdate


class BodegaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = BodegaRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_by_codigo(self, codigo: str):
        return self.repo.get_by_codigo(codigo)

    def get_all(self, skip: int = 0, limit: int = 100, estado: bool = None):
        return self.repo.get_all(skip, limit, estado)

    def create(self, data: BodegaCreate):
        return self.repo.create(
            codigo=data.codigo,
            nombre=data.nombre,
            ciudad=data.ciudad if hasattr(data, 'ciudad') else None,
            direccion=data.direccion
        )

    def update(self, id: int, data: BodegaUpdate):
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int):
        return self.repo.delete(id)