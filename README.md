# Primer avance 

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

## PI 3: Preparar y transformar los datos

### Identificación de columnas semi-estructuradas

Se analizaron los archivos `.csv` cargados y se identificaron columnas con potencial semi-estructurado:

- `descripcion` en `productos.csv`: contiene textos complejos que podrían contener keywords relevantes.
- `fechaagregado` en `carrito.csv`: contiene fecha y hora que pueden separarse para facilitar análisis.

### Transformaciones realizadas

Se desarrolló el notebook `Transformaciones.ipynb`, donde se aplicaron las siguientes acciones:

- Separación de `fechaagregado` en `fecha` y `hora`.
- Conversión de descripciones a minúsculas y detección de palabras clave.


## PI 4: Explorar los datos

### Consultas SQL 

Se creó el script `Querys.sql` con un conjunto de queries en SQL para detectar problemas comunes de calidad de datos, como:

- Claves foráneas huérfanas
- Productos sin stock 
- Pagos con estados inválidos

### ORM

Se desarrolló el script `ORM.py` utilizando **SQLAlchemy ORM** para responder a preguntas clave del negocio.

## PI 5: Identificar estructura y relaciones

### Llaves primarias y foráneas

**Llaves primarias:**

- `usuarios.usuarioid`
- `categorias.categoriaid`
- `productos.productoid`
- `ordenes.ordenid`
- `detalleordenes.detalleid`
- `direccionesenvio.direccionid`
- `carrito.carritoid`
- `metodospago.metodopagoid`
- `ordenesmetodospago.ordenmetodoid`
- `resenasproductos.resenaid`
- `historialpagos.pagoid`

**Llaves foráneas:**

- `ordenes.usuarioid` → `usuarios.usuarioid`
- `productos.categoriaid` → `categorias.categoriaid`
- `detalleordenes.ordenid` → `ordenes.ordenid`
- `detalleordenes.productoid` → `productos.productoid`
- `ordenesmetodospago.ordenid` → `ordenes.ordenid`
- `ordenesmetodospago.metodopagoid` → `metodospago.metodopagoid`
- `historialpagos.ordenid` → `ordenes.ordenid`
- `historialpagos.metodopagoid` → `metodospago.metodopagoid`
- `resenasproductos.usuarioid` → `usuarios.usuarioid`
- `resenasproductos.productoid` → `productos.productoid`
- `direccionesenvio.usuarioid` → `usuarios.usuarioid`
- `carrito.usuarioid` → `usuarios.usuarioid`
- `carrito.productoid` → `productos.productoid`

### Atributos clave para responder preguntas de negocio

Para responder las preguntas propuestas, se identificaron los siguientes atributos relevantes:

| Pregunta de negocio                         | Atributos clave                                                                    |
| ------------------------------------------- | ---------------------------------------------------------------------------------- |
| Productos más vendidos por volumen          | `detalleordenes.cantidad`, `productos.nombre`                                      |
| Ticket promedio por orden                   | `ordenes.total`                                                                    |
| Categorías con más productos vendidos       | `productos.categoriaid`, `detalleordenes.cantidad`                                 |
| Día de la semana con más ventas             | `ordenes.fechaorden`                                                               |
| Variación de órdenes por mes                | `ordenes.fechaorden`, `ordenes.ordenid`                                            |
| Métodos de pago más utilizados              | `ordenesmetodospago.metodopagoid`                                                  |
| Monto promedio por método de pago           | `ordenesmetodospago.montopagado`                                                   |
| Órdenes con múltiples métodos de pago       | `ordenesmetodospago.ordenid` (agrupadas)                                           |
| Pagos en estado 'Procesando' o 'Fallido'    | `historialpagos.estadopago`                                                        |
| Recaudación mensual                         | `historialpagos.monto`, `historialpagos.fechapago`                                 |
| Altas de usuarios por mes                   | `usuarios.fecharegistro`                                                           |
| Usuarios con más de una orden               | `ordenes.usuarioid` (agrupados)                                                    |
| Usuarios sin órdenes                        | `usuarios.usuarioid`, `ordenes.usuarioid`                                          |
| Usuarios que más gastaron                   | `ordenes.usuarioid`, `ordenes.total`                                               |
| Usuarios que dejaron reseñas                | `resenasproductos.usuarioid`                                                       |
| Productos con alto stock y bajas ventas     | `productos.stock`, `detalleordenes.productoid`                                     |
| Productos fuera de stock                    | `productos.stock` = 0                                                              |
| Productos peor calificados                  | `resenasproductos.calificacion`                                                    |
| Productos con más reseñas                   | `resenasproductos.productoid` (conteo)                                             |
| Categoría con mayor valor económico vendido | `detalleordenes.cantidad * detalleordenes.preciounitario`, `productos.categoriaid` |

