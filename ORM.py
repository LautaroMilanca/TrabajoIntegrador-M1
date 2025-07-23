
from sqlalchemy import create_engine, select, func, desc, extract, cast, Integer
from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy.sql import text

Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    usuarioid = Column(Integer, primary_key=True)
    fecharegistro = Column(DateTime)

class Producto(Base):
    __tablename__ = 'productos'
    productoid = Column(Integer, primary_key=True)
    nombre = Column(String)
    stock = Column(Integer)
    precio = Column(Numeric)
    categoriaid = Column(Integer)

class Categoria(Base):
    __tablename__ = 'categorias'
    categoriaid = Column(Integer, primary_key=True)
    nombre = Column(String)

class Orden(Base):
    __tablename__ = 'ordenes'
    ordenid = Column(Integer, primary_key=True)
    usuarioid = Column(Integer)
    fechaorden = Column(DateTime)
    total = Column(Numeric)

class DetalleOrden(Base):
    __tablename__ = 'detalleordenes'
    detalleid = Column(Integer, primary_key=True)
    ordenid = Column(Integer)
    productoid = Column(Integer)
    cantidad = Column(Integer)
    preciounitario = Column(Numeric)

class MetodoPago(Base):
    __tablename__ = 'metodospago'
    metodopagoid = Column(Integer, primary_key=True)
    nombre = Column(String)

class OrdenMetodoPago(Base):
    __tablename__ = 'ordenesmetodospago'
    ordenmetodoid = Column(Integer, primary_key=True)
    ordenid = Column(Integer)
    metodopagoid = Column(Integer)
    montopagado = Column(Numeric)

class HistorialPago(Base):
    __tablename__ = 'historialpagos'
    pagoid = Column(Integer, primary_key=True)
    ordenid = Column(Integer)
    metodopagoid = Column(Integer)
    monto = Column(Numeric)
    fechapago = Column(DateTime)
    estadopago = Column(String)

class Resena(Base):
    __tablename__ = 'resenasproductos'
    resenaid = Column(Integer, primary_key=True)
    usuarioid = Column(Integer)
    productoid = Column(Integer)
    calificacion = Column(Integer)

engine = create_engine("postgresql+psycopg2://admin:admin123@localhost:5432/ecommerce")

