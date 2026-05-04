from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.exceptions import AppException, UnauthorizedException
from app.schemas.movimiento import MovimientoCreate, MovimientoResponse
from app.models.usuario import Usuario, RolUsuario
from app.models.movimiento import TipoMovimiento
from app.services.movimiento import MovimientoService
from app.routes.usuarios import get_current_user

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])


@router.get("/listar-serializados/")
def list_seriales(db: Session = Depends(get_db)):
    from app.models.movimiento import Movimiento
    from app.models.producto import Producto
    from app.models.bodega import Bodega
    
    movimientos = db.query(Movimiento).filter(
        Movimiento.numero_serie.isnot(None),
        Movimiento.numero_serie != ''
    ).all()
    
    seriales_list = []
    for m in movimientos:
        if m.numero_serie:
            for serial in m.numero_serie.split('|'):
                if serial.strip():
                    producto = db.query(Producto).filter(Producto.id == m.producto_id).first()
                    bodega = db.query(Bodega).filter(Bodega.id == m.bodega_destino_id).first()
                    seriales_list.append({
                        "serial": serial.strip(),
                        "item": {"id": producto.id, "nombre": producto.nombre} if producto else None,
                        "bodega_actual": {"id": bodega.id, "nombre": bodega.nombre} if bodega else None,
                        "estado": "en_bodega",
                        "fecha_ingreso": m.fecha_creacion.isoformat() if m.fecha_creacion else None
                    })
    
    return seriales_list


@router.post("/crear", response_model=MovimientoResponse)
def crear_movimiento(data: MovimientoCreate, db: Session = Depends(get_db),
                    usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = MovimientoService(db)
        return service.crear_movimiento(data, usuario.id)
    except AppException as e:
        raise e


@router.post("/crear-ingreso", response_model=List[MovimientoResponse])
def crear_ingreso_multiple(items: List[MovimientoCreate], db: Session = Depends(get_db),
                          usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    import traceback
    import sys
    try:
        print(f"[DEBUG] Received items: {items}", file=sys.stderr)
        service = MovimientoService(db)
        results = []
        consecutive = None
        
        for i, item in enumerate(items):
            print(f"[DEBUG] item: tipo={item.tipo}, bodega_origen_id={item.bodega_origen_id}, consecutive={getattr(item, 'consecutive', None)}", file=sys.stderr)
            created = service.crear_movimiento(item, usuario.id, consecutive)
            print(f"[DEBUG] created: id={created.id}, consecutive={created.consecutive}, bodega_origen_id={created.bodega_origen_id}", file=sys.stderr)
            if i == 0:
                consecutive = created.consecutive
            results.append(created)
        
        return results
    except Exception as e:
        traceback.print_exc()
        print(f"[DEBUG] Exception: {e}", file=sys.stderr)
        raise AppException(str(e))


@router.post("/entrada", response_model=MovimientoResponse)
def crear_entrada(data: MovimientoCreate, proveedor_id: int, db: Session = Depends(get_db),
                usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    data.proveedor_id = proveedor_id
    data.tipo = TipoMovimiento.ENTRADA
    
    try:
        service = MovimientoService(db)
        return service.entrada_bodega(data, proveedor_id, usuario.id)
    except AppException as e:
        raise e


@router.post("/salida", response_model=MovimientoResponse)
def crear_salida(data: MovimientoCreate, motivo: str, db: Session = Depends(get_db),
                usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    data.tipo = TipoMovimiento.SALIDA
    data.motivo = motivo
    
    try:
        service = MovimientoService(db)
        return service.salida_bodega(data, motivo, usuario.id)
    except AppException as e:
        raise e


@router.post("/transferencia", response_model=MovimientoResponse)
def crear_transferencia(data: MovimientoCreate, db: Session = Depends(get_db),
                     usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    data.tipo = TipoMovimiento.TRANSFERENCIA
    
    try:
        service = MovimientoService(db)
        return service.transferencia(data, usuario.id)
    except AppException as e:
        raise e


@router.get("/", response_model=List[MovimientoResponse])
def list_movimientos(tipo: Optional[TipoMovimiento] = None, producto_id: Optional[int] = None,
                    bodega_id: Optional[int] = None, skip: int = 0, limit: int = 100,
                    db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    import traceback
    try:
        service = MovimientoService(db)
        return service.get_all(skip, limit, tipo, producto_id, bodega_id)
    except Exception as e:
        traceback.print_exc()
        raise AppException(str(e))


@router.get("/tecnico/{tecnico_id}", response_model=List[MovimientoResponse])
def get_movimientos_tecnico(tecnico_id: int, skip: int = 0, limit: int = 100,
                            db: Session = Depends(get_db), usuario: Usuario = Depends(get_current_user)):
    service = MovimientoService(db)
    return service.get_by_tecnico(tecnico_id, skip, limit)


@router.get("/solicitud/{solicitud_id}", response_model=List[MovimientoResponse])
def get_movimientos_solicitud(solicitud_id: int, db: Session = Depends(get_db),
                             usuario: Usuario = Depends(get_current_user)):
    service = MovimientoService(db)
    return service.get_by_solicitud(solicitud_id)


@router.get("/orden/{orden_id}", response_model=List[MovimientoResponse])
def get_movimientos_orden(orden_id: int, db: Session = Depends(get_db),
                        usuario: Usuario = Depends(get_current_user)):
    service = MovimientoService(db)
    return service.get_by_orden(orden_id)


@router.put("/{consecutive}", response_model=MovimientoResponse)
def update_movimiento(consecutive: str, data: dict, db: Session = Depends(get_db),
                    usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = MovimientoService(db)
        return service.update_movimiento_by_consecutive(consecutive, data)
    except AppException as e:
        raise e


@router.delete("/{consecutive}")
def delete_movimiento(consecutive: str, db: Session = Depends(get_db),
                   usuario: Usuario = Depends(get_current_user)):
    if usuario.rol not in [RolUsuario.ADMIN, RolUsuario.SEMIADMIN]:
        raise UnauthorizedException("No autorizado")
    
    try:
        service = MovimientoService(db)
        service.delete_movimiento(consecutive)
        return {"message": "Eliminado"}
    except AppException as e:
        raise e


@router.get("/seriales-list/")
def list_seriales(db: Session = Depends(get_db)):
    from app.models.movimiento import Movimiento
    from app.models.producto import Producto
    from app.models.bodega import Bodega
    
    movimientos = db.query(Movimiento).filter(
        Movimiento.numero_serie.isnot(None),
        Movimiento.numero_serie != ''
    ).all()
    
    seriales_list = []
    for m in movimientos:
        if m.numero_serie:
            for serial in m.numero_serie.split('|'):
                if serial.strip():
                    producto = db.query(Producto).filter(Producto.id == m.producto_id).first()
                    bodega = db.query(Bodega).filter(Bodega.id == m.bodega_destino_id).first()
                    seriales_list.append({
                        "serial": serial.strip(),
                        "item": {"id": producto.id, "nombre": producto.nombre} if producto else None,
                        "bodega_actual": {"id": bodega.id, "nombre": bodega.nombre} if bodega else None,
                        "estado": "en_bodega",
                        "fecha_ingreso": m.fecha_creacion.isoformat() if m.fecha_creacion else None
                    })
    
    return seriales_list