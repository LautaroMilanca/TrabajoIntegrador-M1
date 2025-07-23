import pandas as pd
from sqlalchemy import create_engine
import os

# Conexión a PostgreSQL
engine = create_engine("postgresql+psycopg2://admin:admin123@localhost:5432/ecommerce")

# Ruta relativa a carpeta 'Cvs'
ruta = os.path.join(os.getcwd(), "Cvs")

# Mapeo de archivos CSV a tablas
archivos = {
    "2.Usuarios.csv": "usuarios",
    "3.Categorias.csv": "categorias",
    "4.Productos.csv": "productos",
    "5.Ordenes.csv": "ordenes",
    "6.detalle_ordenes.csv": "detalleordenes",
    "7.direcciones_envio.csv": "direccionesenvio",
    "8.Carrito.csv": "carrito",
    "9.metodos_pago.csv": "metodospago",
    "10.ordenes_metodospago.csv": "ordenesmetodospago",
    "11.resenas_productos.csv": "resenasproductos",
    "12.historial_pagos.csv": "historialpagos"
}

# Validaciones por clave foránea
validadores = {
    "ordenes": [("usuarioid", "usuarios")],
    "productos": [("categoriaid", "categorias")],
    "detalleordenes": [("ordenid", "ordenes"), ("productoid", "productos")],
    "direccionesenvio": [("usuarioid", "usuarios")],
    "carrito": [("usuarioid", "usuarios"), ("productoid", "productos")],
    "resenasproductos": [("usuarioid", "usuarios"), ("productoid", "productos")],
    "ordenesmetodospago": [("ordenid", "ordenes"), ("metodopagoid", "metodospago")],
    "historialpagos": [("ordenid", "ordenes"), ("metodopagoid", "metodospago")]
}

# Carga con validación
for archivo, tabla in archivos.items():
    path = os.path.join(ruta, archivo)
    try:
        df = pd.read_csv(path)
        df.columns = df.columns.str.lower()
        if tabla in validadores:
            for columna, tabla_ref in validadores[tabla]:
                ref_ids = pd.read_sql(f"SELECT {columna} FROM {tabla_ref}", engine)
                df = df[df[columna].isin(ref_ids[columna])]
        
        print(f"Cargando {archivo} en la tabla {tabla}...")
        df.to_sql(tabla, engine, if_exists="append", index=False)
    except Exception as e:
        print(f"Error en {archivo} → {e}")

