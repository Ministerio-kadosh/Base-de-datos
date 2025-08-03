-- Script para Eliminar Políticas y Tablas Existentes en Supabase
-- Este script elimina todas las políticas y tablas existentes para una remodelación limpia

-- ===== ELIMINAR POLÍTICAS DE SEGURIDAD (RLS) =====

-- Desactivar RLS para todas las tablas antes de eliminarlas
ALTER TABLE IF EXISTS predicadores DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS reuniones DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS calendario DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS bandeja DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS asistencia DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS asistencias DISABLE ROW LEVEL SECURITY; -- Por si existe la tabla antigua
ALTER TABLE IF EXISTS jovenes DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS movimientos_financieros DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS finanzas DISABLE ROW LEVEL SECURITY; -- Por si existe la tabla antigua
ALTER TABLE IF EXISTS historial_cambios DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS consultas DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS informes DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS entidades_apoyo DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS administradores DISABLE ROW LEVEL SECURITY;
ALTER TABLE IF EXISTS productos DISABLE ROW LEVEL SECURITY;

-- Eliminar todas las políticas existentes
DROP POLICY IF EXISTS policy_predicadores ON predicadores;
DROP POLICY IF EXISTS policy_reuniones ON reuniones;
DROP POLICY IF EXISTS policy_calendario ON calendario;
DROP POLICY IF EXISTS policy_bandeja ON bandeja;
DROP POLICY IF EXISTS policy_asistencia ON asistencia;
DROP POLICY IF EXISTS policy_asistencias ON asistencias; -- Por si existe la tabla antigua
DROP POLICY IF EXISTS policy_jovenes ON jovenes;
DROP POLICY IF EXISTS policy_movimientos_financieros ON movimientos_financieros;
DROP POLICY IF EXISTS policy_finanzas ON finanzas; -- Por si existe la tabla antigua
DROP POLICY IF EXISTS policy_historial_cambios ON historial_cambios;
DROP POLICY IF EXISTS policy_consultas ON consultas;
DROP POLICY IF EXISTS policy_informes ON informes;
DROP POLICY IF EXISTS policy_entidades_apoyo ON entidades_apoyo;
DROP POLICY IF EXISTS policy_administradores ON administradores;
DROP POLICY IF EXISTS policy_productos ON productos;

-- Eliminar políticas adicionales (usando comodín para asegurar que se eliminan todas)
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN (
        SELECT policyname, tablename 
        FROM pg_policies 
        WHERE schemaname = 'public'
    ) LOOP
        EXECUTE format('DROP POLICY IF EXISTS %I ON %I', r.policyname, r.tablename);
    END LOOP;
END
$$;

-- Eliminar políticas específicas por tipo de operación
DROP POLICY IF EXISTS policy_predicadores_select ON predicadores;
DROP POLICY IF EXISTS policy_predicadores_insert ON predicadores;
DROP POLICY IF EXISTS policy_predicadores_update ON predicadores;
DROP POLICY IF EXISTS policy_predicadores_delete ON predicadores;

DROP POLICY IF EXISTS policy_reuniones_select ON reuniones;
DROP POLICY IF EXISTS policy_reuniones_insert ON reuniones;
DROP POLICY IF EXISTS policy_reuniones_update ON reuniones;
DROP POLICY IF EXISTS policy_reuniones_delete ON reuniones;

DROP POLICY IF EXISTS policy_jovenes_select ON jovenes;
DROP POLICY IF EXISTS policy_jovenes_insert ON jovenes;
DROP POLICY IF EXISTS policy_jovenes_update ON jovenes;
DROP POLICY IF EXISTS policy_jovenes_delete ON jovenes;

DROP POLICY IF EXISTS policy_asistencia_select ON asistencia;
DROP POLICY IF EXISTS policy_asistencia_insert ON asistencia;
DROP POLICY IF EXISTS policy_asistencia_update ON asistencia;
DROP POLICY IF EXISTS policy_asistencia_delete ON asistencia;

DROP POLICY IF EXISTS policy_movimientos_select ON movimientos_financieros;
DROP POLICY IF EXISTS policy_movimientos_insert ON movimientos_financieros;
DROP POLICY IF EXISTS policy_movimientos_update ON movimientos_financieros;
DROP POLICY IF EXISTS policy_movimientos_delete ON movimientos_financieros;

DROP POLICY IF EXISTS policy_entidades_select ON entidades_apoyo;
DROP POLICY IF EXISTS policy_entidades_insert ON entidades_apoyo;
DROP POLICY IF EXISTS policy_entidades_update ON entidades_apoyo;
DROP POLICY IF EXISTS policy_entidades_delete ON entidades_apoyo;

DROP POLICY IF EXISTS policy_productos_select ON productos;
DROP POLICY IF EXISTS policy_productos_insert ON productos;
DROP POLICY IF EXISTS policy_productos_update ON productos;
DROP POLICY IF EXISTS policy_productos_delete ON productos;

DROP POLICY IF EXISTS policy_calendario_select ON calendario;
DROP POLICY IF EXISTS policy_calendario_insert ON calendario;
DROP POLICY IF EXISTS policy_calendario_update ON calendario;
DROP POLICY IF EXISTS policy_calendario_delete ON calendario;

DROP POLICY IF EXISTS policy_bandeja_select ON bandeja;
DROP POLICY IF EXISTS policy_bandeja_insert ON bandeja;
DROP POLICY IF EXISTS policy_bandeja_update ON bandeja;
DROP POLICY IF EXISTS policy_bandeja_delete ON bandeja;

DROP POLICY IF EXISTS policy_consultas_select ON consultas;
DROP POLICY IF EXISTS policy_consultas_insert ON consultas;
DROP POLICY IF EXISTS policy_consultas_update ON consultas;
DROP POLICY IF EXISTS policy_consultas_delete ON consultas;

DROP POLICY IF EXISTS policy_informes_select ON informes;
DROP POLICY IF EXISTS policy_informes_insert ON informes;
DROP POLICY IF EXISTS policy_informes_update ON informes;
DROP POLICY IF EXISTS policy_informes_delete ON informes;

DROP POLICY IF EXISTS policy_historial_select ON historial_cambios;
DROP POLICY IF EXISTS policy_historial_insert ON historial_cambios;

-- ===== ELIMINAR TABLAS EXISTENTES =====

-- Eliminar tablas en orden inverso de dependencia
DROP TABLE IF EXISTS informes CASCADE;
DROP TABLE IF EXISTS consultas CASCADE;
DROP TABLE IF EXISTS productos CASCADE;
DROP TABLE IF EXISTS movimientos_financieros CASCADE;
DROP TABLE IF EXISTS finanzas CASCADE; -- Por si existe la tabla antigua
DROP TABLE IF EXISTS asistencia CASCADE;
DROP TABLE IF EXISTS asistencias CASCADE; -- Por si existe la tabla antigua
DROP TABLE IF EXISTS entidades_apoyo CASCADE;
DROP TABLE IF EXISTS administradores CASCADE;
DROP TABLE IF EXISTS predicadores CASCADE;
DROP TABLE IF EXISTS reuniones CASCADE;
DROP TABLE IF EXISTS jovenes CASCADE;
DROP TABLE IF EXISTS calendario CASCADE;
DROP TABLE IF EXISTS bandeja CASCADE;
DROP TABLE IF EXISTS historial_cambios CASCADE;

-- Mensaje de confirmación
DO $$
BEGIN
    RAISE NOTICE 'Eliminación de políticas y tablas completada exitosamente';
END $$;