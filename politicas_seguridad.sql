-- Script de Políticas de Seguridad para Base de Datos en Supabase
-- Este script implementa las políticas de seguridad (RLS) para todas las tablas

-- ===== HABILITAR RLS EN TODAS LAS TABLAS =====

-- Habilitar RLS en todas las tablas
ALTER TABLE predicadores ENABLE ROW LEVEL SECURITY;
ALTER TABLE reuniones ENABLE ROW LEVEL SECURITY;
ALTER TABLE calendario ENABLE ROW LEVEL SECURITY;
ALTER TABLE bandeja ENABLE ROW LEVEL SECURITY;
ALTER TABLE asistencia ENABLE ROW LEVEL SECURITY;
ALTER TABLE jovenes ENABLE ROW LEVEL SECURITY;
ALTER TABLE movimientos_financieros ENABLE ROW LEVEL SECURITY;
ALTER TABLE historial_cambios ENABLE ROW LEVEL SECURITY;
ALTER TABLE consultas ENABLE ROW LEVEL SECURITY;
ALTER TABLE informes ENABLE ROW LEVEL SECURITY;
ALTER TABLE entidades_apoyo ENABLE ROW LEVEL SECURITY;
ALTER TABLE administradores ENABLE ROW LEVEL SECURITY;
ALTER TABLE productos ENABLE ROW LEVEL SECURITY;

-- ===== CREAR POLÍTICAS PARA CADA TABLA =====

-- Política para administradores (solo administradores autenticados pueden ver/editar)
CREATE POLICY policy_administradores ON administradores
    USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

-- Política para predicadores (todos pueden ver, solo autenticados pueden editar)
CREATE POLICY policy_predicadores_select ON predicadores
    FOR SELECT USING (true);

CREATE POLICY policy_predicadores_insert ON predicadores
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_predicadores_update ON predicadores
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_predicadores_delete ON predicadores
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para reuniones
CREATE POLICY policy_reuniones_select ON reuniones
    FOR SELECT USING (true);

CREATE POLICY policy_reuniones_insert ON reuniones
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_reuniones_update ON reuniones
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_reuniones_delete ON reuniones
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para jovenes
CREATE POLICY policy_jovenes_select ON jovenes
    FOR SELECT USING (true);

CREATE POLICY policy_jovenes_insert ON jovenes
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_jovenes_update ON jovenes
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_jovenes_delete ON jovenes
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para asistencia
CREATE POLICY policy_asistencia_select ON asistencia
    FOR SELECT USING (true);

CREATE POLICY policy_asistencia_insert ON asistencia
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_asistencia_update ON asistencia
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_asistencia_delete ON asistencia
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para movimientos_financieros (más restrictiva)
CREATE POLICY policy_movimientos_select ON movimientos_financieros
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY policy_movimientos_insert ON movimientos_financieros
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_movimientos_update ON movimientos_financieros
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_movimientos_delete ON movimientos_financieros
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para entidades_apoyo
CREATE POLICY policy_entidades_select ON entidades_apoyo
    FOR SELECT USING (true);

CREATE POLICY policy_entidades_insert ON entidades_apoyo
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_entidades_update ON entidades_apoyo
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_entidades_delete ON entidades_apoyo
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para productos
CREATE POLICY policy_productos_select ON productos
    FOR SELECT USING (true);

CREATE POLICY policy_productos_insert ON productos
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_productos_update ON productos
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_productos_delete ON productos
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para calendario
CREATE POLICY policy_calendario_select ON calendario
    FOR SELECT USING (true);

CREATE POLICY policy_calendario_insert ON calendario
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_calendario_update ON calendario
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_calendario_delete ON calendario
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para bandeja
CREATE POLICY policy_bandeja_select ON bandeja
    FOR SELECT USING (true);

CREATE POLICY policy_bandeja_insert ON bandeja
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_bandeja_update ON bandeja
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_bandeja_delete ON bandeja
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para consultas (solo administradores)
CREATE POLICY policy_consultas_select ON consultas
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY policy_consultas_insert ON consultas
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_consultas_update ON consultas
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_consultas_delete ON consultas
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para informes
CREATE POLICY policy_informes_select ON informes
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY policy_informes_insert ON informes
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_informes_update ON informes
    FOR UPDATE USING (auth.role() = 'authenticated')
    WITH CHECK (auth.role() = 'authenticated');

CREATE POLICY policy_informes_delete ON informes
    FOR DELETE USING (auth.role() = 'authenticated');

-- Política para historial_cambios (solo lectura para autenticados)
CREATE POLICY policy_historial_select ON historial_cambios
    FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY policy_historial_insert ON historial_cambios
    FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Políticas de seguridad (RLS) implementadas correctamente';
END $$;