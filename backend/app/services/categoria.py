from sqlalchemy.orm import Session
from app.repositories.categoria import CategoriaRepository
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


class CategoriaService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = CategoriaRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_by_codigo(self, codigo: str):
        return self.repo.get_by_codigo(codigo)

    def get_all(self, skip: int = 0, limit: int = 100, estado: bool = True):
        return self.repo.get_all(skip, limit, estado)

    def create(self, data: CategoriaCreate):
        return self.repo.create(
            codigo=data.codigo,
            nombre=data.nombre,
            descripcion=data.descripcion
        )

    def update(self, id: int, data: CategoriaUpdate):
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int):
        return self.repo.delete(id)