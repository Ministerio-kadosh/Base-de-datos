# Scripts de Ejecución y Configuración

Esta carpeta contiene todos los scripts de prueba, configuración y utilidades para el sistema de gestión.

## 📋 Scripts Disponibles

### 🔧 Scripts de Configuración

#### `setup_supabase.py`
- **Propósito**: Configurar automáticamente Supabase con todas las tablas y datos iniciales
- **Uso**: `python setup_supabase.py`
- **Requisitos**: Variables de entorno SUPABASE_URL y SUPABASE_KEY configuradas

#### `env_example.txt`
- **Propósito**: Ejemplo de archivo .env con las variables de entorno necesarias
- **Uso**: Copiar a `.env` y configurar con tus credenciales de Supabase

### 🧪 Scripts de Prueba

#### `test_supabase_connection.py`
- **Propósito**: Verificar la conexión con Supabase y probar operaciones básicas
- **Uso**: `python test_supabase_connection.py`
- **Pruebas**: Conexión, tablas, administradores, predicadores, inserción, vistas

#### `test_tables.py`
- **Propósito**: Probar operaciones CRUD en todas las tablas del sistema
- **Uso**: `python test_tables.py`
- **Pruebas**: Crear, leer, actualizar, eliminar registros en cada tabla

#### `test_tablas_minusculas.py`
- **Propósito**: Verificar que todas las tablas con nombres en minúsculas funcionan correctamente
- **Uso**: `python test_tablas_minusculas.py`
- **Pruebas**: Tablas, login, relaciones entre tablas

#### `verificar_columnas.py`
- **Propósito**: Verificar los nombres exactos de las columnas en cada tabla
- **Uso**: `python verificar_columnas.py`
- **Resultado**: Muestra la estructura real de cada tabla en la base de datos

#### `probar_login.py`
- **Propósito**: Probar el sistema de login con credenciales reales
- **Uso**: `python probar_login.py`
- **Resultado**: Encuentra las credenciales válidas para hacer login

### 📄 Scripts SQL

#### `crear_tablas_faltantes.sql`
- **Propósito**: Crear las tablas que faltan en Supabase (asistencias, informes_generados)
- **Uso**: Ejecutar en el SQL Editor de Supabase
- **Incluye**: Tablas, índices, políticas RLS, datos de prueba

#### `supa_setup.sql`
- **Propósito**: Script completo de configuración inicial de Supabase
- **Uso**: Ejecutar en el SQL Editor de Supabase para crear todo el sistema
- **Incluye**: Todas las tablas, relaciones, índices, políticas, datos iniciales

### 📚 Documentación

#### `CAMBIOS_TABLAS_MINUSCULAS.md`
- **Propósito**: Documentar los cambios realizados para usar tablas con minúsculas
- **Contenido**: Lista de cambios, archivos modificados, instrucciones

## 🚀 Orden de Ejecución Recomendado

1. **Configurar variables de entorno**:
   ```bash
   cp env_example.txt .env
   # Editar .env con tus credenciales de Supabase
   ```

2. **Configurar Supabase**:
   ```bash
   python setup_supabase.py
   ```

3. **Verificar conexión**:
   ```bash
   python test_supabase_connection.py
   ```

4. **Verificar tablas**:
   ```bash
   python test_tablas_minusculas.py
   ```

5. **Verificar columnas**:
   ```bash
   python verificar_columnas.py
   ```

6. **Probar login**:
   ```bash
   python probar_login.py
   ```

7. **Probar operaciones**:
   ```bash
   python test_tables.py
   ```

## 🔑 Credenciales de Prueba

Después de ejecutar los scripts, puedes usar estas credenciales para hacer login:

- **Nombre**: Administrador Principal
- **Código**: 123456

## ⚠️ Notas Importantes

- Todos los scripts requieren las variables de entorno `SUPABASE_URL` y `SUPABASE_KEY`
- Los scripts SQL deben ejecutarse en el SQL Editor de Supabase
- Algunos scripts pueden modificar datos en la base de datos
- Siempre verifica el resultado de cada script antes de continuar

## 🛠️ Solución de Problemas

### Error: Variables de entorno no configuradas
```bash
# Crear archivo .env
cp env_example.txt .env
# Editar .env con tus credenciales
```

### Error: Tablas no existen
```bash
# Ejecutar script SQL en Supabase
# O usar setup_supabase.py
```

### Error: Login falla
```bash
# Verificar credenciales con probar_login.py
python probar_login.py
```

### Error: Columnas no coinciden
```bash
# Verificar estructura real con verificar_columnas.py
python verificar_columnas.py
``` 