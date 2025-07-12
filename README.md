# 🚀 Sistema de Gestión Flask con Supabase

Sistema de gestión completo desarrollado en Flask con base de datos Supabase.

## 📋 Características

- ✅ **Gestión de Predicadores** - CRUD completo
- ✅ **Gestión de Reuniones** - Programación y seguimiento
- ✅ **Calendario de Eventos** - Organización de actividades
- ✅ **Bandeja de Tareas** - Gestión de objetivos
- ✅ **Control de Asistencias** - Seguimiento de participación
- ✅ **Gestión de Jóvenes** - Base de datos de miembros
- ✅ **Finanzas** - Control de ingresos y gastos
- ✅ **Informes** - Generación de reportes
- ✅ **Auditoría** - Historial de cambios
- ✅ **Autenticación** - Sistema de usuarios y roles

## 🛠️ Tecnologías

- **Backend**: Flask (Python)
- **Base de Datos**: Supabase (PostgreSQL)
- **Frontend**: HTML, CSS, JavaScript
- **Despliegue**: Render

## 🚀 Instalación Local

### 1. Clonar el repositorio
```bash
git clone <tu-repositorio>
cd "Base de Datos"
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno
```bash
# Copiar plantilla
copy settings\env_example.txt .env

# Editar con tus credenciales
notepad .env
```

### 4. Configurar Supabase
- Crear proyecto en [Supabase](https://supabase.com)
- Ejecutar `settings/supabase_setup.sql` en el SQL Editor
- Configurar credenciales en `.env`

### 5. Probar conexión
```bash
python settings/test_supabase_connection.py
```

### 6. Ejecutar aplicación
```bash
python app.py
```

## 🌐 Despliegue en Render

### 1. Conectar repositorio
- Conectar tu repositorio de GitHub a Render
- Configurar como servicio web

### 2. Configurar variables de entorno
En el dashboard de Render, configurar:
- `SUPABASE_URL`
- `SUPABASE_KEY`
- `SUPABASE_SERVICE_KEY`
- `SECRET_KEY`
- `GMAIL_PASS` (opcional)

### 3. Desplegar
Render automáticamente:
- Instalará dependencias desde `requirements.txt`
- Ejecutará `gunicorn app:app`
- Configurará el dominio

## 📁 Estructura del Proyecto

```
Base de Datos/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias Python
├── render.yaml           # Configuración de Render
├── .env                  # Variables de entorno (local)
├── .gitignore           # Archivos a ignorar
├── templates/           # Plantillas HTML
├── static/              # Archivos estáticos (CSS, JS)
├── settings/            # Archivos de configuración
│   ├── supabase_setup.sql
│   ├── test_supabase_connection.py
│   ├── SUPABASE_SETUP.md
│   └── env_example.txt
└── *.py                 # Módulos de la aplicación
```

## 🔧 Módulos Principales

- **`app.py`** - Rutas y configuración principal
- **`sesion.py`** - Autenticación y gestión de usuarios
- **`tablas.py`** - Operaciones CRUD de tablas principales
- **`formularios.py`** - Gestión de formularios y datos
- **`consultas.py`** - Consultas personalizadas y búsquedas
- **`informes.py`** - Generación de informes y reportes
- **`email_utils.py`** - Envío de correos electrónicos

## 🔐 Seguridad

- **Row Level Security (RLS)** habilitado en Supabase
- **Autenticación** basada en roles (Admin, Super Admin)
- **Auditoría** completa de cambios
- **Validación** de datos en frontend y backend

## 📊 Base de Datos

### Tablas Principales
- **Administradores** - Usuarios del sistema
- **Predicadores** - Gestión de predicadores
- **Reuniones** - Programación de reuniones
- **Calendario** - Eventos y actividades
- **Bandeja** - Tareas y objetivos
- **Asistencias** - Control de participación
- **Jóvenes** - Base de datos de miembros
- **Finanzas** - Control financiero
- **Historial_Cambios** - Auditoría
- **Informes** - Reportes generados

## 🎯 Funcionalidades

### Gestión de Contenido
- ✅ CRUD completo para todas las entidades
- ✅ Búsquedas avanzadas y filtros
- ✅ Exportación de datos
- ✅ Historial de cambios

### Informes
- ✅ Generación de reportes personalizados
- ✅ Exportación en múltiples formatos
- ✅ Envío por correo electrónico
- ✅ Vistas de estadísticas

### Usabilidad
- ✅ Interfaz responsive
- ✅ Navegación intuitiva
- ✅ Validaciones en tiempo real
- ✅ Mensajes de confirmación

## 🚨 Solución de Problemas

### Error de conexión con Supabase
1. Verificar credenciales en `.env`
2. Ejecutar script de prueba
3. Revisar políticas RLS en Supabase

### Error de dependencias
```bash
pip install -r requirements.txt
```

### Error de variables de entorno
1. Verificar archivo `.env`
2. Configurar todas las variables requeridas

## 📞 Soporte

Para problemas técnicos:
1. Revisar logs en Render
2. Verificar configuración de Supabase
3. Ejecutar script de prueba de conexión

## 📄 Licencia

Este proyecto es de uso interno y privado.

---

**¡Sistema listo para producción! 🎉** 