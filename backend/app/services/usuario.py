from sqlalchemy.orm import Session
from app.repositories.usuario import UsuarioRepository
from app.schemas.usuario import UsuarioCreate, UsuarioUpdate
from app.models.usuario import Usuario, RolUsuario
from app.core.exceptions import ValidationException


class UsuarioService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = UsuarioRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_by_email(self, email: str):
        return self.repo.get_by_email(email)

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.repo.get_all(skip, limit)

    def get_by_rol(self, rol: RolUsuario, skip: int = 0, limit: int = 100):
        return self.repo.get_by_rol(rol, skip, limit)

    def create(self, data: UsuarioCreate):
        if data.rol == RolUsuario.EMPLEADO and data.password:
            raise ValidationException("Empleado no debe tener acceso al sistema")
        return self.repo.create(
            nombre=data.nombre,
            apellido=data.apellido,
            email=data.email,
            password=data.password,
            cargo=data.cargo,
            rol=data.rol
        )

    def update(self, id: int, data: UsuarioUpdate):
        update_data = data.model_dump(exclude_unset=True)
        return self.repo.update(id, **update_data)

    def delete(self, id: int):
        return self.repo.delete(id)