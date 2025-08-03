-- Script para crear un nuevo administrador con rol Super Admin
-- IMPORTANTE: Este script debe ejecutarse con privilegios de administrador en Supabase

-- Verificar si ya existe un administrador con ese nombre
DO $$
DECLARE
    admin_exists BOOLEAN;
    -- Hash SHA256 para 'adali-930'
    hash_codigo TEXT := 'fd7671ea0c36f044fca50b7121b7b62fd32c5be02c7d42e18f98e971556449b4';
    
    -- IMPORTANTE: Este es el hash SHA256 del código 'adali-930'
    -- Generado con: hashlib.sha256('adali-930'.encode()).hexdigest()
BEGIN
    -- Verificar si ya existe
    SELECT EXISTS (SELECT 1 FROM administradores WHERE nombre_admin = 'Darwin Garcia') INTO admin_exists;
    
    IF admin_exists THEN
        RAISE NOTICE 'Ya existe un administrador con el nombre Darwin Garcia';
    ELSE
        -- Usar el hash SHA256 para 'adali-930'
        -- Este hash fue generado con: hashlib.sha256('adali-930'.encode()).hexdigest()
        -- El sistema soporta tanto SHA256 como bcrypt para compatibilidad
        
        -- Insertar el nuevo administrador
        INSERT INTO administradores (nombre_admin, rol_admin, codigo_acceso, fecha_registro)
        VALUES ('Darwin Garcia', 'Super Admin', hash_codigo, CURRENT_TIMESTAMP);
        
        RAISE NOTICE 'Administrador Darwin Garcia creado exitosamente con rol Super Admin';
    END IF;
END;
$$;

-- Verificar que se haya creado correctamente
SELECT id_admin, nombre_admin, rol_admin, fecha_registro 
FROM administradores 
WHERE nombre_admin = 'Darwin Garcia';