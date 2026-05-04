from sqlalchemy.orm import Session
from app.repositories.orden import OrdenRepository
from app.schemas.orden import OrdenCreate, OrdenUpdate
from app.models.orden import Orden, EstadoOrden
from app.core.exceptions import ValidationException


class OrdenService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrdenRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_by_codigo(self, codigo: str):
        return self.repo.get_by_codigo(codigo)

    def get_all(self, skip: int = 0, limit: int = 100, estado: EstadoOrden = None, tecnico_id: int = None):
        return self.repo.get_all(skip, limit, estado, tecnico_id)

    def create(self, data: OrdenCreate):
        return self.repo.create(
            codigo=data.codigo,
            descripcion=data.descripcion,
            tecnico_id=data.tecnico_id
        )

    def update(self, id: int, data: OrdenUpdate):
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def iniciar(self, id: int):
        return self.repo.iniciar(id)

    def completar(self, id: int, observaciones: str = None):
        return self.repo.completar(id, observaciones)

    def cancelar(self, id: int, observaciones: str = None):
        return self.repo.cancelar(id, observaciones)