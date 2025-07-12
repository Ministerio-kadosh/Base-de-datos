# Configuración del Sistema de Gestión

Esta carpeta contiene todos los archivos de configuración, documentación y scripts de ejecución del sistema.

## 📁 Estructura de Carpetas

### 📂 `ejecutar/`
Contiene todos los scripts de prueba, configuración y utilidades ejecutables.

**Ver documentación completa**: [README_EJECUTAR.md](ejecutar/README_EJECUTAR.md)

**Scripts principales**:
- `test_supabase_connection.py` - Verificar conexión con Supabase
- `test_tablas_minusculas.py` - Probar tablas con nombres en minúsculas
- `probar_login.py` - Probar sistema de login
- `verificar_columnas.py` - Verificar estructura de columnas
- `setup_supabase.py` - Configurar Supabase automáticamente

## 📄 Archivos de Documentación

### `README.md`
Documentación completa del sistema de gestión, incluyendo:
- Arquitectura del sistema
- Configuración de Supabase
- Estructura de la base de datos
- Guías de uso
- Solución de problemas

### `SUPABASE_SETUP.md`
Guía detallada para configurar Supabase desde cero:
- Creación del proyecto
- Configuración de tablas
- Políticas de seguridad (RLS)
- Datos iniciales

### `RELACIONES_IMPLEMENTADAS.md`
Documentación de las relaciones entre tablas:
- Claves foráneas
- Consultas con joins
- Ejemplos de uso

### `CAMBIOS_SIN_EMAIL.md`
Documentación de los cambios realizados para eliminar la dependencia del email:
- Modificaciones en autenticación
- Nuevo flujo de login
- Cambios en la base de datos

## 🚀 Inicio Rápido

1. **Ir a la carpeta de scripts**:
   ```bash
   cd settings/ejecutar
   ```

2. **Configurar variables de entorno**:
   ```bash
   cp env_example.txt .env
   # Editar .env con tus credenciales
   ```

3. **Ejecutar configuración**:
   ```bash
   python setup_supabase.py
   ```

4. **Verificar funcionamiento**:
   ```bash
   python test_supabase_connection.py
   python test_tablas_minusculas.py
   ```

## 🔑 Credenciales de Prueba

- **Nombre**: Administrador Principal
- **Código**: 123456

## 📋 Scripts SQL

### `supa_setup.sql`
Script completo para crear todo el sistema en Supabase:
- Todas las tablas
- Relaciones y claves foráneas
- Índices para rendimiento
- Políticas de seguridad (RLS)
- Datos iniciales

**Uso**: Ejecutar en el SQL Editor de Supabase

## ⚠️ Notas Importantes

- Todos los scripts requieren configuración de variables de entorno
- Los scripts SQL modifican la base de datos
- Siempre hacer backup antes de ejecutar scripts de configuración
- Verificar resultados antes de continuar

## 🛠️ Solución de Problemas

Para problemas específicos, consultar:
- [README_EJECUTAR.md](ejecutar/README_EJECUTAR.md) - Scripts de prueba y diagnóstico
- [SUPABASE_SETUP.md](SUPABASE_SETUP.md) - Configuración de Supabase
- [README.md](README.md) - Documentación completa del sistema 