with Session(engine) as session:
    print("\n Productos más vendidos por volumen:")
    resultado = session.query(Producto.nombre, func.sum(DetalleOrden.cantidad).label("total_vendido"))\
        .join(DetalleOrden, Producto.productoid == DetalleOrden.productoid)\
        .group_by(Producto.nombre).order_by(desc("total_vendido")).limit(5).all()
    for nombre, total in resultado:
        print(f"- {nombre}: {total} unidades")

    print("\n Ticket promedio por orden:")
    print(session.query(func.avg(Orden.total)).scalar())

    print("\n Categorías con más productos vendidos:")
    resultado = session.query(Categoria.nombre, func.sum(DetalleOrden.cantidad).label("total_vendido"))\
        .join(Producto, Categoria.categoriaid == Producto.categoriaid)\
        .join(DetalleOrden, Producto.productoid == DetalleOrden.productoid)\
        .group_by(Categoria.nombre).order_by(desc("total_vendido")).limit(5).all()
    for nombre, total in resultado:
        print(f"- {nombre}: {total} unidades")

    print("\n Día de la semana con más ventas:")
    resultado = session.query(func.to_char(Orden.fechaorden, 'Day'), func.count()).group_by(1).order_by(desc(2)).all()
    for dia, cantidad in resultado:
        print(f"- {dia.strip()}: {cantidad} órdenes")

    print("\n Órdenes por mes:")
    resultado = session.query(func.date_trunc('month', Orden.fechaorden).label("mes"), func.count())\
        .group_by("mes").order_by("mes").all()
    for mes, cant in resultado:
        print(f"{mes.date()}: {cant} órdenes")

    print("\n Métodos de pago más utilizados:")
    resultado = session.query(MetodoPago.nombre, func.count(OrdenMetodoPago.ordenid))\
        .join(OrdenMetodoPago, MetodoPago.metodopagoid == OrdenMetodoPago.metodopagoid)\
        .group_by(MetodoPago.nombre).order_by(desc(2)).all()
    for nombre, cantidad in resultado:
        print(f"{nombre}: {cantidad} veces")

    print("\n  Monto promedio pagado por método:")
    resultado = session.query(MetodoPago.nombre, func.avg(OrdenMetodoPago.montopagado))\
        .join(OrdenMetodoPago, MetodoPago.metodopagoid == OrdenMetodoPago.metodopagoid)\
        .group_by(MetodoPago.nombre).all()
    for nombre, promedio in resultado:
        print(f"{nombre}: ${promedio:.2f}")

    print("\n  Órdenes con más de un método de pago:")
    resultado = session.query(OrdenMetodoPago.ordenid).group_by(OrdenMetodoPago.ordenid)\
        .having(func.count(OrdenMetodoPago.metodopagoid) > 1).count()
    print(f"{resultado} órdenes")

    print("\n  Pagos 'Procesando' o 'Fallido':")
    resultado = session.query(func.count()).select_from(HistorialPago)\
        .filter(HistorialPago.estadopago.in_(['Procesando', 'Fallido'])).scalar()
    print(f"{resultado} pagos")

    print("\n Monto total recaudado por mes:")
    resultado = session.query(func.date_trunc('month', HistorialPago.fechapago), func.sum(HistorialPago.monto))\
        .group_by(1).order_by(1).all()
    for mes, total in resultado:
        print(f"{mes.date()}: ${total:.2f}")

    print("\n Usuarios registrados por mes:")
    resultado = session.query(func.date_trunc('month', Usuario.fecharegistro), func.count())\
        .group_by(1).order_by(1).all()
    for mes, total in resultado:
        print(f"{mes.date()}: {total} usuarios")

    print("\n  Usuarios con más de una orden:")
    resultado = session.query(Orden.usuarioid).group_by(Orden.usuarioid).having(func.count() > 1).count()
    print(f"{resultado} usuarios")

    print("\n Usuarios sin órdenes:")
    resultado = session.execute(text("""
        SELECT COUNT(*) FROM usuarios u
        LEFT JOIN ordenes o ON u.usuarioid = o.usuarioid
        WHERE o.ordenid IS NULL
    """)).scalar()
    print(f"{resultado} usuarios")

    print("\n  Usuarios que más gastaron:")
    resultado = session.query(Orden.usuarioid, func.sum(Orden.total).label("gasto"))\
        .group_by(Orden.usuarioid).order_by(desc("gasto")).limit(5).all()
    for uid, gasto in resultado:
        print(f"Usuario {uid}: ${gasto:.2f}")

    print("\n  Usuarios que dejaron reseñas:")
    resultado = session.query(func.count(func.distinct(Resena.usuarioid))).scalar()
    print(f"{resultado} usuarios")

    print("\n  Productos con alto stock y bajas ventas:")
    resultado = session.query(Producto.nombre, Producto.stock, func.coalesce(func.sum(DetalleOrden.cantidad), 0).label("vendido"))\
        .outerjoin(DetalleOrden, Producto.productoid == DetalleOrden.productoid)\
        .group_by(Producto.nombre, Producto.stock)\
        .having(Producto.stock > 50).order_by("vendido").limit(5).all()
    for nombre, stock, vendido in resultado:
        print(f"{nombre}: stock={stock}, vendidos={vendido}")

    print("\n  Productos fuera de stock:")
    resultado = session.query(Producto).filter(Producto.stock == 0).all()
    for p in resultado:
        print(f"{p.nombre}")

    print("\n  Productos peor calificados:")
    resultado = session.query(Producto.nombre, func.avg(Resena.calificacion).label("promedio"))\
        .join(Resena, Producto.productoid == Resena.productoid)\
        .group_by(Producto.nombre).order_by("promedio").limit(5).all()
    for nombre, cal in resultado:
        print(f"{nombre}: {cal:.2f}")

    print("\n  Productos con más reseñas:")
    resultado = session.query(Producto.nombre, func.count(Resena.resenaid).label("nresenas"))\
        .join(Resena, Producto.productoid == Resena.productoid)\
        .group_by(Producto.nombre).order_by(desc("nresenas")).limit(5).all()
    for nombre, cantidad in resultado:
        print(f"{nombre}: {cantidad} reseñas")

    print("\n  Categoría con mayor valor económico vendido:")
    resultado = session.query(Categoria.nombre, func.sum(DetalleOrden.preciounitario * DetalleOrden.cantidad))\
        .join(Producto, Categoria.categoriaid == Producto.categoriaid)\
        .join(DetalleOrden, Producto.productoid == DetalleOrden.productoid)\
        .group_by(Categoria.nombre).order_by(desc(2)).limit(1).all()
    for nombre, total in resultado:
        print(f"{nombre}: ${total:.2f}")
