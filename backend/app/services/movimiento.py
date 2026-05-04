from sqlalchemy.orm import Session
from app.repositories.movimiento import MovimientoRepository
from app.repositories.inventario import InventarioRepository
from app.repositories.producto import ProductoRepository
from app.repositories.bodega import BodegaRepository
from app.schemas.movimiento import MovimientoCreate
from app.models.movimiento import Movimiento, TipoMovimiento
from app.models.inventario import EstadoProducto
from app.models.producto import TipoProducto
from app.core.exceptions import ValidationException, InventoryException
import logging
logger = logging.getLogger(__name__)


class MovimientoService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = MovimientoRepository(db)
        self.inventario_repo = InventarioRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.bodega_repo = BodegaRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100, tipo: TipoMovimiento = None,
               producto_id: int = None, bodega_id: int = None):
        return self.repo.get_all(skip, limit, tipo, producto_id, bodega_id)

    def get_by_tecnico(self, tecnico_id: int, skip: int = 0, limit: int = 100):
        return self.repo.get_by_tecnico(tecnico_id, skip, limit)

    def get_by_solicitud(self, solicitud_id: int):
        return self.repo.get_by_solicitud(solicitud_id)

    def get_by_orden(self, orden_id: int):
        return self.repo.get_by_orden(orden_id)

    def _validar_producto(self, producto_id: int):
        producto = self.producto_repo.get_by_id(producto_id)
        if not producto:
            raise ValidationException(f"Producto con id {producto_id} no encontrado")
        return producto

    def _validar_bodega(self, bodega_id: int):
        bodega = self.bodega_repo.get_by_id(bodega_id)
        if not bodega:
            raise ValidationException(f"Bodega con id {bodega_id} no encontrada")
        return bodega

    def _validar_cantidad(self, cantidad: float, unidad_medida: str):
        if cantidad <= 0:
            raise ValidationException("La cantidad debe ser mayor a 0")
        if unidad_medida == "und" and cantidad != int(cantidad):
            raise ValidationException("Los productos con unidad 'und' no permiten decimales")

    def _crear_movimiento(self, data: MovimientoCreate, usuario_id: int = None, consecutive: str = None):
        return self.repo.create(
            tipo=data.tipo,
            producto_id=data.producto_id,
            cantidad=float(data.cantidad),
            valor_unitario=float(data.valor_unitario),
            bodega_origen_id=data.bodega_origen_id,
            bodega_destino_id=data.bodega_destino_id,
            proveedor_id=data.proveedor_id,
            usuario_id=usuario_id,
            tecnico_id=getattr(data, 'tecnico_id', None),
            solicitud_id=getattr(data, 'solicitud_id', None),
            orden_id=getattr(data, 'orden_id', None),
            motivo=getattr(data, 'motivo', None),
            numero_serie=getattr(data, 'numero_serie', None),
            estado_producto=getattr(data, 'estado_producto', None),
            iva=getattr(data, 'iva', False),
            serializado=getattr(data, 'serializado', False),
            referencia=getattr(data, 'referencia', None),
            ubicacion=getattr(data, 'ubicacion', None),
            observaciones=getattr(data, 'observaciones', None),
            consecutive=consecutive,
            consecutive_item=getattr(data, 'consecutive_item', None),
            asignar_a=getattr(data, 'asignar_a', None),
            usuario_asignado_id=getattr(data, 'usuario_asignado_id', None)
        )

    def crear_movimiento(self, data: MovimientoCreate, usuario_id: int = None, consecutive: str = None):
        tipo_str = data.tipo.value if hasattr(data.tipo, 'value') else str(data.tipo)
        if tipo_str == "entrada" or tipo_str == "ingreso":
            return self.entrada_bodega(data, getattr(data, 'proveedor_id', None), usuario_id, consecutive)
        elif tipo_str == "salida":
            return self.salida_bodega(data, data.motivo or "Salida de inventario", usuario_id)
        elif tipo_str == "transferencia":
            return self.transferencia(data, usuario_id)
        elif tipo_str == "consumo":
            return self.consumo(data, usuario_id)
        elif tipo_str == "entrega":
            return self.entrega_tecnico(data, usuario_id, consecutive)
        elif tipo_str == "devolucion":
            return self.devolucion_tecnico(data, usuario_id, consecutive)
        else:
            raise ValidationException(f"Tipo de movimiento no válido: {tipo_str}")

    def entrada_bodega(self, data: MovimientoCreate, proveedor_id: int, usuario_id: int = None, consecutive: str = None):
        producto = self._validar_producto(data.producto_id)
        self._validar_bodega(data.bodega_destino_id)
        self._validar_cantidad(float(data.cantidad), producto.unidad_medida)
        
        numero_serie = getattr(data, 'numero_serie', None)
        serializado = getattr(data, 'serializado', False)
        
        if serializado and numero_serie:
            existing = self.repo.get_by_serial(numero_serie)
            if existing:
                raise ValidationException(f"El serial {numero_serie} ya existe en el sistema")
        
        valor_unitario = float(data.valor_unitario)
        estado_producto_data = getattr(data, 'estado_producto', None)
        
        if producto.tipo == TipoProducto.NO_SERIALIZADO:
            estado = EstadoProducto(estado_producto_data) if estado_producto_data else EstadoProducto.NUEVO
            self.inventario_repo.recalcular_costo_promedio(
                data.producto_id,
                data.bodega_destino_id,
                float(data.cantidad),
                valor_unitario
            )
        elif serializado:
            self.inventario_repo.crear_o_actualizar(
                data.producto_id,
                data.bodega_destino_id,
                float(data.cantidad),
                valor_unitario,
                EstadoProducto(estado_producto_data) if estado_producto_data else EstadoProducto.NUEVO
            )
        else:
            self.inventario_repo.crear_o_actualizar(
                data.producto_id,
                data.bodega_destino_id,
                float(data.cantidad),
                valor_unitario,
                EstadoProducto(estado_producto_data) if estado_producto_data else EstadoProducto.NUEVO
            )
        
        return self._crear_movimiento(data, usuario_id, consecutive)

    def salida_bodega(self, data: MovimientoCreate, motivo: str, usuario_id: int = None):
        producto = self._validar_producto(data.producto_id)
        self._validar_bodega(data.bodega_origen_id)
        self._validar_cantidad(float(data.cantidad), producto.unidad_medida)
        
        estado = EstadoProducto(getattr(data, 'estado_producto', None)) if getattr(data, 'estado_producto', None) else EstadoProducto.NUEVO
        
        if not self.inventario_repo.get_by_producto_bodega_estado(
            data.producto_id, data.bodega_origen_id, estado
        ):
            raise InventoryException("No existe inventario para el producto en esta bodega")
        
        self.inventario_repo.reducir_stock(
            data.producto_id,
            data.bodega_origen_id,
            float(data.cantidad),
            estado
        )
        
        return self._crear_movimiento(data, usuario_id)

    def transferencia(self, data: MovimientoCreate, usuario_id: int = None):
        producto = self._validar_producto(data.producto_id)
        self._validar_bodega(data.bodega_origen_id)
        self._validar_bodega(data.bodega_destino_id)
        self._validar_cantidad(float(data.cantidad), producto.unidad_medida)
        
        estado = EstadoProducto(getattr(data, 'estado_producto', None)) if getattr(data, 'estado_producto', None) else EstadoProducto.NUEVO
        
        self.inventario_repo.reducir_stock(
            data.producto_id,
            data.bodega_origen_id,
            float(data.cantidad),
            estado
        )
        
        self.inventario_repo.crear_o_actualizar(
            data.producto_id,
            data.bodega_destino_id,
            float(data.cantidad),
            float(data.valor_unitario),
            estado
        )
        
        return self._crear_movimiento(data, usuario_id)

    def consumo(self, data: MovimientoCreate, usuario_id: int = None):
        producto = self._validar_producto(data.producto_id)
        self._validar_bodega(data.bodega_origen_id)
        self._validar_cantidad(float(data.cantidad), producto.unidad_medida)
        
        estado = EstadoProducto(data.estado_producto) if data.estado_producto else EstadoProducto.NUEVO
        
        self.inventario_repo.reducir_stock(
            data.producto_id,
            data.bodega_origen_id,
            float(data.cantidad),
            estado
        )
        
        return self._crear_movimiento(data, usuario_id)

    def consumo_tecnico(self, data: MovimientoCreate, orden_id: int, usuario_id: int = None):
        producto = self._validar_producto(data.producto_id)
        self._validar_cantidad(float(data.cantidad), producto.unidad_medida)
        
        if not data.tecnico_id:
            raise ValidationException("Se requiere especificar el técnico")
        
        estado = EstadoProducto(data.estado_producto) if data.estado_producto else EstadoProducto.NUEVO
        
        self.inventario_repo.reducir_stock(
            data.producto_id,
            data.bodega_origen_id,
            float(data.cantidad),
            estado
        )
        
        return self._crear_movimiento(data, usuario_id)

    def entrega_tecnico(self, data: MovimientoCreate, usuario_id: int = None, consecutive: str = None):
        import sys
        producto = self._validar_producto(data.producto_id)
        bodega_id = data.bodega_origen_id
        cantidad = float(data.cantidad)
        
        if not getattr(data, 'usuario_asignado_id', None):
            raise ValidationException("Se requiere especificar el técnico")
        
        # Check current stock in bodega
        try:
            inv = self.inventario_repo.get_by_producto_bodega_estado(
                data.producto_id, 
                bodega_id, 
                EstadoProducto.NUEVO
            )
            if inv:
                stock_actual = float(inv.cantidad)
                print(f"[DEBUG] Stock {producto.nombre} in bodega {bodega_id}: {stock_actual}, reduction: {cantidad}", file=sys.stderr)
                
                if stock_actual >= cantidad:
                    self.inventario_repo.reducir_stock(
                        data.producto_id,
                        bodega_id,
                        cantidad,
                        EstadoProducto.NUEVO
                    )
                    print(f"[DEBUG] Reduced {cantidad} from bodega {bodega_id}", file=sys.stderr)
                else:
                    raise InventoryException(f"Stock insuficiente en bodega. Disponible: {stock_actual}")
            else:
                # Try USADO state
                inv_usado = self.inventario_repo.get_by_producto_bodega_estado(
                    data.producto_id,
                    bodega_id,
                    EstadoProducto.USADO
                )
                if inv_usado and float(inv_usado.cantidad) >= cantidad:
                    self.inventario_repo.reducir_stock(
                        data.producto_id,
                        bodega_id,
                        cantidad,
                        EstadoProducto.USADO
                    )
                else:
                    raise InventoryException(f"No hay inventario del producto en esta bodega")
        except InventoryException as e:
            raise e
        
        return self._crear_movimiento(data, usuario_id, consecutive)

    def devolucion_tecnico(self, data: MovimientoCreate, usuario_id: int = None, consecutive: str = None):
        producto = self._validar_producto(data.producto_id)
        self._validar_bodega(data.bodega_destino_id)
        self._validar_cantidad(float(data.cantidad), producto.unidad_medida)
        
        numero_serie = getattr(data, 'numero_serie', None)
        serializado = getattr(data, 'serializado', False)
        
        estado = EstadoProducto.NUEVO
        
        self.inventario_repo.crear_o_actualizar(
            data.producto_id,
            data.bodega_destino_id,
            float(data.cantidad),
            float(data.valor_unitario or 0),
            estado
        )
        
        return self._crear_movimiento(data, usuario_id, consecutive)

    def get_by_consecutive(self, consecutive: str):
        return self.repo.get_by_consecutive(consecutive)

    def update_movimiento_by_consecutive(self, consecutive: str, data: dict):
        items = self.db.query(Movimiento).filter(Movimiento.consecutive == consecutive).all()
        if not items:
            raise ValidationException(f"Movimiento {consecutive} no encontrado")
        
        for m in items:
            if 'observaciones' in data:
                m.observaciones = data['observaciones']
            if 'asignar_a' in data:
                m.asignar_a = data['asignar_a']
            if 'usuario_asignado_id' in data:
                m.usuario_asignado_id = data['usuario_asignado_id']
        
        self.db.commit()
        self.db.refresh(items[0])
        return items[0]

    def update_movimiento(self, consecutive: str, data: dict, movimiento_id: int = None):
        if movimiento_id:
            movimiento = self.db.query(Movimiento).filter(Movimiento.id == movimiento_id).first()
        else:
            movimiento = self.db.query(Movimiento).filter(Movimiento.consecutive == consecutive).first()
        
        if not movimiento:
            raise ValidationException(f"Movimiento {consecutive} no encontrado")
        
        cantidad_val = data.get('cantidad')
        valor_unitario_val = data.get('valor_unitario')
        iva_val = data.get('iva')
        ubicacion_val = data.get('ubicacion')
        
        if cantidad_val is not None:
            movimiento.cantidad = cantidad_val
        if valor_unitario_val is not None:
            movimiento.valor_unitario = float(valor_unitario_val)
        if iva_val is not None:
            iva_bool = iva_val if isinstance(iva_val, bool) else (str(iva_val).lower() == 'true')
            movimiento.iva = iva_bool
        if ubicacion_val is not None:
            movimiento.ubicacion = str(ubicacion_val)
        
        self.db.commit()
        self.db.refresh(movimiento)
        return movimiento
    
    def delete_movimiento(self, consecutive: str):
        movimiento = self.repo.get_by_consecutive(consecutive)
        if not movimiento:
            raise ValidationException(f"Movimiento {consecutive} no encontrado")
        
        self.db.delete(movimiento)
        self.db.commit()
        return {"message": "Eliminado"}