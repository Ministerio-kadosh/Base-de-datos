# 🧪 Archivos de Prueba y Diagnóstico

Esta carpeta contiene archivos de prueba y diagnóstico que **NO deben ejecutarse en producción**.

## 📁 Archivos Incluidos:

### **diagnostico_problemas.py**
- **Propósito**: Diagnóstico completo de la aplicación
- **Uso**: `python diagnostico_problemas.py`
- **Funciones**:
  - Verificar variables de entorno
  - Probar conexión a Supabase
  - Verificar tablas principales
  - Mostrar datos de administradores, predicadores, etc.

### **test_funciones.py**
- **Propósito**: Probar funciones de backend individualmente
- **Uso**: `python test_funciones.py`
- **Funciones**:
  - Probar funciones de búsqueda de predicadores
  - Probar funciones de búsqueda de reuniones
  - Probar funciones de formularios (bandeja, asistencias, etc.)

### **test_app.py**
- **Propósito**: Probar la aplicación Flask completa
- **Uso**: `python test_app.py` (requiere que app.py esté ejecutándose)
- **Funciones**:
  - Probar endpoint de salud
  - Probar login
  - Probar endpoints de predicadores, bandeja, reuniones

### **test_login_detallado.py**
- **Propósito**: Pruebas detalladas del sistema de login
- **Uso**: `python test_login_detallado.py`
- **Funciones**:
  - Probar diferentes escenarios de login
  - Verificar validaciones de credenciales
  - Probar casos edge de autenticación

### **probar_login.py**
- **Propósito**: Prueba simple del sistema de login
- **Uso**: `python probar_login.py`
- **Funciones**:
  - Probar login básico
  - Verificar respuesta del servidor

### **test_supabase_connection.py**
- **Propósito**: Pruebas detalladas de conexión a Supabase
- **Uso**: `python test_supabase_connection.py`
- **Funciones**:
  - Probar conexión a Supabase
  - Verificar permisos de acceso
  - Probar operaciones CRUD básicas

### **test_tablas_minusculas.py**
- **Propósito**: Verificar tablas con nombres en minúsculas
- **Uso**: `python test_tablas_minusculas.py`
- **Funciones**:
  - Verificar estructura de tablas
  - Probar consultas con nombres en minúsculas

### **test_tables.py**
- **Propósito**: Pruebas generales de tablas
- **Uso**: `python test_tables.py`
- **Funciones**:
  - Probar todas las tablas principales
  - Verificar operaciones CRUD
  - Probar relaciones entre tablas

### **verificar_columnas.py**
- **Propósito**: Verificar estructura de columnas
- **Uso**: `python verificar_columnas.py`
- **Funciones**:
  - Verificar columnas de cada tabla
  - Identificar columnas faltantes
  - Verificar tipos de datos

### **verificar_tablas_existentes.py**
- **Propósito**: Verificar qué tablas existen en Supabase
- **Uso**: `python verificar_tablas_existentes.py`
- **Funciones**:
  - Listar tablas existentes
  - Identificar tablas faltantes
  - Verificar estructura de tablas

## ⚠️ IMPORTANTE:

- **NO ejecutar estos archivos en producción**
- **Solo usar para desarrollo y debugging**
- **Mantener fuera del código de producción**

## 🚀 Cómo Usar:

```bash
# Navegar a la carpeta de pruebas
cd settings/test

# Ejecutar diagnóstico
python diagnostico_problemas.py

# Probar funciones
python test_funciones.py

# Verificar tablas
python verificar_tablas_existentes.py

# Probar aplicación (requiere app.py ejecutándose)
python test_app.py

# Probar login
python probar_login.py
python test_login_detallado.py

# Probar conexión a Supabase
python test_supabase_connection.py

# Verificar tablas y columnas
python test_tables.py
python test_tablas_minusculas.py
python verificar_columnas.py
```

## 🔧 Configuración Requerida:

- Variables de entorno configuradas (.env)
- Supabase conectado
- Dependencias instaladas (requirements.txt)

## 📝 Notas:

- Estos archivos son para **desarrollo y debugging únicamente**
- No incluir en despliegues de producción
- Mantener actualizados con cambios en el código principal 