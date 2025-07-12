-- =====================================================
-- CONFIGURACIÓN DE BASE DE DATOS SUPABASE
-- Sistema de Gestión Flask - Configuración Completa
-- =====================================================

-- 1. HABILITAR EXTENSIONES NECESARIAS
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- =====================================================
-- 2. CREAR TABLAS DEL SISTEMA
-- =====================================================

-- Tabla de Administradores (Usuarios del sistema)
CREATE TABLE IF NOT EXISTS "Administradores" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(100) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL DEFAULT 'Admin',
    codigo VARCHAR(50) NOT NULL,
    activo BOOLEAN DEFAULT true,
    fecha_agregado TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW()
);

-- Tabla de Predicadores
CREATE TABLE IF NOT EXISTS "Predicadores" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Nombre VARCHAR(50) NOT NULL,
    Apellido VARCHAR(50) NOT NULL,
    Numero VARCHAR(20) NOT NULL,
    estado VARCHAR(20) DEFAULT 'activo',
    fecha TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- Tabla de Reuniones
CREATE TABLE IF NOT EXISTS "Reuniones" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_reunion TIMESTAMP,
    lugar VARCHAR(200),
    tipo VARCHAR(50),
    estado VARCHAR(20) DEFAULT 'activo',
    fecha TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- Tabla de Calendario (Eventos)
CREATE TABLE IF NOT EXISTS "Calendario" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    fecha_inicio TIMESTAMP NOT NULL,
    fecha_fin TIMESTAMP,
    tipo_evento VARCHAR(50),
    lugar VARCHAR(200),
    estado VARCHAR(20) DEFAULT 'activo',
    fecha TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- Tabla de Bandeja (Tareas y Objetivos)
CREATE TABLE IF NOT EXISTS "Bandeja" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    Objetivo VARCHAR(100) NOT NULL,
    Descripcion VARCHAR(500) NOT NULL,
    prioridad VARCHAR(20) DEFAULT 'media',
    estado VARCHAR(20) DEFAULT 'creado',
    fecha_limite TIMESTAMP,
    fecha TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- Tabla de Asistencias
CREATE TABLE IF NOT EXISTS "Asistencias" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre_persona VARCHAR(100) NOT NULL,
    fecha_asistencia DATE NOT NULL,
    tipo_reunion VARCHAR(50),
    presente BOOLEAN DEFAULT true,
    observaciones TEXT,
    fecha TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- Tabla de Jóvenes
CREATE TABLE IF NOT EXISTS "Jovenes" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    edad INTEGER,
    telefono VARCHAR(20),
    email VARCHAR(100),
    direccion TEXT,
    fecha_registro DATE DEFAULT CURRENT_DATE,
    estado VARCHAR(20) DEFAULT 'activo',
    fecha TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- Tabla de Finanzas
CREATE TABLE IF NOT EXISTS "Finanzas" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    concepto VARCHAR(200) NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    tipo VARCHAR(20) NOT NULL, -- 'ingreso' o 'gasto'
    categoria VARCHAR(50),
    fecha_transaccion DATE NOT NULL,
    descripcion TEXT,
    estado VARCHAR(20) DEFAULT 'activo',
    fecha TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- Tabla de Historial de Cambios (Auditoría)
CREATE TABLE IF NOT EXISTS "Historial_Cambios" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    fecha TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) NOT NULL,
    estado VARCHAR(20) NOT NULL, -- 'Creado', 'Editado', 'Eliminado', 'Revertido', 'Restaurado'
    tabla VARCHAR(50) NOT NULL,
    id_registro UUID NOT NULL,
    datos_anteriores JSONB,
    datos_nuevos JSONB
);

-- Tabla de Informes
CREATE TABLE IF NOT EXISTS "Informes" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    titulo VARCHAR(200) NOT NULL,
    descripcion TEXT,
    consultas JSONB NOT NULL, -- Array de consultas a ejecutar
    formato VARCHAR(20) DEFAULT 'json', -- 'json', 'csv', 'pdf'
    estado VARCHAR(20) DEFAULT 'activo',
    fecha_creacion TIMESTAMP DEFAULT NOW(),
    fecha_actualizacion TIMESTAMP DEFAULT NOW(),
    usuario VARCHAR(100) DEFAULT 'sistema'
);

-- =====================================================
-- 3. CONFIGURAR ROW LEVEL SECURITY (RLS)
-- =====================================================

-- Habilitar RLS en todas las tablas
ALTER TABLE "Administradores" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Predicadores" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Reuniones" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Calendario" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Bandeja" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Asistencias" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Jovenes" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Finanzas" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Historial_Cambios" ENABLE ROW LEVEL SECURITY;
ALTER TABLE "Informes" ENABLE ROW LEVEL SECURITY;

