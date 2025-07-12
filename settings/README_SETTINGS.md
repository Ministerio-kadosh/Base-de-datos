# 📁 Carpeta Settings - Archivos de Configuración

Esta carpeta contiene todos los archivos de configuración, documentación y utilidades del proyecto.

## 📋 **Contenido de la Carpeta**

### 🔧 **Scripts de Configuración**
- `supa_setup.sql` - Script SQL completo para configurar Supabase
- `setup_supabase.py` - Script Python para configuración automática
- `test_supabase_connection.py` - Script para probar conexión a Supabase

### 📚 **Documentación**
- `RELACIONES_IMPLEMENTADAS.md` - Documentación de relaciones entre tablas
- `CAMBIOS_SIN_EMAIL.md` - Documentación de cambios para sistema sin email
- `SUPABASE_SETUP.md` - Guía completa de configuración de Supabase
- `README.md` - Documentación general del proyecto

### 🧪 **Scripts de Prueba**
- `test_tables.py` - Script para verificar y poblar tablas con datos de prueba

### ⚙️ **Configuración**
- `env_example.txt` - Ejemplo de variables de entorno

## 🚀 **Cómo Usar**

### **1. Configurar Supabase**
```bash
# Ejecutar el script SQL en Supabase SQL Editor
# Copiar y pegar el contenido de supa_setup.sql
```

### **2. Probar Conexión**
```bash
python settings/test_supabase_connection.py
```

### **3. Verificar Tablas**
```bash
python settings/test_tables.py
```

### **4. Configurar Variables de Entorno**
```bash
# Usar env_example.txt como referencia
# Configurar en Render o localmente
```

## 📖 **Documentación Disponible**

- **RELACIONES_IMPLEMENTADAS.md**: Explica todas las relaciones entre tablas
- **CAMBIOS_SIN_EMAIL.md**: Detalla los cambios para eliminar email del sistema
- **SUPABASE_SETUP.md**: Guía paso a paso para configurar Supabase

## ⚠️ **Notas Importantes**

1. **No modificar** estos archivos durante el desarrollo normal
2. **Hacer backup** antes de ejecutar scripts de configuración
3. **Leer documentación** antes de ejecutar scripts
4. **Probar en desarrollo** antes de aplicar en producción

## 🔄 **Mantenimiento**

- Actualizar documentación cuando se hagan cambios importantes
- Mantener scripts de prueba actualizados
- Revisar variables de entorno periódicamente
- Actualizar ejemplos según sea necesario 