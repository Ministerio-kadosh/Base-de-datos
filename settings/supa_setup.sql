-- =====================================================
-- SCRIPT DE CONFIGURACIÓN COMPLETA PARA SUPABASE
-- Sistema de Gestión - Base de Datos
-- =====================================================

-- =====================================================
-- LIMPIEZA AUTOMÁTICA DE TABLAS EXISTENTES
-- =====================================================

-- Ejecutar en orden (por las relaciones)
DROP TABLE IF EXISTS historial_cambios CASCADE;
DROP TABLE IF EXISTS informes CASCADE;
DROP TABLE IF EXISTS finanzas CASCADE;
DROP TABLE IF EXISTS asistencias CASCADE;
DROP TABLE IF EXISTS jovenes CASCADE;
DROP TABLE IF EXISTS calendario CASCADE;
DROP TABLE IF EXISTS reuniones CASCADE;
DROP TABLE IF EXISTS bandeja CASCADE;
DROP TABLE IF EXISTS predicadores CASCADE;
DROP TABLE IF EXISTS administradores CASCADE;

-- =====================================================
-- HABILITAR EXTENSIONES NECESARIAS
-- =====================================================

-- Habilitar extensiones necesarias
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- TABLA: ADMINISTRADORES
-- =====================================================
CREATE TABLE IF NOT EXISTS administradores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL DEFAULT 'Admin',
    codigo VARCHAR(255) NOT NULL,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    estado VARCHAR(20) DEFAULT 'Activo'
);

