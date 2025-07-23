-- Tabla: Usuarios
CREATE TABLE Usuarios (
    UsuarioID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    DNI VARCHAR(20) UNIQUE NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Contraseña VARCHAR(255) NOT NULL,
    FechaRegistro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Categorías
CREATE TABLE Categorias (
    CategoriaID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(255)
);

-- Tabla: Productos
CREATE TABLE Productos (
    ProductoID SERIAL PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Descripcion TEXT,
    Precio NUMERIC(10,2) NOT NULL,
    Stock INT NOT NULL,
    CategoriaID INT REFERENCES Categorias(CategoriaID)
);

-- Tabla: Órdenes
CREATE TABLE Ordenes (
    OrdenID SERIAL PRIMARY KEY,
    UsuarioID INT REFERENCES Usuarios(UsuarioID),
    FechaOrden TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Total NUMERIC(10,2) NOT NULL,
    Estado VARCHAR(50) DEFAULT 'Pendiente'
);

-- Tabla: Detalle de Órdenes
CREATE TABLE DetalleOrdenes (
    DetalleID SERIAL PRIMARY KEY,
    OrdenID INT REFERENCES Ordenes(OrdenID),
    ProductoID INT REFERENCES Productos(ProductoID),
    Cantidad INT NOT NULL,
    PrecioUnitario NUMERIC(10,2) NOT NULL
);

-- Tabla: Direcciones de Envío
CREATE TABLE DireccionesEnvio (
    DireccionID SERIAL PRIMARY KEY,
    UsuarioID INT REFERENCES Usuarios(UsuarioID),
    Calle VARCHAR(255) NOT NULL,
    Ciudad VARCHAR(100) NOT NULL,
    Departamento VARCHAR(100),
    Provincia VARCHAR(100),
    Distrito VARCHAR(100),
    Estado VARCHAR(100),
    CodigoPostal VARCHAR(20),
    Pais VARCHAR(100) NOT NULL
);

-- Tabla: Carrito de Compras
CREATE TABLE Carrito (
    CarritoID SERIAL PRIMARY KEY,
    UsuarioID INT REFERENCES Usuarios(UsuarioID),
    ProductoID INT REFERENCES Productos(ProductoID),
    Cantidad INT NOT NULL,
    FechaAgregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Métodos de Pago
CREATE TABLE MetodosPago (
    MetodoPagoID SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(255)
);

-- Tabla: Ordenes Métodos de Pago
CREATE TABLE OrdenesMetodosPago (
    OrdenMetodoID SERIAL PRIMARY KEY,
    OrdenID INT REFERENCES Ordenes(OrdenID),
    MetodoPagoID INT REFERENCES MetodosPago(MetodoPagoID),
    MontoPagado NUMERIC(10,2) NOT NULL
);

-- Tabla: Reseñas de Productos
CREATE TABLE ResenasProductos (
    ResenaID SERIAL PRIMARY KEY,
    UsuarioID INT REFERENCES Usuarios(UsuarioID),
    ProductoID INT REFERENCES Productos(ProductoID),
    Calificacion INT CHECK (Calificacion >= 1 AND Calificacion <= 5),
    Comentario TEXT,
    Fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla: Historial de Pagos
CREATE TABLE HistorialPagos (
    PagoID SERIAL PRIMARY KEY,
    OrdenID INT REFERENCES Ordenes(OrdenID),
    MetodoPagoID INT REFERENCES MetodosPago(MetodoPagoID),
    Monto NUMERIC(10,2) NOT NULL,
    FechaPago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    EstadoPago VARCHAR(50) DEFAULT 'Procesando'
);