-- Políticas para Administradores
CREATE POLICY "Administradores pueden ver todos los administradores" 
ON "Administradores" FOR SELECT 
USING (true);

CREATE POLICY "Solo Super Admins pueden insertar administradores" 
ON "Administradores" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Solo Super Admins pueden actualizar administradores" 
ON "Administradores" FOR UPDATE 
USING (true);

CREATE POLICY "Solo Super Admins pueden eliminar administradores" 
ON "Administradores" FOR DELETE 
USING (true);

-- Políticas para Predicadores
CREATE POLICY "Usuarios pueden ver predicadores activos" 
ON "Predicadores" FOR SELECT 
USING (estado != 'eliminado');

CREATE POLICY "Usuarios autenticados pueden insertar predicadores" 
ON "Predicadores" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar predicadores" 
ON "Predicadores" FOR UPDATE 
USING (true);

CREATE POLICY "Usuarios autenticados pueden eliminar predicadores" 
ON "Predicadores" FOR DELETE 
USING (true);

-- Políticas para Reuniones
CREATE POLICY "Usuarios pueden ver reuniones" 
ON "Reuniones" FOR SELECT 
USING (true);

CREATE POLICY "Usuarios autenticados pueden insertar reuniones" 
ON "Reuniones" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar reuniones" 
ON "Reuniones" FOR UPDATE 
USING (true);

CREATE POLICY "Usuarios autenticados pueden eliminar reuniones" 
ON "Reuniones" FOR DELETE 
USING (true);

-- Políticas para Calendario
CREATE POLICY "Usuarios pueden ver eventos del calendario" 
ON "Calendario" FOR SELECT 
USING (true);

CREATE POLICY "Usuarios autenticados pueden insertar eventos" 
ON "Calendario" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar eventos" 
ON "Calendario" FOR UPDATE 
USING (true);

CREATE POLICY "Usuarios autenticados pueden eliminar eventos" 
ON "Calendario" FOR DELETE 
USING (true);

-- Políticas para Bandeja
CREATE POLICY "Usuarios pueden ver tareas de bandeja" 
ON "Bandeja" FOR SELECT 
USING (true);

CREATE POLICY "Usuarios autenticados pueden insertar tareas" 
ON "Bandeja" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar tareas" 
ON "Bandeja" FOR UPDATE 
USING (true);

CREATE POLICY "Usuarios autenticados pueden eliminar tareas" 
ON "Bandeja" FOR DELETE 
USING (true);

-- Políticas para Asistencias
CREATE POLICY "Usuarios pueden ver asistencias" 
ON "Asistencias" FOR SELECT 
USING (true);

CREATE POLICY "Usuarios autenticados pueden insertar asistencias" 
ON "Asistencias" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar asistencias" 
ON "Asistencias" FOR UPDATE 
USING (true);

CREATE POLICY "Usuarios autenticados pueden eliminar asistencias" 
ON "Asistencias" FOR DELETE 
USING (true);

-- Políticas para Jóvenes
CREATE POLICY "Usuarios pueden ver jóvenes" 
ON "Jovenes" FOR SELECT 
USING (true);

CREATE POLICY "Usuarios autenticados pueden insertar jóvenes" 
ON "Jovenes" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar jóvenes" 
ON "Jovenes" FOR UPDATE 
USING (true);

CREATE POLICY "Usuarios autenticados pueden eliminar jóvenes" 
ON "Jovenes" FOR DELETE 
USING (true);

-- Políticas para Finanzas
CREATE POLICY "Usuarios pueden ver finanzas" 
ON "Finanzas" FOR SELECT 
USING (true);

CREATE POLICY "Usuarios autenticados pueden insertar finanzas" 
ON "Finanzas" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar finanzas" 
ON "Finanzas" FOR UPDATE 
USING (true);

CREATE POLICY "Usuarios autenticados pueden eliminar finanzas" 
ON "Finanzas" FOR DELETE 
USING (true);

-- Políticas para Historial de Cambios
CREATE POLICY "Usuarios pueden ver historial de cambios" 
ON "Historial_Cambios" FOR SELECT 
USING (true);

CREATE POLICY "Sistema puede insertar en historial" 
ON "Historial_Cambios" FOR INSERT 
WITH CHECK (true);

-- Políticas para Informes
CREATE POLICY "Usuarios pueden ver informes" 
ON "Informes" FOR SELECT 
USING (estado = 'activo');

