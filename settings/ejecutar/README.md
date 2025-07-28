# ⚙️ Archivos de Configuración y Setup

Esta carpeta contiene archivos de configuración y setup para la aplicación.

## 📁 Archivos Incluidos:

### **setup_supabase.py**
- **Propósito**: Script de configuración inicial de Supabase
- **Uso**: `python setup_supabase.py`
- **Funciones**:
  - Crear tablas iniciales
  - Configurar índices
  - Establecer triggers de auditoría
  - Configurar RLS (Row Level Security)

### **crear_tablas_faltantes.sql**
- **Propósito**: Script SQL para crear tablas que faltan
- **Uso**: Ejecutar en Supabase SQL Editor
- **Funciones**:
  - Crear tablas faltantes
  - Configurar relaciones
  - Establecer restricciones

### **env_example.txt**
- **Propósito**: Ejemplo de variables de entorno
- **Uso**: Copiar a `.env` y configurar valores
- **Contenido**:
  - Variables de Supabase
  - Configuración de email
  - Claves secretas

### **README_EJECUTAR.md**
- **Propósito**: Documentación de ejecución
- **Uso**: Referencia para setup
- **Contenido**:
  - Instrucciones de instalación
  - Pasos de configuración
  - Troubleshooting

### **CAMBIOS_TABLAS_MINUSCULAS.md**
- **Propósito**: Documentación de cambios en estructura
- **Uso**: Referencia histórica
- **Contenido**:
  - Cambios realizados
  - Migraciones necesarias
  - Notas de compatibilidad

## ⚠️ IMPORTANTE:

- **Ejecutar solo una vez** durante la configuración inicial
- **Hacer backup** antes de ejecutar scripts SQL
- **Verificar variables de entorno** antes de ejecutar
- **Revisar documentación** antes de usar

## 🚀 Cómo Usar:

```bash
# 1. Configurar variables de entorno
cp env_example.txt .env
# Editar .env con tus valores

# 2. Ejecutar setup inicial
python setup_supabase.py

# 3. Ejecutar scripts SQL en Supabase
# Copiar y pegar crear_tablas_faltantes.sql en SQL Editor
```

## 🔧 Configuración Requerida:

- Cuenta de Supabase activa
- Variables de entorno configuradas
- Permisos de administrador en Supabase
- Python con dependencias instaladas

## 📝 Notas:

- Estos archivos son para **configuración inicial**
- No ejecutar en producción sin revisar
- Mantener actualizados con cambios en la estructura
- Documentar cualquier cambio realizado 