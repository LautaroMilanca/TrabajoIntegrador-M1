# Proyecto Integrador 1 – Configuración de Base de Datos y Carga de Datos

## PI 1: Configurar el entorno de base de datos

### PostgreSQL

Se optó por **PostgreSQL** debido a su compatibilidad con SQL. Además, es software libre y se integra fácilmente con herramientas como **DBeaver** y **Python**.

### Docker

Para garantizar un entorno controlado, reproducible y aislado, se utilizó **Docker** para levantar una instancia de PostgreSQL.  
El contenedor se configuró con los siguientes parámetros:

- **Nombre del contenedor**: `ecommerce-db`
- **Usuario**: `admin`
- **Contraseña**: `admin123`
- **Base de datos inicial**: `ecommerce`
- **Puerto expuesto**: `5432`

#### Comando utilizado:

```bash
docker run --name ecommerce-db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin123 \
  -e POSTGRES_DB=ecommerce \
  -p 5432:5432 \
  -d postgres:15
```

### DBeaver

Se utilizó **DBeaver** como cliente SQL para conectarse a la base, ejecutar scripts, crear tablas y gestionar los datos de manera gráfica.  
Una vez ejecutado el contenedor, se estableció la conexión desde DBeaver y se verificó su funcionamiento creando y visualizando tablas, ejecutando consultas y cargando datos de prueba.

---

## PI 2: Crear las tablas y cargar los datos

###  Crear las tablas utilizando los scripts SQL proporcionados

Para estructurar correctamente la información contenida en los archivos `.csv`, se utilizaron scripts SQL adaptados a PostgreSQL.  
Las tablas fueron creadas en la base de datos `ecommerce` levantada mediante un contenedor Docker.

Las tablas creadas fueron:

- `usuarios`
- `categorias`
- `productos`
- `ordenes`
- `detalleordenes`
- `direccionesenvio`
- `carrito`
- `metodospago`
- `ordenesmetodospago`
- `resenasproductos`
- `historialpagos`

### Importar datos desde archivos CSV

Una vez creadas las tablas, se procedió a importar los datos desde archivos `.csv` provistos.  
Estos archivos contenían información relevante para poblar las distintas entidades del modelo: usuarios, productos, órdenes, métodos de pago, entre otros.

### Script de carga: `ValidaciondeDatos.py`

Para automatizar este proceso y validar la integridad de los datos, se desarrolló un script en Python llamado `ValidaciondeDatos.py`, utilizando las librerías `pandas`, `sqlalchemy` y `psycopg2`. El script realiza las siguientes acciones:

1. **Lee todos los archivos `.csv`** ubicados en la carpeta local `/Cvs` y los carga como `DataFrame`.
2. **Convierte todos los nombres de columnas a minúsculas**, garantizando compatibilidad con PostgreSQL.
3. **Valida claves foráneas** antes de insertar registros:
   - Que los `usuarioid` en la tabla `ordenes` existan en `usuarios`.
   - Que los `categoriaid` en `productos` existan en `categorias`.
4. **Carga los datos válidos** a la base de datos, descartando automáticamente aquellos registros que no cumplan las relaciones de integridad.

---

