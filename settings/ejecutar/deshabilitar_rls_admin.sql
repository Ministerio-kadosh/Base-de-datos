-- Script para deshabilitar temporalmente las políticas RLS en la tabla administradores
-- IMPORTANTE: Este script debe ejecutarse con privilegios de administrador en Supabase

-- Deshabilitar RLS para la tabla administradores
ALTER TABLE administradores DISABLE ROW LEVEL SECURITY;

-- Verificar el estado de RLS
SELECT tablename, rowsecurity FROM pg_tables WHERE tablename = 'administradores';

-- NOTA: Después de crear el administrador, se recomienda volver a habilitar RLS con:
-- ALTER TABLE administradores ENABLE ROW LEVEL SECURITY;