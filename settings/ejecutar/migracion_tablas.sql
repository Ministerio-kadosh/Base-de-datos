-- Script de Migración para Remodelación de Base de Datos
-- Basado en la estructura definida en Remodelacion.md

-- ===== MIGRACIÓN DE TABLAS =====

-- 1. Renombrar tabla asistencias a asistencia
ALTER TABLE IF EXISTS asistencias RENAME TO asistencia;

-- 2. Renombrar tabla finanzas a movimientos_financieros
ALTER TABLE IF EXISTS finanzas RENAME TO movimientos_financieros;

-- ===== MIGRACIÓN DE CAMPOS =====

-- 3. Actualizar campos de tabla asistencia
ALTER TABLE asistencia RENAME COLUMN IF EXISTS "Id_asistencia" TO id_asistencia;
ALTER TABLE asistencia RENAME COLUMN IF EXISTS "Id_Jovenes" TO id_joven;
ALTER TABLE asistencia RENAME COLUMN IF EXISTS "Fecha_viernes" TO fecha_reunion;

-- 4. Actualizar campos de tabla reuniones
ALTER TABLE reuniones RENAME COLUMN IF EXISTS "Id_Reuniones" TO id_reunion;
ALTER TABLE reuniones RENAME COLUMN IF EXISTS "Dirección" TO director;
ALTER TABLE reuniones RENAME COLUMN IF EXISTS "Oferida" TO ofrenda;

-- 5. Actualizar campos de tabla predicadores
ALTER TABLE predicadores RENAME COLUMN IF EXISTS "Id" TO id_predicador;
ALTER TABLE predicadores RENAME COLUMN IF EXISTS "Nombre" TO nombre;
ALTER TABLE predicadores RENAME COLUMN IF EXISTS "Apellido" TO apellido;
ALTER TABLE predicadores RENAME COLUMN IF EXISTS "Numero" TO telefono;

-- 6. Actualizar campos de tabla jovenes
ALTER TABLE jovenes RENAME COLUMN IF EXISTS "Id" TO id_joven;
ALTER TABLE jovenes RENAME COLUMN IF EXISTS "Nombre" TO nombre;
ALTER TABLE jovenes RENAME COLUMN IF EXISTS "Apellido" TO apellido;
ALTER TABLE jovenes RENAME COLUMN IF EXISTS "Numero" TO telefono;

-- 7. Actualizar campos de tabla calendario
ALTER TABLE calendario RENAME COLUMN IF EXISTS "Id" TO id_evento;
ALTER TABLE calendario RENAME COLUMN IF EXISTS "Nombre" TO nombre_evento;
ALTER TABLE calendario RENAME COLUMN IF EXISTS "Objetivo" TO objetivo_evento;
ALTER TABLE calendario RENAME COLUMN IF EXISTS "Fecha" TO fecha_evento;

-- 8. Actualizar campos de tabla bandeja
ALTER TABLE bandeja RENAME COLUMN IF EXISTS "Id" TO id_bandeja;
ALTER TABLE bandeja RENAME COLUMN IF EXISTS "Objetivo" TO objetivo;
ALTER TABLE bandeja RENAME COLUMN IF EXISTS "Descripcion" TO descripcion;

-- 9. Actualizar campos de tabla movimientos_financieros (anterior finanzas)
ALTER TABLE movimientos_financieros RENAME COLUMN IF EXISTS "Id" TO id_movimiento;
ALTER TABLE movimientos_financieros RENAME COLUMN IF EXISTS "Tipo" TO tipo_movimiento;
ALTER TABLE movimientos_financieros RENAME COLUMN IF EXISTS "Concepto" TO concepto;
ALTER TABLE movimientos_financieros RENAME COLUMN IF EXISTS "Monto" TO monto;
ALTER TABLE movimientos_financieros RENAME COLUMN IF EXISTS "Entidad" TO id_entidad;
ALTER TABLE movimientos_financieros RENAME COLUMN IF EXISTS "Producto" TO id_producto;
ALTER TABLE movimientos_financieros RENAME COLUMN IF EXISTS "Registrado_por" TO registrado_por;

-- ===== CREAR NUEVAS TABLAS =====

-- 10. Crear tabla entidades_apoyo si no existe
CREATE TABLE IF NOT EXISTS entidades_apoyo (
    id_entidad SERIAL PRIMARY KEY,
    nombre_entidad VARCHAR(255) NOT NULL,
    tipo_entidad VARCHAR(50),
    contacto VARCHAR(100),
    es_donante BOOLEAN DEFAULT false,
    es_proveedor BOOLEAN DEFAULT false,
    es_comercio BOOLEAN DEFAULT false
);