## PI 6: Evaluar la calidad de los datos

### Análisis realizado

Para detectar problemas de calidad en los datos, se utilizaron dos enfoques complementarios:

1. **Consultas SQL en el script `Querys.sql`**, que detectaron:
   - Claves foráneas inválidas.
   - Pagos con estados inválidos.
   - Entre otras

2. **ORM en `ORM.py`**, donde se aplicaron filtros y funciones agregadas para:
   - Contar productos con stock cero
   - Validar la existencia de múltiples métodos de pago por orden
   - Calcular medias, totales y agrupaciones que revelan anomalías en los datos
   - Entre otras

### Inconsistencias detectadas

- Registros con claves foráneas que no existen en las tablas principales.
- Órdenes sin pagos asociados
- Pagos con estado `NULL`, `Procesando` o `Fallido`
- Entre otras

### Acciones  aplicadas

- Se desarrolló el script `ValidaciondeDatos.py` que descarta automáticamente los registros con claves foráneas inválidas antes de insertarlos.
- Se estandarizaron nombres de columnas y se transformaron fechas y campos textuales para mejorar su limpieza y análisis.
- Se documentaron los errores para su posterior revisión o depuración.

# Segundo avance 

## PI 1: Análisis de negocio y descubrimiento de requisitos

### Objetivos del negocio

A partir de las preguntas planteadas, el negocio desea:

- Conocer los **productos más vendidos** y los **peor calificados**.
- Detectar **usuarios que más compran**.
- Evaluar el **rendimiento de categorías** y su valor económico generado.
- Medir el uso y efectividad de **métodos de pago**.
- Controlar **órdenes por período**, **ticket promedio**, y **ventas por día**.
- Supervisar el **estado de los pagos** y el **almacenamiento de stock**.

### Datos disponibles

A través del modelado de base de datos relacional y la carga de archivos CSV, podemos obtener la siguiente informacion:

- Detalles de cada producto (`productos`, `categorias`)
- Información completa de los usuarios (`usuarios`)
- Reseñas de productos (`resenasproductos`)
- Transacciones de compra (`ordenes`, `detalleordenes`)
- Pagos realizados y sus métodos (`historialpagos`, `ordenesmetodospago`, `metodospago`)
- Información de stock y carrito (`carrito`)
- Direcciones y fechas de envío (`direccionesenvio`)

## PI 2: Identificación de componentes del modelo dimensional
### Hechos (Fact Tables)

Se nombra a contiuacion los  hechos  para el modelo dimensional:

- **HechoDetalleOrdenes**: permite calcular métricas como:
  - `cantidad` de productos vendidos
  - `precio_unitario` de cada ítem
  - `total_linea` (cantidad * precio_unitario)

- **HechoOrdenes**: registra:
  - `total` por orden
  - `estado` de la orden

- **HechoPagos**: toma información de las tablas `historialpagos` y `ordenesmetodospago`:
  - `montopagado`
  - `estado_pago`
  - permite analizar múltiples métodos de pago por orden

---

### Dimensiones

Las siguientes dimensiones fueron diseñadas para permitir el análisis por filtros y agrupaciones:

- **dim_usuario**: incluye información del cliente (`nombre`, `email`, `fecharegistro`)
- **dim_producto**: incluye `nombre`, `descripcion`, `precio`, `stock`
- **dim_categoria**: describe el tipo de producto
- **dim_metodopago**: describe cómo se pagó la orden
- **dim_fecha_orden**: extraída de `ordenes.fechaorden`, con descomposición en año, mes, día, semana, día de la semana
- **dim_estado_pago**: para evaluar el estado de los pagos ('Procesando', 'Fallido', 'Completado', etc.)


### Esquema estrella
Se diseñó un modelo dimensional en forma de estrella siguiendo la metodología de Kimball, centrado en la tabla de **HechoDetalleOrdenes**. Este modelo permite responder de forma eficiente a las preguntas del negocio relacionadas con ventas, productos, clientes y pagos.

                          dim_usuario
                               |
                          dim_producto ---- dim_categoria
                               |
       dim_fecha_orden --- detalleordenes --- dim_metodopago
                               |
                         historialpagos / ordenesmetodospago

## PI 3: Diseño del modelo de datos

### Slowly Changing Dimensions (SCD)

Para capturar la evolución de los datos en el tiempo y preservar el historial relevante para el análisis, se aplicaron estrategias de Slowly Changing Dimensions (SCD):

