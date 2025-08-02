# 📋 Instrucciones para Ejecutar la Remodelación Limpia

## 🔍 Verificaciones Previas

### 1. Realizar Copia de Seguridad

**¡IMPORTANTE!** Antes de ejecutar el script de remodelación, es fundamental realizar una copia de seguridad de la base de datos actual.

```sql
-- En Supabase SQL Editor, ejecutar:
COPY (SELECT * FROM predicadores) TO '/tmp/predicadores_backup.csv' WITH CSV HEADER;
COPY (SELECT * FROM reuniones) TO '/tmp/reuniones_backup.csv' WITH CSV HEADER;
COPY (SELECT * FROM jovenes) TO '/tmp/jovenes_backup.csv' WITH CSV HEADER;
-- Repetir para todas las tablas importantes
```

Alternativamente, puedes usar la función de exportación de Supabase desde la interfaz gráfica.

### 2. Verificar Conexiones Activas

```sql
-- Verificar conexiones activas a la base de datos
SELECT * FROM pg_stat_activity WHERE datname = current_database();
```

### 3. Verificar Tablas Existentes

```sql
-- Listar todas las tablas existentes
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
```

## 🚀 Pasos para la Remodelación

### 1. Preparar el Entorno

- Asegúrate de tener acceso administrativo a Supabase
- Cierra todas las conexiones activas a la base de datos
- Ten a mano las credenciales de acceso

### 2. Ejecutar el Script de Remodelación

#### Opción A: Desde Supabase SQL Editor

1. Inicia sesión en tu panel de control de Supabase
2. Ve a la sección "SQL Editor"
3. Crea un nuevo query
4. Copia y pega el contenido completo del archivo `remodelacion_limpia.sql`
5. Haz clic en "Run" para ejecutar el script
6. Espera a que se complete la ejecución (puede tardar unos minutos)

#### Opción B: Desde la Línea de Comandos

```bash
# Usando psql (reemplaza los valores entre corchetes con tus credenciales)
psql -h [host] -U [usuario] -d [base_de_datos] -f remodelacion_limpia.sql
```

### 3. Verificar la Ejecución

Al final del script, deberías ver los siguientes mensajes:

```
NOTICE:  Remodelación limpia completada exitosamente
NOTICE:  Todas las tablas han sido creadas con la nueva estructura
NOTICE:  Políticas de seguridad (RLS) implementadas correctamente
```

## ✅ Verificaciones Posteriores

### 1. Verificar Tablas Creadas

```sql
-- Verificar que todas las tablas existen
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN (
    'predicadores', 'reuniones', 'calendario', 'bandeja', 
    'asistencia', 'jovenes', 'movimientos_financieros',
    'entidades_apoyo', 'administradores', 'productos',
    'consultas', 'informes', 'historial_cambios'
);
```

### 2. Verificar Estructura de Tablas

```sql
-- Verificar estructura de tabla predicadores (ejemplo)
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'predicadores' 
ORDER BY ordinal_position;
```

### 3. Verificar Políticas de Seguridad

```sql
-- Verificar políticas de seguridad implementadas
SELECT * FROM pg_policies WHERE schemaname = 'public';
```

### 4. Insertar Datos de Prueba

```sql
-- Insertar un administrador de prueba
INSERT INTO administradores (nombre_admin, rol_admin, codigo_acceso) 
VALUES ('Admin Prueba', 'superadmin', '$2b$12$1234567890123456789012'); -- Reemplazar con un hash bcrypt real

-- Insertar un predicador de prueba
INSERT INTO predicadores (nombre, apellido, telefono) 
VALUES ('Juan', 'Pérez', '555-1234');
```

### 5. Probar Consultas Básicas

```sql
-- Probar consulta básica
SELECT * FROM predicadores;
```

## 🔄 Actualizar la Aplicación

Después de ejecutar el script de remodelación, es necesario actualizar la aplicación para que funcione con la nueva estructura de la base de datos:

1. Actualizar las variables de entorno si es necesario
2. Reiniciar la aplicación
3. Probar todas las funcionalidades principales:
   - Inicio de sesión
   - Registro de predicadores
   - Consulta de reuniones
   - Registro de asistencia
   - Generación de informes

## 🛠️ Solución de Problemas

### Problema: Error al eliminar tablas

**Solución:** Verifica que no hay conexiones activas a las tablas y que tienes permisos suficientes.

```sql
-- Forzar cierre de conexiones a la base de datos
SELECT pg_terminate_backend(pid) 
FROM pg_stat_activity 
WHERE datname = current_database() AND pid <> pg_backend_pid();
```

### Problema: Error en políticas RLS

**Solución:** Verifica que la autenticación de Supabase está configurada correctamente.

```sql
-- Verificar configuración de autenticación
SELECT * FROM auth.config;
```

### Problema: Datos no aparecen después de la migración

**Solución:** Verifica las políticas RLS y asegúrate de estar autenticado correctamente.

```sql
-- Desactivar temporalmente RLS para una tabla específica (solo para diagnóstico)
ALTER TABLE predicadores DISABLE ROW LEVEL SECURITY;
-- No olvides volver a activarla después
```

## 📞 Contacto para Soporte

Si encuentras problemas durante la ejecución del script o después de la remodelación, puedes:

1. Revisar los logs de la aplicación
2. Consultar la documentación de Supabase
3. Contactar al equipo de desarrollo

---

**✅ Siguiendo estas instrucciones, la remodelación limpia de la base de datos debería completarse exitosamente.**