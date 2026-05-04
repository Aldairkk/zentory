from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from datetime import datetime
import logging

from app.core.config import settings
from app.core.database import Base, engine
from app.core.exceptions import AppException
from app.routes import (
    auth_router,
    usuarios_router,
    productos_router,
    categorias_router,
    bodegas_router,
    proveedores_router,
    inventario_router,
    movimientos_router,
    solicitudes_router,
    ordenes_router,
)

logging.basicConfig(level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Zentory ERP - Sistema de Gestión de Inventario y Órdenes de Trabajo"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    logger.error(f"Error: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


app.include_router(auth_router, prefix="/api")
app.include_router(usuarios_router, prefix="/api")
app.include_router(productos_router, prefix="/api")
app.include_router(categorias_router, prefix="/api")
app.include_router(bodegas_router, prefix="/api")
app.include_router(proveedores_router, prefix="/api")
app.include_router(inventario_router, prefix="/api")
app.include_router(movimientos_router, prefix="/api")
app.include_router(solicitudes_router, prefix="/api")
app.include_router(ordenes_router, prefix="/api")

# Serve frontend
frontend_path = Path("/app/index.html")
if frontend_path.exists():
    @app.get("/")
    def serve_frontend():
        return FileResponse(frontend_path)


@app.on_event("startup")
def startup_event():
    logger.info("Creando tablas...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas")
    
    from app.core.database import SessionLocal
    from app.models import Usuario, RolUsuario, Bodega, Proveedor, Producto, Inventario, Movimiento, TipoMovimiento, Orden, EstadoOrden, Solicitud, Categoria
    from app.core.security import get_password_hash
    
    db = SessionLocal()
    try:
        # Create admin if not exists
        admin_exists = db.query(Usuario).filter(Usuario.email == settings.ADMIN_EMAIL).first()
        if not admin_exists:
            admin = Usuario(
                nombre="Administrador",
                apellido="Sistema",
                email=settings.ADMIN_EMAIL,
                password=get_password_hash(settings.ADMIN_PASSWORD),
                cargo="Administrador",
                rol=RolUsuario.ADMIN,
                estado=True
            )
            db.add(admin)
            db.commit()
            logger.info(f"Admin created: {settings.ADMIN_EMAIL}")
        else:
            logger.info("Admin already exists")
        
        # Create sample data if empty
        if db.query(Categoria).count() == 0:
            logger.info("Creating sample data...")
            
            # Categorías
            categorias = [
                Categoria(codigo="CAT001", nombre="Electrónica", descripcion="Dispositivos y componentes electrónicos"),
                Categoria(codigo="CAT002", nombre="Herramientas", descripcion="Herramientas de trabajo"),
                Categoria(codigo="CAT003", nombre="Materiales", descripcion="Materiales de construcción"),
                Categoria(codigo="CAT004", nombre="Insumos", descripcion="Insumos de oficina y generales"),
            ]
            db.add_all(categorias)
            db.commit()
            
            # Proveedores
            proveedores = [
                Proveedor(nit="12345678-9", nombre="Distribuidora Tech SPA", email="ventas@distech.cl", telefono="+56 2 2345 6789", ciudad="Santiago", direccion="Av. Principal 123, Santiago", estado=True),
                Proveedor(nit="98765432-1", nombre="Ferretería Industrial LTDA", email="contacto@ferreind.cl", telefono="+56 2 2345 1234", ciudad="Santiago", direccion="Calle Comercial 456, Santiago", estado=True),
                Proveedor(nit="45678912-3", nombre="Materiales yMás", email="pedro@materialesmas.cl", telefono="+56 2 2567 8901", ciudad="Santiago", direccion="Av. Construcc 789, Santiago", estado=True),
            ]
            db.add_all(proveedores)
            db.commit()
            
            # Bodegas
            bodegas = [
                Bodega(codigo="BO001", nombre="Bodega Central", ciudad="Santiago", direccion="Av. Industrial 100, Santiago", es_principal=True, estado=True),
                Bodega(codigo="BO002", nombre="Bodega A", ciudad="Santiago", direccion="Calle Almacén 200, Santiago", es_principal=False, estado=True),
                Bodega(codigo="BO003", nombre="Bodega B", ciudad="Santiago", direccion="Av. Logística 300, Santiago", es_principal=False, estado=True),
            ]
            db.add_all(bodegas)
            db.commit()
            
            # Productos (Items)
            productos = [
                # Serializados
                Producto(codigo="PROD001", nombre="Laptop Dell Latitude 5520", descripcion="Laptop 15.6 pulgadas, i7, 16GB RAM", categoria_id=1, proveedor_id=1, serializado=True, precio=850000, estado=True),
                Producto(codigo="PROD002", nombre="Monitor Samsung 27\"", descripcion="Monitor Full HD 27 pulgadas", categoria_id=1, proveedor_id=1, serializado=True, precio=180000, estado=True),
                # No serializados
                Producto(codigo="PROD003", nombre="Mouse Inalámbrico", descripcion="Mouse wireless USB", categoria_id=4, proveedor_id=1, serializado=False, precio=15000, estado=True),
                Producto(codigo="PROD004", nombre="Teclado Mecánico", descripcion="Teclado gamer RGB", categoria_id=4, proveedor_id=1, serializado=False, precio=45000, estado=True),
                Producto(codigo="PROD005", nombre="Destornillador Set 20 pzas", descripcion="Kit de destornilladores profesionales", categoria_id=2, proveedor_id=2, serializado=False, precio=35000, estado=True),
                Producto(codigo="PROD006", nombre="Cemento 25kg", descripcion="Saco de cemento Portland", categoria_id=3, proveedor_id=3, serializado=False, precio=12000, estado=True),
                Producto(codigo="PROD007", nombre="Cables HDMI 2m", descripcion="Cable HDMI de 2 metros", categoria_id=1, proveedor_id=1, serializado=False, precio=8000, estado=True),
                Producto(codigo="PROD008", nombre="Pendrive 64GB", descripcion="Memoria USB 64GB", categoria_id=4, proveedor_id=1, serializado=False, precio=12000, estado=True),
            ]
            db.add_all(productos)
            db.commit()
            
            # Usuarios técnicos
            tecnico1 = Usuario(
                nombre="Juan",
                apellido="Pérez",
                email="juan.perez@zentory.com",
                password=get_password_hash("Tecnico123!"),
                cargo="Técnico de Campo",
                rol=RolUsuario.TECNICO,
                estado=True
            )
            tecnico2 = Usuario(
                nombre="María",
                apellido="López",
                email="maria.lopez@zentory.com",
                password=get_password_hash("Tecnico123!"),
                cargo="Técnica de Campo",
                rol=RolUsuario.TECNICO,
                estado=True
            )
            db.add_all([tecnico1, tecnico2])
            db.commit()
            
            # Inventario (Stock)
            bodega_central = db.query(Bodega).filter(Bodega.codigo == "BO001").first()
            
            inventarios = [
                Inventario(producto_id=3, bodega_id=bodega_central.id, cantidad=50, stock_minimo=10),
                Inventario(producto_id=4, bodega_id=bodega_central.id, cantidad=30, stock_minimo=5),
                Inventario(producto_id=5, bodega_id=bodega_central.id, cantidad=25, stock_minimo=8),
                Inventario(producto_id=6, bodega_id=bodega_central.id, cantidad=100, stock_minimo=20),
                Inventario(producto_id=7, bodega_id=bodega_central.id, cantidad=40, stock_minimo=10),
                Inventario(producto_id=8, bodega_id=bodega_central.id, cantidad=60, stock_minimo=15),
            ]
            db.add_all(inventarios)
            db.commit()
            
            # Movimientos
            from datetime import datetime, timedelta
            
            movimientos = [
                Movimiento(consecutive="ING-001", tipo=TipoMovimiento.ENTRADA, producto_id=3, cantidad=50, bodega_destino_id=bodega_central.id, usuario_id=1, observaciones="Compra a proveedor", referencia="ALMACEN", fecha_movimiento=datetime.utcnow() - timedelta(days=5)),
                Movimiento(consecutive="ING-001", tipo=TipoMovimiento.ENTRADA, producto_id=4, cantidad=30, bodega_destino_id=bodega_central.id, usuario_id=1, observaciones="Compra a proveedor", referencia="ALMACEN", fecha_movimiento=datetime.utcnow() - timedelta(days=4)),
                Movimiento(consecutive="ING-001", tipo=TipoMovimiento.ENTRADA, producto_id=5, cantidad=25, bodega_destino_id=bodega_central.id, usuario_id=1, observaciones="Compra a proveedor", referencia="ALMACEN", fecha_movimiento=datetime.utcnow() - timedelta(days=3)),
                Movimiento(consecutive="ING-001", tipo=TipoMovimiento.ENTRADA, producto_id=6, cantidad=100, bodega_destino_id=bodega_central.id, usuario_id=1, observaciones="Compra a proveedor", referencia="ALMACEN", fecha_movimiento=datetime.utcnow() - timedelta(days=2)),
                Movimiento(consecutive="ING-002", tipo=TipoMovimiento.ENTRADA, producto_id=7, cantidad=40, bodega_destino_id=bodega_central.id, usuario_id=1, observaciones="Compra a proveedor", referencia="ALMACEN", fecha_movimiento=datetime.utcnow() - timedelta(days=1)),
                Movimiento(consecutive="SAL-001", tipo=TipoMovimiento.SALIDA, producto_id=7, cantidad=10, bodega_origen_id=bodega_central.id, usuario_id=1, observaciones="Asignación a técnico", referencia="CAMPO", fecha_movimiento=datetime.utcnow() - timedelta(hours=12)),
            ]
            db.add_all(movimientos)
            db.commit()
            
            # Órdenes de Trabajo
            ordenes_trabajo = [
                Orden(codigo="OT-001", descripcion="Instalación de red en oficina central", tecnico_id=tecnico1.id, fecha_inicio=datetime.utcnow() - timedelta(days=2), estado=EstadoOrden.EN_PROCESO),
                Orden(codigo="OT-002", descripcion="Mantenimiento de equipos en bodega A", tecnico_id=tecnico2.id, fecha_inicio=datetime.utcnow() - timedelta(days=1), estado=EstadoOrden.PENDIENTE),
                Orden(codigo="OT-003", descripcion="Configuración de servidores", tecnico_id=tecnico1.id, fecha_inicio=datetime.utcnow() + timedelta(days=1), estado=EstadoOrden.PENDIENTE),
            ]
            db.add_all(ordenes_trabajo)
            db.commit()
            
            logger.info("Sample data created successfully")
        
    except Exception as e:
        logger.error(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Zentory ERP API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)