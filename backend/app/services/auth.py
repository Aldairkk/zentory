from sqlalchemy.orm import Session
from app.repositories.usuario import UsuarioRepository
from app.schemas.auth import LoginRequest, LoginResponse
from app.models.usuario import Usuario, RolUsuario
from app.core.security import create_access_token
from app.core.exceptions import UnauthorizedException, NotFoundException


class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.usuario_repo = UsuarioRepository(db)

    def login(self, request: LoginRequest) -> LoginResponse:
        usuario = self.usuario_repo.get_by_email(request.email)
        
        if not usuario:
            raise UnauthorizedException("Credenciales inválidas")
        
        if not usuario.estado:
            raise UnauthorizedException("Usuario inactivo")
        
        if not self.usuario_repo.verificar_password(usuario, request.password):
            raise UnauthorizedException("Credenciales inválidas")
        
        if usuario.rol == RolUsuario.EMPLEADO:
            raise UnauthorizedException("Empleado no tiene acceso al sistema")
        
        access_token = create_access_token({
            "sub": str(usuario.id),
            "email": usuario.email,
            "rol": usuario.rol.value
        })
        
        return LoginResponse(
            access_token=access_token,
            usuario_id=usuario.id,
            email=usuario.email,
            nombre=f"{usuario.nombre} {usuario.apellido}",
            rol=usuario.rol.value
        )

    def verificar_rol(self, usuario_id: int, rol_requerido: RolUsuario) -> bool:
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            return False
        return usuario.rol == rol_requerido

    def es_admin(self, usuario_id: int) -> bool:
        return self.verificar_rol(usuario_id, RolUsuario.ADMIN)

    def es_semiadmin(self, usuario_id: int) -> bool:
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            return False
        return usuario.rol in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]

    def es_tecnico(self, usuario_id: int) -> bool:
        usuario = self.usuario_repo.get_by_id(usuario_id)
        if not usuario:
            return False
        return usuario.rol == RolUsuario.TECNICO