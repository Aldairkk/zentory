from .auth import router as auth_router
from .usuarios import router as usuarios_router
from .productos import router as productos_router
from .categorias import router as categorias_router
from .bodegas import router as bodegas_router
from .proveedores import router as proveedores_router
from .inventario import router as inventario_router
from .movimientos import router as movimientos_router
from .solicitudes import router as solicitudes_router
from .ordenes import router as ordenes_router

__all__ = [
    "auth_router",
    "usuarios_router",
    "productos_router",
    "categorias_router",
    "bodegas_router",
    "proveedores_router",
    "inventario_router",
    "movimientos_router",
    "solicitudes_router",
    "ordenes_router",
]