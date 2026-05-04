from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from app.models.inventario import Inventario, EstadoProducto
from app.core.exceptions import NotFoundException, InventoryException
from typing import Optional, List


class InventarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Inventario]:
        return self.db.query(Inventario).filter(Inventario.id == id).first()

    def get_by_producto_bodega_estado(self, producto_id: int, bodega_id: int, estado_producto: EstadoProducto) -> Optional[Inventario]:
        return self.db.query(Inventario).filter(
            and_(
                Inventario.producto_id == producto_id,
                Inventario.bodega_id == bodega_id,
                Inventario.estado_producto == estado_producto
            )
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100, bodega_id: Optional[int] = None) -> List[Inventario]:
        query = self.db.query(Inventario).options(
            joinedload(Inventario.producto),
            joinedload(Inventario.bodega)
        )
        if bodega_id:
            query = query.filter(Inventario.bodega_id == bodega_id)
        return query.offset(skip).limit(limit).all()

    def get_by_producto(self, producto_id: int) -> List[Inventario]:
        return self.db.query(Inventario).filter(Inventario.producto_id == producto_id).all()

    def get_by_bodega(self, bodega_id: int) -> List[Inventario]:
        return self.db.query(Inventario).filter(Inventario.bodega_id == bodega_id).all()

    def get_stock_total(self, producto_id: int) -> float:
        inventarios = self.get_by_producto(producto_id)
        return sum(float(inv.cantidad) for inv in inventarios)

    def crear_o_actualizar(self, producto_id: int, bodega_id: int, cantidad: float, 
                      valor_unitario: float, estado_producto: EstadoProducto) -> Inventario:
        inventario = self.get_by_producto_bodega_estado(producto_id, bodega_id, estado_producto)
        
        if inventario:
            inventario.cantidad = float(inventario.cantidad) + cantidad
            inventario.valor_unitario = valor_unitario
            self.db.commit()
            self.db.refresh(inventario)
        else:
            inventario = Inventario(
                producto_id=producto_id,
                bodega_id=bodega_id,
                cantidad=cantidad,
                valor_unitario=valor_unitario,
                estado_producto=estado_producto
            )
            self.db.add(inventario)
            self.db.commit()
            self.db.refresh(inventario)
        
        return inventario

    def reducir_stock(self, producto_id: int, bodega_id: int, cantidad: float,
                    estado_producto: EstadoProducto) -> Inventario:
        inventario = self.get_by_producto_bodega_estado(producto_id, bodega_id, estado_producto)
        
        if not inventario:
            raise InventoryException(f"No existe inventario para el producto en esta bodega")
        
        stock_actual = float(inventario.cantidad)
        if stock_actual < cantidad:
            raise InventoryException(
                f"Stock insuficiente. Disponible: {stock_actual}, Solicitado: {cantidad}"
            )
        
        inventario.cantidad = stock_actual - cantidad
        self.db.commit()
        self.db.refresh(inventario)
        return inventario

    def recalcular_costo_promedio(self, producto_id: int, bodega_id: int, 
                                cantidad_nueva: float, valor_unitario_nuevo: float) -> Inventario:
        inventario = self.get_by_producto_bodega_estado(producto_id, bodega_id, EstadoProducto.NUEVO)
        
        if not inventario or float(inventario.cantidad) == 0:
            return self.crear_o_actualizar(
                producto_id, bodega_id, cantidad_nueva, 
                valor_unitario_nuevo, EstadoProducto.NUEVO
            )
        
        stock_actual = float(inventario.cantidad)
        costo_actual = float(inventario.valor_unitario)
        
        nuevo_valor_unitario = (
            (stock_actual * costo_actual) + (cantidad_nueva * valor_unitario_nuevo)
        ) / (stock_actual + cantidad_nueva)
        
        inventario.cantidad = stock_actual + cantidad_nueva
        inventario.valor_unitario = nuevo_valor_unitario
        self.db.commit()
        self.db.refresh(inventario)
        return inventario