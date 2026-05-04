from sqlalchemy.orm import Session
from app.repositories.solicitud import SolicitudRepository
from app.repositories.inventario import InventarioRepository
from app.repositories.producto import ProductoRepository
from app.repositories.bodega import BodegaRepository
from app.schemas.solicitud import SolicitudCreate
from app.models.solicitud import Solicitud, EstadoSolicitud
from app.models.inventario import EstadoProducto
from app.models.producto import TipoProducto
from app.core.exceptions import ValidationException, InventoryException


class SolicitudService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SolicitudRepository(db)
        self.inventario_repo = InventarioRepository(db)
        self.producto_repo = ProductoRepository(db)
        self.bodega_repo = BodegaRepository(db)

    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)

    def get_all(self, skip: int = 0, limit: int = 100, estado: EstadoSolicitud = None, tecnico_id: int = None):
        return self.repo.get_all(skip, limit, estado, tecnico_id)

    def get_pendientes(self, skip: int = 0, limit: int = 100):
        return self.repo.get_pendientes(skip, limit)

    def crear(self, data: SolicitudCreate, tecnico_id: int = None):
        if tecnico_id:
            data.tecnico_id = tecnico_id
        
        producto = self.producto_repo.get_by_id(data.producto_id)
        if not producto:
            raise ValidationException(f"Producto no encontrado")
        
        bodega = self.bodega_repo.get_by_id(data.bodega_id)
        if not bodega:
            raise ValidationException(f"Bodega no encontrada")
        
        if producto.unidad_medida == "und" and data.cantidad != int(data.cantidad):
            raise ValidationException("Unidades enteras requeridas")
        
        return self.repo.create(
            producto_id=data.producto_id,
            bodega_id=data.bodega_id,
            tecnico_id=data.tecnico_id,
            cantidad=data.cantidad,
            observaciones=data.observaciones
        )

    def aprobar(self, id: int, aprobador_id: int):
        solicitud = self.repo.get_by_id(id)
        if not solicitud:
            raise ValidationException(f"Solicitud no encontrada")
        
        if solicitud.estado != EstadoSolicitud.PENDIENTE:
            raise ValidationException("Solo se pueden aprobar solicitudes pendientes")
        
        estado_producto = EstadoProducto.NUEVO
        inventario = self.inventario_repo.get_by_producto_bodega_estado(
            solicitud.producto_id,
            solicitud.bodega_id,
            estado_producto
        )
        
        if not inventario or float(inventario.cantidad) < solicitud.cantidad:
            raise InventoryException("Stock insuficiente en bodega")
        
        self.inventario_repo.reducir_stock(
            solicitud.producto_id,
            solicitud.bodega_id,
            float(solicitud.cantidad),
            estado_producto
        )
        
        return self.repo.aprobar(id, aprobador_id)

    def rechazar(self, id: int, aprobador_id: int):
        return self.repo.rechazar(id, aprobador_id)

    def cancelar(self, id: int):
        solicitud = self.repo.get_by_id(id)
        if not solicitud:
            raise ValidationException(f"Solicitud no encontrada")
        
        if solicitud.tecnico_id:
            return self.repo.cancelar(id)
        raise ValidationException("Solo el técnico puede cancelar su solicitud")