- **`dim_categoria` – SCD Tipo 1**  
  Se espera que los cambios en categorías (como nombre o descripción) sean meras correcciones. No es necesario conservar el valor anterior.

- **`dim_usuario` – SCD Tipo 2**  
  Atributos como nombre, email o fecha de registro pueden cambiar. Se conservará historial mediante columnas como:  
  - `fecha_inicio`  
  - `fecha_fin`  
  - `es_actual`

- **`dim_producto` – SCD Tipo 2**  
  Cambios en precio, stock o descripción impactan el análisis histórico. Se aplicará versión temporal con los mismos campos de control que en `dim_usuario`.

- **`dim_metodopago` – SCD Tipo 2**  
  Aunque es menos frecuente, si se modifican las descripciones o condiciones de un método de pago, se conservará el historial.

- **`dim_fecha_orden` – No aplica SCD**  
  Las fechas son inmutables. Esta dimensión es puramente derivada y no requiere versionado.

- **`dim_estado_pago` – No aplica SCD**  
  Los estados son categóricos y fijos. Si bien pueden cambiar a lo largo del proceso (por ejemplo, de "Procesando" a "Completado"), eso se maneja desde la tabla de hechos o de eventos, no como SCD en la dimensión.


## PI 4: Documentación y comunicación del modelo

### Diagrama Entidad-Relación (ER)

Se construyó un **modelo en estrella** para representar el esquema dimensional de la base de datos de e-commerce. Este modelo facilita la exploración y el análisis de los datos, estructurándolos en torno a una tabla de hechos central y múltiples dimensiones.

#### Estructura del modelo:

- **Hecho principal**:
  - `detalleordenes`: representa cada ítem comprado en una orden, incluyendo cantidad y precio unitario.

- **Dimensiones conectadas**:
  - `dim_usuario`: información del cliente (`nombre`, `email`, `fecharegistro`).
  - `dim_producto`: detalles del producto (`nombre`, `descripcion`, `precio`, `stock`).
  - `dim_categoria`: categoría del producto.
  - `dim_metodopago`: método utilizado en la transacción.
  - `dim_fecha_orden`: fecha de la compra, descompuesta en año, mes, día, semana, día de la semana.
  - `dim_estado_pago`: estado del pago (procesando, completado, fallido, etc.).

### Justificación del diseño

- Se utilizó la **metodología Kimball**, priorizando la simplicidad, claridad y eficiencia de consultas analíticas.
- Las dimensiones fueron seleccionadas cuidadosamente para cubrir los ejes más relevantes del análisis de negocio: producto, usuario, tiempo, método de pago y estado de la transacción.
- Se aplicaron estrategias de Slowly Changing Dimensions (SCD) donde fue necesario mantener el historial de cambios (tipo 2 en `dim_usuario`, `dim_producto`, `dim_metodopago`).
- La dimensión `dim_fecha_orden` permite análisis temporales flexibles (por día, semana, mes).
- Se normalizó el estado del pago (`dim_estado_pago`) para facilitar reportes sobre transacciones pendientes, fallidas o completadas.


# Tercer avance 

## PI 1: Modelo

### Implementación del modelo físico en SQL

Se implementaron los scripts SQL correspondientes a la capa de análisis. El modelo se basa en una arquitectura en estrella, donde:

- `hechos_ventas` representa la tabla de hechos principal.
- Las tablas dimensionales (`dim_usuario`, `dim_producto`, `dim_categoria`, `dim_metodopago`, `dim_fecha_orden`, `dim_estado_pago`) proveen contexto para analizar las métricas de negocio.

Los scripts fueron organizados en la carpeta:

```
SQL avance 3/
├── TablahechosVentas.sql
├── TablasDimensionales.sql
```

## PI 2: Transformación

En esta etapa tenía previsto realizar la transformación completa de los datos utilizando **DBT (Data Build Tool)**.
Por cuestiones de tiempo, no llegué a implementarlo completamente, pero definí el plan detallado que seguiría para garantizar limpieza, trazabilidad y análisis eficiente.

### Plan de transformación definido

#### 1. Limpieza y normalización de datos

En una primera capa de staging (bronze → silver), **hubiese aplicado transformaciones iniciales** sobre las tablas crudas para asegurar calidad. Algunas tareas planificadas fueron:

- Convertir los tipos de datos apropiadamente (por ejemplo, `fechaorden` a `DATE`).
- Aplicar limpieza de strings (`LOWER`, `TRIM`, eliminación de espacios) para unificar formatos en campos como `email`, `nombre`, etc.
- Detectar y remover duplicados.
- Validar claves foráneas y registros huérfanos.
- Normalizar formatos y asegurar consistencia semántica entre tablas.

