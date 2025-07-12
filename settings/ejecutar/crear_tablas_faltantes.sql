-- Script para crear las tablas faltantes en Supabase
-- Ejecutar este script en el SQL Editor de Supabase

-- Tabla asistencias
CREATE TABLE IF NOT EXISTS asistencias (
    id SERIAL PRIMARY KEY,
    reunion_id INTEGER REFERENCES reuniones(id) ON DELETE CASCADE,
    joven_id INTEGER REFERENCES jovenes(id) ON DELETE CASCADE,
    asistio BOOLEAN DEFAULT false,
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema',
    fecha_actualizacion TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Tabla informes_generados
CREATE TABLE IF NOT EXISTS informes_generados (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    tipo_informe VARCHAR(50) NOT NULL,
    datos_informe JSONB,
    fecha_generacion TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema',
    estado VARCHAR(20) DEFAULT 'activo'
);

-- Crear índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_asistencias_reunion_id ON asistencias(reunion_id);
CREATE INDEX IF NOT EXISTS idx_asistencias_joven_id ON asistencias(joven_id);
CREATE INDEX IF NOT EXISTS idx_informes_generados_tipo ON informes_generados(tipo_informe);
CREATE INDEX IF NOT EXISTS idx_informes_generados_fecha ON informes_generados(fecha_generacion);

-- Habilitar RLS (Row Level Security)
ALTER TABLE asistencias ENABLE ROW LEVEL SECURITY;
ALTER TABLE informes_generados ENABLE ROW LEVEL SECURITY;

-- Políticas RLS para asistencias
CREATE POLICY "Permitir lectura de asistencias" ON asistencias
    FOR SELECT USING (true);

CREATE POLICY "Permitir inserción de asistencias" ON asistencias
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Permitir actualización de asistencias" ON asistencias
    FOR UPDATE USING (true);

CREATE POLICY "Permitir eliminación de asistencias" ON asistencias
    FOR DELETE USING (true);

-- Políticas RLS para informes_generados
CREATE POLICY "Permitir lectura de informes_generados" ON informes_generados
    FOR SELECT USING (true);

CREATE POLICY "Permitir inserción de informes_generados" ON informes_generados
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Permitir actualización de informes_generados" ON informes_generados
    FOR UPDATE USING (true);

CREATE POLICY "Permitir eliminación de informes_generados" ON informes_generados
    FOR DELETE USING (true);

-- Insertar datos de prueba para asistencias
INSERT INTO asistencias (reunion_id, joven_id, asistio, usuario) VALUES
(1, 1, true, 'sistema'),
(1, 2, false, 'sistema'),
(2, 1, true, 'sistema');

-- Insertar datos de prueba para informes_generados
INSERT INTO informes_generados (titulo, tipo_informe, datos_informe, usuario) VALUES
('Informe General Mensual', 'general', '{"total_reuniones": 5, "total_asistencias": 15}', 'sistema'),
('Informe de Predicadores', 'predicadores', '{"total_predicadores": 3, "reuniones_por_predicador": {"1": 2, "2": 2, "3": 1}}', 'sistema');

-- Verificar que las tablas se crearon correctamente
SELECT 'asistencias' as tabla, COUNT(*) as registros FROM asistencias
UNION ALL
SELECT 'informes_generados' as tabla, COUNT(*) as registros FROM informes_generados; 