CREATE POLICY "Usuarios autenticados pueden insertar informes" 
ON "Informes" FOR INSERT 
WITH CHECK (true);

CREATE POLICY "Usuarios autenticados pueden actualizar informes" 
ON "Informes" FOR UPDATE 
USING (true);

CREATE POLICY "Usuarios autenticados pueden eliminar informes" 
ON "Informes" FOR DELETE 
USING (true);

-- =====================================================
-- 4. CREAR ÍNDICES PARA OPTIMIZACIÓN
-- =====================================================

-- Índices para Administradores
CREATE INDEX idx_administradores_email ON "Administradores"(email);
CREATE INDEX idx_administradores_rol ON "Administradores"(rol);
CREATE INDEX idx_administradores_activo ON "Administradores"(activo);

-- Índices para Predicadores
CREATE INDEX idx_predicadores_nombre ON "Predicadores"(Nombre);
CREATE INDEX idx_predicadores_apellido ON "Predicadores"(Apellido);
CREATE INDEX idx_predicadores_estado ON "Predicadores"(estado);
CREATE INDEX idx_predicadores_fecha ON "Predicadores"(fecha);

-- Índices para Reuniones
CREATE INDEX idx_reuniones_fecha ON "Reuniones"(fecha_reunion);
CREATE INDEX idx_reuniones_tipo ON "Reuniones"(tipo);
CREATE INDEX idx_reuniones_estado ON "Reuniones"(estado);

-- Índices para Calendario
CREATE INDEX idx_calendario_fecha_inicio ON "Calendario"(fecha_inicio);
CREATE INDEX idx_calendario_fecha_fin ON "Calendario"(fecha_fin);
CREATE INDEX idx_calendario_tipo_evento ON "Calendario"(tipo_evento);

-- Índices para Bandeja
CREATE INDEX idx_bandeja_estado ON "Bandeja"(estado);
CREATE INDEX idx_bandeja_prioridad ON "Bandeja"(prioridad);
CREATE INDEX idx_bandeja_fecha_limite ON "Bandeja"(fecha_limite);

-- Índices para Asistencias
CREATE INDEX idx_asistencias_fecha ON "Asistencias"(fecha_asistencia);
CREATE INDEX idx_asistencias_presente ON "Asistencias"(presente);
CREATE INDEX idx_asistencias_tipo_reunion ON "Asistencias"(tipo_reunion);

-- Índices para Jóvenes
CREATE INDEX idx_jovenes_nombre ON "Jovenes"(nombre);
CREATE INDEX idx_jovenes_apellido ON "Jovenes"(apellido);
CREATE INDEX idx_jovenes_estado ON "Jovenes"(estado);

-- Índices para Finanzas
CREATE INDEX idx_finanzas_fecha ON "Finanzas"(fecha_transaccion);
CREATE INDEX idx_finanzas_tipo ON "Finanzas"(tipo);
CREATE INDEX idx_finanzas_categoria ON "Finanzas"(categoria);

-- Índices para Historial de Cambios
CREATE INDEX idx_historial_fecha ON "Historial_Cambios"(fecha);
CREATE INDEX idx_historial_usuario ON "Historial_Cambios"(usuario);
CREATE INDEX idx_historial_tabla ON "Historial_Cambios"(tabla);
CREATE INDEX idx_historial_estado ON "Historial_Cambios"(estado);

-- Índices para Informes
CREATE INDEX idx_informes_titulo ON "Informes"(titulo);
CREATE INDEX idx_informes_estado ON "Informes"(estado);
CREATE INDEX idx_informes_fecha_creacion ON "Informes"(fecha_creacion);

-- =====================================================
-- 5. FUNCIONES Y TRIGGERS
-- =====================================================

-- Función para actualizar timestamp de actualización
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_actualizacion = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers para actualizar timestamp
CREATE TRIGGER update_administradores_updated_at 
    BEFORE UPDATE ON "Administradores" 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_informes_updated_at 
    BEFORE UPDATE ON "Informes" 
    FOR EACH ROW 
    EXECUTE FUNCTION update_updated_at_column();

-- Función para validar email único
CREATE OR REPLACE FUNCTION validate_unique_email()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM "Administradores" WHERE email = NEW.email AND id != NEW.id) THEN
        RAISE EXCEPTION 'El email ya está registrado';
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger para validar email único
CREATE TRIGGER validate_administradores_email 
    BEFORE INSERT OR UPDATE ON "Administradores" 
    FOR EACH ROW 
    EXECUTE FUNCTION validate_unique_email();