#### 2. Creación de tablas de hechos y dimensiones

En la capa silver/gold, tenía diseñado crear:

- **Tablas dimensionales**: `dim_usuario`, `dim_producto`, `dim_categoria`, `dim_metodopago`, `dim_fecha`, `dim_estado_pago`, cada una con sus atributos clave para análisis por segmentos.
- **Tabla de hechos**: `hechos_ventas`, que incluiría métricas clave como cantidad, precio unitario, total por línea, y claves foráneas hacia las dimensiones.

Estas transformaciones se hubiesen construido en modelos `.sql` dentro de la estructura de carpetas de DBT, con dependencias bien definidas.

#### 3. Slowly Changing Dimensions (SCD)

Otra de las transformaciones que tenía planificado implementar era el manejo de **dimensiones que cambian con el tiempo**. En particular:

- **SCD Tipo 1** para `dim_categoria`, ya que los cambios no necesitan conservar historial.
- **SCD Tipo 2** para `dim_usuario`, `dim_producto`, `dim_metodopago`, incorporando columnas como `fecha_inicio`, `fecha_fin` y `es_actual` para mantener versiones históricas y trazabilidad temporal.

## PI 3: Relaciones

### Manejo de relaciones entre modelos

Como parte del trabajo también se contempló la gestión de relaciones entre modelos en DBT. 

Dado que DBT no aplica integridad referencial directamente en la base de datos, la estrategia a seguir  hubiera incluido los siguientes puntos clave para garantizar coherencia entre hechos y dimensiones:

### Relaciones a gestionar

- Relación entre `hechos_ventas.usuarioid` y `dim_usuario.usuarioid`
- Relación entre `hechos_ventas.productoid` y `dim_producto.productoid`
- Relación entre `dim_producto.categoriaid` y `dim_categoria.categoriaid`
- Relación entre `hechos_ventas.fecha` y `dim_fecha_orden.fecha`
- Relación entre `hechos_ventas.metodopagoid` y `dim_metodopago.metodopagoid`
- Relación entre `hechos_ventas.estadopago` y `dim_estado_pago.estado`

### Validaciones a considerar con DBT

En un escenario ideal, se hubieran incorporado pruebas en DBT (`tests`) sobre los modelos transformados para validar relaciones:

```yaml
tests:
  - relationships:
      model: hechos_ventas
      column_name: usuarioid
      to: ref('dim_usuario')
      field: usuarioid
```

Este tipo de pruebas permite:

- Detectar claves huérfanas (por ejemplo, ventas con usuarios inexistentes)
- Garantizar consistencia entre dimensiones y hechos
- Mejorar la confiabilidad de los datos para dashboards o análisis posteriores

## PI 4: Insights

### Insights del negocio – Storytelling

Tras la carga, validación y exploración de los datos, se obtuvieron diversos **hallazgos clave** que permiten entender mejor el comportamiento de los usuarios, los productos más exitosos y el desempeño comercial general. Estos insights fueron obtenidos mediante consultas SQL y análisis con Python (SQLAlchemy ORM).

#### 1. ¿Qué compran los usuarios y cómo?

Los productos más vendidos pertenecen principalmente a las categorías **Electrónica** y **Moda**, revelando una alta demanda en tecnología y vestimenta. Se identificó un patrón de compra frecuente con preferencia por productos de precio medio y buena valoración.

Los métodos de pago más utilizados fueron **tarjeta de crédito** y **transferencia bancaria**, destacando la necesidad de mantener múltiples opciones activas para facilitar conversiones.

#### 2. ¿Cuándo compran más?

La mayoría de las compras se concentran los **días lunes y viernes**, con picos mensuales cerca del **inicio de cada mes**, lo cual puede estar relacionado con fechas de cobro. 

#### 3. ¿Qué productos no se venden?

Algunos productos presentan alto stock pero muy pocas ventas. Esto indica un exceso de inventario y una posible mala elección de surtido. Se identificaron productos con buenas calificaciones pero baja rotación, lo cual sugiere falta de visibilidad.

#### 4. ¿Cómo son nuestros usuarios?

Más del 30% de los usuarios registrados **nunca han realizado una compra**, revelando una oportunidad para estrategias de reactivación (emails, cupones). Por otro lado, un grupo pequeño de usuarios concentra una gran parte de las ventas, siendo **clientes fieles o frecuentes**.

#### 5. ¿Cuánto recaudamos?

Se calculó la **recaudación mensual** total y por método de pago, permitiendo evaluar el desempeño financiero. También se detectaron algunos pagos en estado **‘Procesando’ o ‘Fallido’**, lo que sugiere revisar las integraciones con los proveedores de pago.