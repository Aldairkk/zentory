from sqlalchemy.orm import Session
from app.models import Usuario, RolUsuario
from app.core.exceptions import NotFoundException, DuplicateException
from typing import Optional, List
from app.core.security import pwd_context


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.id == id).first()

    def get_by_email(self, email: str) -> Optional[Usuario]:
        return self.db.query(Usuario).filter(Usuario.email == email).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Usuario]:
        return self.db.query(Usuario).offset(skip).limit(limit).all()

    def get_by_rol(self, rol: RolUsuario) -> List[Usuario]:
        return self.db.query(Usuario).filter(Usuario.rol == rol).all()

    def create(self, nombre: str, apellido: str, email: str, password: str, cargo: str = None, rol: RolUsuario = RolUsuario.TECNICO) -> Usuario:
        existing = self.get_by_email(email)
        if existing:
            raise DuplicateException(f"El email {email} ya está registrado")
        
        hashed = pwd_context.hash(password)
        usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=hashed,
            cargo=cargo,
            rol=rol,
            estado=True
        )
        self.db.add(usuario)
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def verificar_password(self, usuario: Usuario, password: str) -> bool:
        return pwd_context.verify(password, usuario.password)

    def update(self, id: int, **kwargs) -> Usuario:
        usuario = self.get_by_id(id)
        if not usuario:
            raise NotFoundException(f"Usuario con id {id} no encontrado")
        
        if "password" in kwargs:
            kwargs["password"] = pwd_context.hash(kwargs["password"])
        
        for key, value in kwargs.items():
            if value is not None and hasattr(usuario, key):
                setattr(usuario, key, value)
        
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, id: int):
        usuario = self.get_by_id(id)
        if not usuario:
            raise NotFoundException(f"Usuario con id {id} no encontrado")
        
        usuario.estado = False
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def update(self, id: int, **kwargs) -> Usuario:
        usuario = self.get_by_id(id)
        if not usuario:
            raise NotFoundException(f"Usuario con id {id} no encontrado")
        
        for key, value in kwargs.items():
            if value is not None and hasattr(usuario, key):
                if key == "password":
                    value = get_password_hash(value)
                setattr(usuario, key, value)
        
        self.db.commit()
        self.db.refresh(usuario)
        return usuario

    def delete(self, id: int):
        usuario = self.get_by_id(id)
        if not usuario:
            raise NotFoundException(f"Usuario con id {id} no encontrado")
        
        usuario.estado = False
        self.db.commit()

    def verificar_password(self, usuario: Usuario, password: str) -> bool:
        from app.core.security import verify_password
        return verify_password(password, usuario.password)