-- =====================================================
-- 6. DATOS INICIALES
-- =====================================================

-- Insertar administrador inicial (Super Admin)
INSERT INTO "Administradores" (email, nombre, rol, codigo) 
VALUES (
    'admin@sistema.com',
    'Administrador Sistema',
    'Super Admin',
    'admin123'
) ON CONFLICT (email) DO NOTHING;

-- Insertar algunos predicadores de ejemplo
INSERT INTO "Predicadores" (Nombre, Apellido, Numero) VALUES
('Juan', 'Pérez', '123456789'),
('María', 'González', '987654321'),
('Carlos', 'Rodríguez', '555666777')
ON CONFLICT DO NOTHING;

-- Insertar algunas reuniones de ejemplo
INSERT INTO "Reuniones" (titulo, descripcion, fecha_reunion, lugar, tipo) VALUES
('Reunión General', 'Reunión mensual de la congregación', '2024-01-15 19:00:00', 'Templo Principal', 'General'),
('Estudio Bíblico', 'Estudio semanal de la Biblia', '2024-01-20 20:00:00', 'Sala de Estudio', 'Estudio')
ON CONFLICT DO NOTHING;

-- Insertar algunos eventos de calendario
INSERT INTO "Calendario" (titulo, descripcion, fecha_inicio, fecha_fin, tipo_evento, lugar) VALUES
('Culto Dominical', 'Culto principal del domingo', '2024-01-21 10:00:00', '2024-01-21 12:00:00', 'Culto', 'Templo Principal'),
('Reunión de Jóvenes', 'Actividad especial para jóvenes', '2024-01-25 18:00:00', '2024-01-25 21:00:00', 'Juvenil', 'Sala de Jóvenes')
ON CONFLICT DO NOTHING;

-- Insertar algunas tareas de bandeja
INSERT INTO "Bandeja" (Objetivo, Descripcion, prioridad) VALUES
('Preparar sermón dominical', 'Investigar y preparar el mensaje para el próximo domingo', 'alta'),
('Organizar evento juvenil', 'Planificar actividades para el próximo evento de jóvenes', 'media')
ON CONFLICT DO NOTHING;

-- =====================================================
-- 7. VISTAS ÚTILES
-- =====================================================

-- Vista para estadísticas generales
CREATE OR REPLACE VIEW "Estadisticas_Generales" AS
SELECT 
    (SELECT COUNT(*) FROM "Predicadores" WHERE estado = 'activo') as total_predicadores,
    (SELECT COUNT(*) FROM "Reuniones" WHERE estado = 'activo') as total_reuniones,
    (SELECT COUNT(*) FROM "Jovenes" WHERE estado = 'activo') as total_jovenes,
    (SELECT COUNT(*) FROM "Bandeja" WHERE estado = 'creado') as tareas_pendientes,
    (SELECT COUNT(*) FROM "Asistencias" WHERE presente = true AND fecha_asistencia >= CURRENT_DATE - INTERVAL '30 days') as asistencias_ultimo_mes;

-- Vista para resumen de finanzas
CREATE OR REPLACE VIEW "Resumen_Finanzas" AS
SELECT 
    tipo,
    categoria,
    SUM(monto) as total,
    COUNT(*) as cantidad_transacciones,
    AVG(monto) as promedio
FROM "Finanzas" 
WHERE estado = 'activo'
GROUP BY tipo, categoria;

-- =====================================================
-- 8. COMENTARIOS Y DOCUMENTACIÓN
-- =====================================================

COMMENT ON TABLE "Administradores" IS 'Tabla de usuarios administradores del sistema';
COMMENT ON TABLE "Predicadores" IS 'Tabla de predicadores registrados';
COMMENT ON TABLE "Reuniones" IS 'Tabla de reuniones programadas';
COMMENT ON TABLE "Calendario" IS 'Tabla de eventos del calendario';
COMMENT ON TABLE "Bandeja" IS 'Tabla de tareas y objetivos';
COMMENT ON TABLE "Asistencias" IS 'Tabla de control de asistencias';
COMMENT ON TABLE "Jovenes" IS 'Tabla de jóvenes registrados';
COMMENT ON TABLE "Finanzas" IS 'Tabla de transacciones financieras';
COMMENT ON TABLE "Historial_Cambios" IS 'Tabla de auditoría de cambios en el sistema';
COMMENT ON TABLE "Informes" IS 'Tabla de informes generados';

-- =====================================================
-- FINALIZACIÓN
-- =====================================================

-- Verificar que todas las tablas se crearon correctamente
SELECT 'Configuración completada exitosamente' as mensaje; 