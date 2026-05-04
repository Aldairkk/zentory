from sqlalchemy.orm import Session, joinedload
from app.models.movimiento import Movimiento, TipoMovimiento
from app.models.inventario import Inventario
from app.core.exceptions import NotFoundException
from typing import Optional, List
from datetime import datetime


class MovimientoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, id: int) -> Optional[Movimiento]:
        return self.db.query(Movimiento).filter(Movimiento.id == id).first()

    def get_by_serial(self, numero_serie: str) -> Optional[Movimiento]:
        return self.db.query(Movimiento).filter(
            Movimiento.numero_serie == numero_serie,
            Movimiento.serializado == True
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100, tipo: Optional[TipoMovimiento] = None,
               producto_id: Optional[int] = None, bodega_id: Optional[int] = None) -> List[Movimiento]:
        query = self.db.query(Movimiento)
        if tipo:
            query = query.filter(Movimiento.tipo == tipo)
        if producto_id:
            query = query.filter(Movimiento.producto_id == producto_id)
        if bodega_id:
            query = query.filter(
                (Movimiento.bodega_origen_id == bodega_id) | 
                (Movimiento.bodega_destino_id == bodega_id)
            )
        return query.order_by(Movimiento.fecha_movimiento.desc()).offset(skip).limit(limit).all()

    def get_by_tecnico(self, tecnico_id: int, skip: int = 0, limit: int = 100) -> List[Movimiento]:
        return self.db.query(Movimiento).filter(
            Movimiento.tecnico_id == tecnico_id
        ).order_by(Movimiento.fecha_movimiento.desc()).offset(skip).limit(limit).all()

    def get_by_solicitud(self, solicitud_id: int) -> List[Movimiento]:
        return self.db.query(Movimiento).filter(Movimiento.solicitud_id == solicitud_id).all()

    def get_by_orden(self, orden_id: int) -> List[Movimiento]:
        return self.db.query(Movimiento).filter(Movimiento.orden_id == orden_id).all()
    
    def get_by_consecutive(self, consecutive: str) -> Optional[Movimiento]:
        return self.db.query(Movimiento).filter(Movimiento.consecutive == consecutive).first()
    
    def get_by_serial(self, numero_serie: str) -> Optional[Movimiento]:
        return self.db.query(Movimiento).filter(
            Movimiento.numero_serie.like(f"%{numero_serie.upper()}%")
        ).first()

    def get_serial_in_inventario(self, numero_serie: str, producto_id: int, bodega_id: int) -> Optional[Inventario]:
        return self.db.query(Inventario).filter(
            Inventario.producto_id == producto_id,
            Inventario.bodega_id == bodega_id,
            Inventario.numero_serie.like(f"%{numero_serie.upper()}%")
        ).first()

    def create(self, tipo: TipoMovimiento, producto_id: int, cantidad: float, valor_unitario: float,
              bodega_origen_id: Optional[int] = None, bodega_destino_id: Optional[int] = None,
              proveedor_id: Optional[int] = None, usuario_id: Optional[int] = None,
              tecnico_id: Optional[int] = None, solicitud_id: Optional[int] = None,
              orden_id: Optional[int] = None, motivo: Optional[str] = None,
              numero_serie: Optional[str] = None, estado_producto: Optional[str] = None,
              iva: bool = False, serializado: bool = False, referencia: Optional[str] = None,
              ubicacion: Optional[str] = None, observaciones: Optional[str] = None,
              consecutive: Optional[str] = None, consecutive_item: Optional[str] = None,
              asignar_a: Optional[str] = None, usuario_asignado_id: Optional[int] = None) -> Movimiento:
        
        tipo_prefix = tipo.value[:3].upper()
        
        if consecutive:
            pass
        else:
            last_mov = self.db.query(Movimiento).filter(
                Movimiento.consecutive.like(f"{tipo_prefix}-%")
            ).order_by(Movimiento.id.desc()).first()
            
            if last_mov and last_mov.consecutive:
                num = int(last_mov.consecutive.split('-')[1]) + 1
            else:
                num = 1
            consecutive = f"{tipo_prefix}-{num:03d}"
        
        movimiento = Movimiento(
            consecutive=consecutive,
            consecutive_item=consecutive_item,
            tipo=tipo,
            producto_id=producto_id,
            bodega_origen_id=bodega_origen_id,
            bodega_destino_id=bodega_destino_id,
            proveedor_id=proveedor_id,
            usuario_id=usuario_id,
            tecnico_id=tecnico_id,
            solicitud_id=solicitud_id,
            orden_id=orden_id,
            cantidad=cantidad,
            valor_unitario=valor_unitario,
            motivo=motivo,
            numero_serie=numero_serie,
            estado_producto=estado_producto,
            iva=iva,
            serializado=serializado,
            referencia=referencia,
            ubicacion=ubicacion,
            observaciones=observaciones,
            asignar_a=asignar_a,
            usuario_asignado_id=usuario_asignado_id
        )
        self.db.add(movimiento)
        self.db.commit()
        self.db.refresh(movimiento)
        return movimiento