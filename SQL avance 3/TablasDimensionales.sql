-- Dimensión Usuario (SCD Tipo 2)
CREATE TABLE dim_usuario (
    usuario_sk SERIAL PRIMARY KEY,
    usuario_id INT,
    nombre VARCHAR(100),
    email VARCHAR(255),
    fecha_registro DATE,
    fecha_inicio DATE,
    fecha_fin DATE,
    es_actual BOOLEAN DEFAULT TRUE
);

-- Dimensión Producto (SCD Tipo 2)
CREATE TABLE dim_producto (
    producto_sk SERIAL PRIMARY KEY,
    producto_id INT,
    nombre VARCHAR(255),
    descripcion TEXT,
    precio NUMERIC(10, 2),
    stock INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    es_actual BOOLEAN DEFAULT TRUE
);

-- Dimensión Categoría (SCD Tipo 1)
CREATE TABLE dim_categoria (
    categoria_sk SERIAL PRIMARY KEY,
    categoria_id INT,
    nombre VARCHAR(100),
    descripcion VARCHAR(255)
);

-- Dimensión Método de Pago (SCD Tipo 2)
CREATE TABLE dim_metodopago (
    metodopago_sk SERIAL PRIMARY KEY,
    metodopago_id INT,
    nombre VARCHAR(100),
    descripcion VARCHAR(255),
    fecha_inicio DATE,
    fecha_fin DATE,
    es_actual BOOLEAN DEFAULT TRUE
);

-- Dimensión Fecha Orden
CREATE TABLE dim_fecha_orden (
    fecha DATE PRIMARY KEY,
    anio INT,
    mes INT,
    dia INT,
    semana INT,
    dia_semana VARCHAR(20)
);

-- Dimensión Estado de Pago
CREATE TABLE dim_estado_pago (
    estado_pago_sk SERIAL PRIMARY KEY,
    estado VARCHAR(50)
);