-- 11. Crear tabla administradores si no existe
CREATE TABLE IF NOT EXISTS administradores (
    id_admin SERIAL PRIMARY KEY,
    nombre_admin VARCHAR(100) NOT NULL,
    rol_admin VARCHAR(50),
    codigo_acceso VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Crear tabla productos si no existe
CREATE TABLE IF NOT EXISTS productos (
    id_producto SERIAL PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    precio_referencia NUMERIC(10,2),
    id_entidad INTEGER REFERENCES entidades_apoyo(id_entidad)
);

-- 13. Crear tabla consultas si no existe
CREATE TABLE IF NOT EXISTS consultas (
    id_consulta SERIAL PRIMARY KEY,
    nombre_consulta VARCHAR(100) NOT NULL,
    sql_consulta TEXT NOT NULL,
    parametros JSONB,
    descripcion TEXT,
    id_admin_creador INTEGER REFERENCES administradores(id_admin),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 14. Crear tabla informes si no existe
CREATE TABLE IF NOT EXISTS informes (
    id_informe SERIAL PRIMARY KEY,
    titulo_informe VARCHAR(100) NOT NULL,
    id_consulta INTEGER REFERENCES consultas(id_consulta),
    parametros_usados JSONB,
    formato_salida VARCHAR(10),
    estado VARCHAR(20) DEFAULT 'pendiente',
    resultados JSONB,
    id_usuario INTEGER,
    fecha_generacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===== AGREGAR CAMPOS FALTANTES =====

-- 15. Agregar campos faltantes a tabla predicadores
ALTER TABLE predicadores ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- 16. Agregar campos faltantes a tabla jovenes
ALTER TABLE jovenes ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- 17. Agregar campos faltantes a tabla reuniones
ALTER TABLE reuniones ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- 18. Agregar campos faltantes a tabla calendario
ALTER TABLE calendario ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- 19. Agregar campos faltantes a tabla movimientos_financieros
ALTER TABLE movimientos_financieros ADD COLUMN IF NOT EXISTS fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- ===== AGREGAR CAMPOS A TABLA ASISTENCIA =====

-- 20. Agregar campos faltantes a tabla asistencia
ALTER TABLE asistencia ADD COLUMN IF NOT EXISTS nombre_joven VARCHAR(100);
ALTER TABLE asistencia ADD COLUMN IF NOT EXISTS asistio BOOLEAN DEFAULT false;

-- ===== AGREGAR CAMPOS A TABLA REUNIONES =====

-- 21. Agregar campos faltantes a tabla reuniones
ALTER TABLE reuniones ADD COLUMN IF NOT EXISTS lectura VARCHAR(100);
ALTER TABLE reuniones ADD COLUMN IF NOT EXISTS cantos VARCHAR(255);
ALTER TABLE reuniones ADD COLUMN IF NOT EXISTS predicador VARCHAR(100);

-- ===== AGREGAR CAMPOS A TABLA CALENDARIO =====

-- 22. Agregar campos faltantes a tabla calendario
ALTER TABLE calendario ADD COLUMN IF NOT EXISTS observaciones TEXT;

-- ===== CREAR ÍNDICES PARA OPTIMIZACIÓN =====

-- 23. Crear índices para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_predicadores_nombre ON predicadores(nombre);
CREATE INDEX IF NOT EXISTS idx_jovenes_nombre ON jovenes(nombre);
CREATE INDEX IF NOT EXISTS idx_reuniones_fecha ON reuniones(fecha_reunion);
CREATE INDEX IF NOT EXISTS idx_asistencia_fecha ON asistencia(fecha_reunion);
CREATE INDEX IF NOT EXISTS idx_movimientos_fecha ON movimientos_financieros(fecha_registro);

-- ===== VERIFICAR MIGRACIÓN =====

-- 24. Verificar que todas las tablas existen
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'predicadores', 'reuniones', 'calendario', 'bandeja', 
    'asistencia', 'jovenes', 'movimientos_financieros',
    'entidades_apoyo', 'administradores', 'productos',
    'consultas', 'informes'
);

-- 25. Verificar estructura de tabla predicadores
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'predicadores' 
ORDER BY ordinal_position;

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Migración completada exitosamente';
    RAISE NOTICE 'Todas las tablas han sido actualizadas según la nueva estructura';
END $$; 