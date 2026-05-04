from sqlalchemy.orm import Session
from app.repositories.proveedor import ProveedorRepository
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate


class ProveedorService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ProveedorRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100, estado: bool = True):
        return self.repo.get_all(skip, limit, estado)

    def create(self, data: ProveedorCreate):
        return self.repo.create(
            nombre=data.nombre,
            nit=data.nit,
            email=data.email,
            telefono=data.telefono,
            ciudad=data.ciudad if hasattr(data, 'ciudad') else None,
            direccion=data.direccion
        )

    def update(self, id: int, data: ProveedorUpdate):
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int):
        return self.repo.delete(id)