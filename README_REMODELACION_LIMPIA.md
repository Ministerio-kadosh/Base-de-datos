# 🔄 Remodelación Limpia de Base de Datos

## 📋 Descripción

Este proyecto contiene un script SQL (`remodelacion_limpia.sql`) que realiza una remodelación completa de la base de datos en Supabase. El script elimina todas las tablas y políticas existentes y crea una estructura nueva y limpia según las especificaciones definidas en el archivo `Remodelacion.md`.

## ⚠️ Advertencia

**¡ATENCIÓN!** Este script eliminará **TODAS** las tablas y datos existentes en la base de datos. Asegúrate de hacer una copia de seguridad antes de ejecutarlo si necesitas conservar alguna información.

## 🚀 Cómo Usar

### Opción 1: Ejecutar en Supabase SQL Editor

1. Inicia sesión en tu panel de control de Supabase
2. Ve a la sección "SQL Editor"
3. Copia y pega el contenido del archivo `remodelacion_limpia.sql`
4. Haz clic en "Run" para ejecutar el script

### Opción 2: Ejecutar desde la línea de comandos

```bash
# Usando psql (asegúrate de tener las credenciales correctas)
psql -h [host] -U [usuario] -d [base_de_datos] -f remodelacion_limpia.sql
```

## ✅ Qué Hace Este Script

### 1. Elimina Políticas y Tablas Existentes

- Desactiva Row Level Security (RLS) en todas las tablas
- Elimina todas las políticas de seguridad existentes
- Elimina todas las tablas existentes en orden inverso de dependencia

### 2. Crea Nuevas Tablas

- Crea 13 tablas con la estructura correcta:
  - `administradores`
  - `entidades_apoyo`
  - `productos`
  - `predicadores`
  - `jovenes`
  - `reuniones`
  - `asistencia`
  - `movimientos_financieros`
  - `bandeja`
  - `calendario`
  - `consultas`
  - `informes`
  - `historial_cambios`

### 3. Crea Índices para Optimización

- Crea índices en campos clave para mejorar el rendimiento de las consultas

### 4. Implementa Políticas de Seguridad (RLS)

- Habilita Row Level Security en todas las tablas
- Crea políticas específicas para cada tabla:
  - Políticas de selección (SELECT)
  - Políticas de inserción (INSERT)
  - Políticas de actualización (UPDATE)
  - Políticas de eliminación (DELETE)

### 5. Verifica la Instalación

- Comprueba que todas las tablas se han creado correctamente
- Muestra mensajes de confirmación

## 🔒 Seguridad Implementada

El script implementa las siguientes medidas de seguridad:

1. **Row Level Security (RLS)** en todas las tablas
2. **Políticas de acceso** basadas en autenticación
3. **Restricciones de integridad referencial** entre tablas
4. **Campo para contraseñas** ampliado para almacenar hash bcrypt

## 📊 Estructura de Tablas

La estructura de tablas sigue las especificaciones definidas en `Remodelacion.md` y `MIGRACION_COMPLETADA.md`, con las siguientes características:

- Todos los campos siguen la convención `snake_case`
- Nombres descriptivos y coherentes
- Estructura uniforme en todas las tablas
- Campos de auditoría (fecha_registro, usuario_responsable)

## 🔍 Verificación

Para verificar que la remodelación fue exitosa:

1. Ejecuta el script completo
2. Verifica que se muestren los mensajes de confirmación
3. Comprueba que todas las tablas aparezcan en la lista de verificación

## 📞 Soporte

Si encuentras algún problema durante la ejecución del script:

1. Revisa los mensajes de error en la consola SQL
2. Verifica las credenciales y permisos de la base de datos
3. Asegúrate de que no hay conexiones activas a las tablas que se están eliminando

---

**✅ Este script implementa todas las mejoras y correcciones mencionadas en los archivos `MEJORAS_IMPLEMENTADAS.md` y `MIGRACION_COMPLETADA.md`**