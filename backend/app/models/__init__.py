# Re-export all models from individual files
from app.models.usuario import Usuario, RolUsuario
from app.models.producto import Producto, TipoProducto
from app.models.categoria import Categoria
from app.models.proveedor import Proveedor
from app.models.bodega import Bodega
from app.models.inventario import Inventario, EstadoProducto
from app.models.movimiento import Movimiento, TipoMovimiento
from app.models.orden import Orden, EstadoOrden
from app.models.solicitud import Solicitud, EstadoSolicitud

# Also export enums that are used in __init__ for backward compatibility
__all__ = [
    'Usuario', 'RolUsuario',
    'Producto', 'TipoProducto',
    'Categoria',
    'Proveedor',
    'Bodega',
    'Inventario', 'EstadoProducto',
    'Movimiento', 'TipoMovimiento',
    'Orden', 'EstadoOrden',
    'Solicitud', 'EstadoSolicitud',
]