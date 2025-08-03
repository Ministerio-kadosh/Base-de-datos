-- Script de Remodelación Limpia para Base de Datos en Supabase
-- Este script crea solamente las tablas con la nueva estructura

-- ===== CREAR NUEVAS TABLAS =====

-- 1. Crear tabla administradores
CREATE TABLE administradores (
    id_admin SERIAL PRIMARY KEY,
    nombre_admin VARCHAR(100) NOT NULL,
    rol_admin VARCHAR(50),
    codigo_acceso VARCHAR(255) NOT NULL, -- Ampliado para almacenar hash bcrypt
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Crear tabla entidades_apoyo
CREATE TABLE entidades_apoyo (
    id_entidad SERIAL PRIMARY KEY,
    nombre_entidad VARCHAR(255) NOT NULL,
    tipo_entidad VARCHAR(50),
    contacto VARCHAR(100),
    es_donante BOOLEAN DEFAULT false,
    es_proveedor BOOLEAN DEFAULT false,
    es_comercio BOOLEAN DEFAULT false
);

-- 3. Crear tabla productos
CREATE TABLE productos (
    id_producto SERIAL PRIMARY KEY,
    nombre_producto VARCHAR(100) NOT NULL,
    precio_referencia NUMERIC(10,2),
    id_entidad INTEGER REFERENCES entidades_apoyo(id_entidad)
);

-- 4. Crear tabla predicadores
CREATE TABLE predicadores (
    id_predicador SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Crear tabla jovenes
CREATE TABLE jovenes (
    id_joven SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Crear tabla reuniones
CREATE TABLE reuniones (
    id_reunion SERIAL PRIMARY KEY,
    director VARCHAR(255),
    lectura VARCHAR(100),
    cantos VARCHAR(255),
    ofrenda NUMERIC(10,2),
    predicador VARCHAR(100),
    fecha_reunion DATE NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Crear tabla asistencia
CREATE TABLE asistencia (
    id_asistencia SERIAL PRIMARY KEY,
    id_joven INTEGER REFERENCES jovenes(id_joven),
    nombre_joven VARCHAR(100),
    fecha_reunion DATE NOT NULL,
    asistio BOOLEAN DEFAULT false
);

-- 8. Crear tabla movimientos_financieros
CREATE TABLE movimientos_financieros (
    id_movimiento SERIAL PRIMARY KEY,
    tipo_movimiento VARCHAR(50) NOT NULL,
    concepto VARCHAR(255) NOT NULL,
    monto NUMERIC(10,2) NOT NULL,
    id_entidad INTEGER REFERENCES entidades_apoyo(id_entidad),
    id_producto INTEGER REFERENCES productos(id_producto),
    registrado_por VARCHAR(100),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 9. Crear tabla bandeja
CREATE TABLE bandeja (
    id_bandeja SERIAL PRIMARY KEY,
    objetivo VARCHAR(255) NOT NULL,
    descripcion TEXT
);

-- 10. Crear tabla calendario
CREATE TABLE calendario (
    id_evento SERIAL PRIMARY KEY,
    nombre_evento VARCHAR(255) NOT NULL,
    objetivo_evento VARCHAR(255),
    fecha_evento DATE NOT NULL,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 11. Crear tabla consultas
CREATE TABLE consultas (
    id_consulta SERIAL PRIMARY KEY,
    nombre_consulta VARCHAR(100) NOT NULL,
    sql_consulta TEXT NOT NULL,
    parametros JSONB,
    descripcion TEXT,
    id_admin_creador INTEGER REFERENCES administradores(id_admin),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 12. Crear tabla informes
CREATE TABLE informes (
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

-- 13. Crear tabla historial_cambios
CREATE TABLE historial_cambios (
    id_cambio SERIAL PRIMARY KEY,
    tabla_afectada VARCHAR(50) NOT NULL,
    id_registro INTEGER NOT NULL,
    tipo_cambio VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    usuario_responsable VARCHAR(100),
    fecha_cambio TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Creación de tablas completada exitosamente';
    RAISE NOTICE 'Todas las tablas han sido creadas con la nueva estructura';
END $$;