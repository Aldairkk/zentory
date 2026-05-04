from sqlalchemy.orm import Session
from app.repositories.inventario import InventarioRepository
from app.repositories.producto import ProductoRepository
from app.repositories.bodega import BodegaRepository
from app.schemas.inventario import InventarioCreate, InventarioUpdate
from app.models.inventario import Inventario, EstadoProducto
from app.models.producto import TipoProducto
from app.core.exceptions import InventoryException, ValidationException


class InventarioService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = InventarioRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.bodega_repo = BodegaRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100, bodega_id: int = None):
        return self.repo.get_all(skip, limit, bodega_id)

    def get_by_producto(self, producto_id: int):
        return self.repo.get_by_producto(producto_id)

    def get_by_bodega(self, bodega_id: int):
        return self.repo.get_by_bodega(bodega_id)

    def get_stock_total(self, producto_id: int) -> float:
        return self.repo.get_stock_total(producto_id)

    def validar_stock(self, producto_id: int, bodega_id: int, cantidad: float, 
                     estado_producto: EstadoProducto = EstadoProducto.NUEVO) -> bool:
        inventario = self.repo.get_by_producto_bodega_estado(producto_id, bodega_id, estado_producto)
        if not inventario:
            return False
        return float(inventario.cantidad) >= cantidad

    def _validar_producto(self, producto_id: int):
        producto = self.producto_repo.get_by_id(producto_id)
        if not producto:
            raise ValidationException(f"Producto con id {producto_id} no encontrado")
        if not producto.estado:
            raise ValidationException(f"Producto inactivo")
        return producto

    def _validar_bodega(self, bodega_id: int):
        bodega = self.bodega_repo.get_by_id(bodega_id)
        if not bodega:
            raise ValidationException(f"Bodega con id {bodega_id} no encontrada")
        if not bodega.estado:
            raise ValidationException(f"Bodega inactiva")
        return bodega

    def _validar_cantidad(self, cantidad: float, unidad_medida: str):
        if cantidad <= 0:
            raise ValidationException("La cantidad debe ser mayor a 0")
        
        if unidad_medida == "und" and cantidad != int(cantidad):
            raise ValidationException("Los productos con unidad 'und' no permiten decimales")

    def _calcular_valor_total(self, cantidad: float, valor_unitario: float) -> float:
        return round(cantidad * valor_unitario, 2)

    def crear_ingreso(self, data: InventarioCreate, usuario_id: int = None):
        producto = self._validar_producto(data.producto_id)
        bodega = self._validar_bodega(data.bodega_id)
        
        self._validar_cantidad(float(data.cantidad), producto.unidad_medida)
        
        cantidad = float(data.cantidad)
        valor_unitario = float(data.valor_unitario)
        
        if producto.tipo == TipoProducto.NO_SERIALIZADO and data.estado_producto == EstadoProducto.NUEVO:
            inventario = self.repo.recalcular_costo_promedio(
                data.producto_id, 
                data.bodega_id, 
                cantidad, 
                valor_unitario
            )
        else:
            inventario = self.repo.crear_o_actualizar(
                data.producto_id,
                data.bodega_id,
                cantidad,
                valor_unitario,
                data.estado_producto
            )
        
        return inventario

    def reducir_stock(self, producto_id: int, bodega_id: int, cantidad: float,
                     estado_producto: EstadoProducto = EstadoProducto.NUEVO):
        producto = self._validar_producto(producto_id)
        bodega = self._validar_bodega(bodega_id)
        
        self._validar_cantidad(cantidad, producto.unidad_medida)
        
        if not self.validar_stock(producto_id, bodega_id, cantidad, estado_producto):
            raise InventoryException(
                f"Stock insuficiente para el producto en esta bodega"
            )
        
        return self.repo.reducir_stock(producto_id, bodega_id, cantidad, estado_producto)

    def get_resumen_inventario(self, bodega_id: int = None):
        inventarios = self.get_all(bodega_id=bodega_id)
        
        stock_total = sum(float(inv.cantidad) for inv in inventarios)
        valor_total = sum(
            float(inv.cantidad) * float(inv.valor_unitario) 
            for inv in inventarios
        )
        
        return {
            "total_items": len(inventarios),
            "stock_total": stock_total,
            "valor_total": round(valor_total, 2)
        }