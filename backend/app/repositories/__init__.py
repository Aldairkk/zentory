from .usuario import UsuarioRepository
from .producto import ProductoRepository
from .bodega import BodegaRepository
from .proveedor import ProveedorRepository
from .inventario import InventarioRepository
from .movimiento import MovimientoRepository
from .solicitud import SolicitudRepository

__all__ = [
    "UsuarioRepository",
    "ProductoRepository",
    "BodegaRepository",
    "ProveedorRepository",
    "InventarioRepository",
    "MovimientoRepository",
    "SolicitudRepository",
]