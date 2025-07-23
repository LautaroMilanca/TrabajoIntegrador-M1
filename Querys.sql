--Emails duplicados
SELECT email, COUNT(*)
FROM usuarios
GROUP BY
    email
HAVING
    COUNT(*) > 1;

--Productos con stock negativo
SELECT * FROM productos WHERE stock < 0;

--Productos con precio igual o menor a 0
SELECT * FROM productos WHERE precio <= 0;

--Productos sin categoría asignada
SELECT * FROM productos WHERE categoriaid IS NULL;

--Órdenes con total igual a 0
SELECT * FROM ordenes WHERE total = 0;

--Órdenes con fecha futura
SELECT * FROM ordenes WHERE fechaorden > NOW();

--Órdenes sin detalles
SELECT o.ordenid
FROM ordenes o
    LEFT JOIN detalleordenes d ON o.ordenid = d.ordenid
WHERE
    d.detalleid IS NULL;

--Detalles con cantidad negativa o cero
SELECT * FROM detalleordenes WHERE cantidad <= 0;

--Detalles con precio unitario 0
SELECT * FROM detalleordenes WHERE preciounitario = 0;

--Pagos con estado inválido
SELECT *
FROM historialpagos
WHERE
    estadopago NOT IN(
        'Procesando',
        'Fallido',
        'Completado'
    );

--Pagos con fecha futura
SELECT * FROM historialpagos WHERE fechapago > NOW();

--Métodos de pago sin descripción
SELECT *
FROM metodospago
WHERE
    descripcion IS NULL
    OR descripcion = '';