-- =====================================================
-- TABLA: PREDICADORES
-- =====================================================
CREATE TABLE IF NOT EXISTS predicadores (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Apellido VARCHAR(100) NOT NULL,
    Numero VARCHAR(20) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- TABLA: REUNIONES
-- =====================================================
CREATE TABLE IF NOT EXISTS reuniones (
    id SERIAL PRIMARY KEY,
    Dirige VARCHAR(100) NOT NULL,
    Lectura TEXT NOT NULL,
    Cantos_alegre VARCHAR(100) NOT NULL,
    Ofrenda VARCHAR(100) NOT NULL,
    Predica VARCHAR(100) NOT NULL,
    fecha_reunion DATE NOT NULL,
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- TABLA: CALENDARIO
-- =====================================================
CREATE TABLE IF NOT EXISTS calendario (
    id SERIAL PRIMARY KEY,
    Evento VARCHAR(200) NOT NULL,
    Fecha DATE NOT NULL,
    Observaciones TEXT,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- TABLA: BANDEJA
-- =====================================================
CREATE TABLE IF NOT EXISTS bandeja (
    id SERIAL PRIMARY KEY,
    Objetivo VARCHAR(200) NOT NULL,
    Descripcion TEXT NOT NULL,
    estado VARCHAR(20) DEFAULT 'Pendiente',
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- TABLA: ASISTENCIAS
-- =====================================================
CREATE TABLE IF NOT EXISTS asistencias (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Numero VARCHAR(20) NOT NULL,
    unoviernes VARCHAR(20) DEFAULT 'Ausente',
    dosviernes VARCHAR(20) DEFAULT 'Ausente',
    tresViernes VARCHAR(20) DEFAULT 'Ausente',
    cuatroviernes VARCHAR(20) DEFAULT 'Ausente',
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- TABLA: JOVENES
-- =====================================================
CREATE TABLE IF NOT EXISTS jovenes (
    id SERIAL PRIMARY KEY,
    Nombre VARCHAR(100) NOT NULL,
    Edad INTEGER NOT NULL,
    Telefono VARCHAR(20) NOT NULL,
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- TABLA: FINANZAS
-- =====================================================
CREATE TABLE IF NOT EXISTS finanzas (
    id SERIAL PRIMARY KEY,
    Concepto VARCHAR(200) NOT NULL,
    Monto DECIMAL(10,2) NOT NULL,
    Fecha DATE NOT NULL,
    Observaciones TEXT,
    tipo VARCHAR(20) DEFAULT 'Ingreso',
    estado VARCHAR(20) DEFAULT 'Activo',
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- TABLA: HISTORIAL_CAMBIOS
-- =====================================================
CREATE TABLE IF NOT EXISTS historial_cambios (
    id SERIAL PRIMARY KEY,
    tabla VARCHAR(50) NOT NULL,
    id_registro INTEGER NOT NULL,
    accion VARCHAR(20) NOT NULL, -- INSERT, UPDATE, DELETE
    datos_anteriores JSONB,
    datos_nuevos JSONB,
    usuario VARCHAR(100) NOT NULL,
    fecha_cambio TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- TABLA: INFORMES
-- =====================================================
CREATE TABLE IF NOT EXISTS informes (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    consultas JSONB,
    formato VARCHAR(20) DEFAULT 'json',
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    estado VARCHAR(20) DEFAULT 'activo',
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- RELACIONES ENTRE TABLAS
-- =====================================================

-- Relación: Asistencias -> Jóvenes (por nombre)
-- Agregar campo para relacionar asistencias con jóvenes
ALTER TABLE asistencias ADD COLUMN IF NOT EXISTS joven_id INTEGER REFERENCES jovenes(id) ON DELETE SET NULL;

-- Relación: Reuniones -> Predicadores (por quien dirige)
-- Agregar campo para relacionar reuniones con predicadores
ALTER TABLE reuniones ADD COLUMN IF NOT EXISTS predicador_id INTEGER REFERENCES predicadores(id) ON DELETE SET NULL;

-- Relación: Finanzas -> Reuniones (para ofrendas específicas)
-- Agregar campo para relacionar finanzas con reuniones
ALTER TABLE finanzas ADD COLUMN IF NOT EXISTS reunion_id INTEGER REFERENCES reuniones(id) ON DELETE SET NULL;

-- Relación: Calendario -> Reuniones (para eventos relacionados)
-- Agregar campo para relacionar calendario con reuniones
ALTER TABLE calendario ADD COLUMN IF NOT EXISTS reunion_id INTEGER REFERENCES reuniones(id) ON DELETE SET NULL;

-- Relación: Asistencias -> Reuniones (para asistencias específicas)
-- Agregar campo para relacionar asistencias con reuniones
ALTER TABLE asistencias ADD COLUMN IF NOT EXISTS reunion_id INTEGER REFERENCES reuniones(id) ON DELETE SET NULL;

-- =====================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_predicadores_nombre ON predicadores(Nombre, Apellido);
CREATE INDEX IF NOT EXISTS idx_reuniones_fecha ON reuniones(fecha);
CREATE INDEX IF NOT EXISTS idx_calendario_fecha ON calendario(Fecha);
CREATE INDEX IF NOT EXISTS idx_asistencias_nombre ON asistencias(Nombre);
CREATE INDEX IF NOT EXISTS idx_finanzas_fecha ON finanzas(Fecha);
CREATE INDEX IF NOT EXISTS idx_finanzas_concepto ON finanzas(Concepto);
CREATE INDEX IF NOT EXISTS idx_historial_tabla_fecha ON historial_cambios(tabla, fecha_cambio);
CREATE INDEX IF NOT EXISTS idx_informes_estado ON informes(estado);

-- Índices para relaciones
CREATE INDEX IF NOT EXISTS idx_asistencias_joven_id ON asistencias(joven_id);
CREATE INDEX IF NOT EXISTS idx_reuniones_predicador_id ON reuniones(predicador_id);
CREATE INDEX IF NOT EXISTS idx_finanzas_reunion_id ON finanzas(reunion_id);
CREATE INDEX IF NOT EXISTS idx_calendario_reunion_id ON calendario(reunion_id);
CREATE INDEX IF NOT EXISTS idx_asistencias_reunion_id ON asistencias(reunion_id);
CREATE INDEX IF NOT EXISTS idx_reuniones_fecha_reunion ON reuniones(fecha_reunion);

-- =====================================================
-- POLÍTICAS RLS (ROW LEVEL SECURITY)
-- =====================================================

-- Habilitar RLS en todas las tablas
ALTER TABLE administradores ENABLE ROW LEVEL SECURITY;
ALTER TABLE predicadores ENABLE ROW LEVEL SECURITY;
ALTER TABLE reuniones ENABLE ROW LEVEL SECURITY;
ALTER TABLE calendario ENABLE ROW LEVEL SECURITY;
ALTER TABLE bandeja ENABLE ROW LEVEL SECURITY;
ALTER TABLE asistencias ENABLE ROW LEVEL SECURITY;
ALTER TABLE jovenes ENABLE ROW LEVEL SECURITY;
ALTER TABLE finanzas ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_cambios ENABLE ROW LEVEL SECURITY;
ALTER TABLE informes ENABLE ROW LEVEL SECURITY;

-- Políticas para permitir acceso completo (ajustar según necesidades)
CREATE POLICY "Permitir acceso completo a administradores" ON administradores FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a predicadores" ON predicadores FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a reuniones" ON reuniones FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a calendario" ON calendario FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a bandeja" ON bandeja FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a asistencias" ON asistencias FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a jovenes" ON jovenes FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a finanzas" ON finanzas FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a historial_cambios" ON historial_cambios FOR ALL USING (true);
CREATE POLICY "Permitir acceso completo a informes" ON informes FOR ALL USING (true);

-- =====================================================
-- DATOS INICIALES
-- =====================================================

-- Insertar administrador por defecto
INSERT INTO administradores (nombre, rol, codigo) VALUES 
('Administrador Principal', 'Super Admin', '123456')
ON CONFLICT DO NOTHING;

-- Insertar algunos predicadores de ejemplo
INSERT INTO predicadores (Nombre, Apellido, Numero) VALUES 
('Juan', 'Pérez', '123456789'),
('María', 'García', '987654321'),
('Carlos', 'López', '555123456')
ON CONFLICT DO NOTHING;

-- Insertar reunión de ejemplo
INSERT INTO reuniones (Dirige, Lectura, Cantos_alegre, Ofrenda, Predica, fecha_reunion) VALUES 
('Pastor Principal', 'Juan 3:16', 'Alabanzas', 'Diezmo', 'El amor de Dios', CURRENT_DATE)
ON CONFLICT DO NOTHING;

-- Insertar evento de calendario
INSERT INTO calendario (Evento, Fecha, Observaciones) VALUES 
('Reunión de Jóvenes', CURRENT_DATE + INTERVAL '7 days', 'Evento semanal')
ON CONFLICT DO NOTHING;

-- Insertar tarea en bandeja
INSERT INTO bandeja (Objetivo, Descripcion) VALUES 
('Organizar evento', 'Preparar reunión mensual')
ON CONFLICT DO NOTHING;

-- Insertar asistencia de ejemplo
INSERT INTO asistencias (Nombre, Numero, unoviernes, dosviernes, tresViernes, cuatroviernes) VALUES 
('Ana Martínez', '111222333', 'Presente', 'Presente', 'Ausente', 'Presente')
ON CONFLICT DO NOTHING;

-- Insertar joven de ejemplo
INSERT INTO jovenes (Nombre, Edad, Telefono) VALUES 
('Luis Rodríguez', 20, '444555666')
ON CONFLICT DO NOTHING;

-- Insertar finanza de ejemplo
INSERT INTO finanzas (Concepto, Monto, Fecha, Observaciones) VALUES 
('Diezmo', 100.00, CURRENT_DATE, 'Entrada semanal')
ON CONFLICT DO NOTHING;

-- Insertar informe de ejemplo
INSERT INTO informes (titulo, descripcion, consultas) VALUES 
('Informe General', 'Informe de prueba del sistema', '[]')
ON CONFLICT DO NOTHING;

-- =====================================================
-- FUNCIONES DE TRIGGER PARA HISTORIAL
-- =====================================================

-- Función para registrar cambios en historial
CREATE OR REPLACE FUNCTION registrar_cambio()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO historial_cambios (tabla, id_registro, accion, datos_nuevos, usuario)
        VALUES (TG_TABLE_NAME, NEW.id, 'INSERT', to_jsonb(NEW), COALESCE(NEW.usuario, 'sistema'));
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO historial_cambios (tabla, id_registro, accion, datos_anteriores, datos_nuevos, usuario)
        VALUES (TG_TABLE_NAME, NEW.id, 'UPDATE', to_jsonb(OLD), to_jsonb(NEW), COALESCE(NEW.usuario, 'sistema'));
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO historial_cambios (tabla, id_registro, accion, datos_anteriores, usuario)
        VALUES (TG_TABLE_NAME, OLD.id, 'DELETE', to_jsonb(OLD), COALESCE(OLD.usuario, 'sistema'));
        RETURN OLD;
    END IF;
    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

-- Triggers para registrar cambios automáticamente
CREATE TRIGGER trigger_predicadores_historial
    AFTER INSERT OR UPDATE OR DELETE ON predicadores
    FOR EACH ROW EXECUTE FUNCTION registrar_cambio();

CREATE TRIGGER trigger_reuniones_historial
    AFTER INSERT OR UPDATE OR DELETE ON reuniones
    FOR EACH ROW EXECUTE FUNCTION registrar_cambio();

CREATE TRIGGER trigger_calendario_historial
    AFTER INSERT OR UPDATE OR DELETE ON calendario
    FOR EACH ROW EXECUTE FUNCTION registrar_cambio();

CREATE TRIGGER trigger_bandeja_historial
    AFTER INSERT OR UPDATE OR DELETE ON bandeja
    FOR EACH ROW EXECUTE FUNCTION registrar_cambio();

CREATE TRIGGER trigger_asistencias_historial
    AFTER INSERT OR UPDATE OR DELETE ON asistencias
    FOR EACH ROW EXECUTE FUNCTION registrar_cambio();

CREATE TRIGGER trigger_jovenes_historial
    AFTER INSERT OR UPDATE OR DELETE ON jovenes
    FOR EACH ROW EXECUTE FUNCTION registrar_cambio();

CREATE TRIGGER trigger_finanzas_historial
    AFTER INSERT OR UPDATE OR DELETE ON finanzas
    FOR EACH ROW EXECUTE FUNCTION registrar_cambio();

-- =====================================================
-- MENSAJE DE CONFIRMACIÓN
-- =====================================================

DO $$
BEGIN
    RAISE NOTICE '✅ Base de datos configurada exitosamente!';
    RAISE NOTICE '📊 Tablas creadas: administradores, predicadores, reuniones, calendario, bandeja, asistencias, jovenes, finanzas, historial_cambios, informes';
    RAISE NOTICE '🔒 RLS habilitado en todas las tablas';
    RAISE NOTICE '📈 Índices creados para optimización';
    RAISE NOTICE '🔄 Triggers configurados para historial automático';
    RAISE NOTICE '👤 Administrador por defecto: nombre="Administrador Principal", código="123456"';
END $$; 