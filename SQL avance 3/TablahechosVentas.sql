CREATE TABLE hechos_ventas (
    venta_id SERIAL PRIMARY KEY,
    usuario_sk INT REFERENCES dim_usuario (usuario_sk),
    producto_sk INT REFERENCES dim_producto (producto_sk),
    categoria_sk INT REFERENCES dim_categoria (categoria_sk),
    metodopago_sk INT REFERENCES dim_metodopago (metodopago_sk),
    fecha DATE REFERENCES dim_fecha_orden (fecha),
    estado_pago_sk INT REFERENCES dim_estado_pago (estado_pago_sk),
    cantidad INT,
    precio_unitario NUMERIC(10, 2),
    total NUMERIC(10, 2),
    fecha_orden TIMESTAMP
);