# Estructura del Código - Sistema de Gestión

## 📁 Estructura de Directorios

```
Base de Datos/
├── app.py                          # Aplicación principal Flask
├── sesion.py                       # Gestión de autenticación y sesiones
├── tablas.py                       # Operaciones CRUD para tablas principales
├── formularios.py                  # Gestión de formularios
├── consultas.py                    # Consultas personalizadas y búsquedas
├── informes.py                     # Generación de informes
├── email.py                        # Utilidades de envío de correos
├── requirements.txt                # Dependencias de Python
├── render.yaml                     # Configuración de despliegue en Render
├── .env                           # Variables de entorno (local)
├── env_example.txt                # Ejemplo de variables de entorno
├── ESTRUCTURA_CODIGO.md           # Este archivo
├── README.md                      # Documentación principal
│
├── static/                        # Archivos estáticos
│   ├── css/
│   │   ├── main.css              # Estilos principales
│   │   ├── tablas.css            # Estilos para tablas
│   │   ├── formularios.css       # Estilos para formularios
│   │   ├── consultas.css         # Estilos para consultas
│   │   └── informes.css          # Estilos para informes
│   │
│   └── js/
│       ├── sesion.js             # Gestión de sesión en frontend
│       ├── tablas_formularios.js # Funciones para tablas y formularios
│       ├── consultas_select.js   # Funciones de consultas
│       ├── formularios_insert.js # Inserción de formularios
│       └── informes_export.js    # Exportación de informes
│
├── templates/                     # Plantillas HTML
│   ├── base.html                 # Plantilla base
│   ├── index.html                # Página de login
│   ├── Tablas.html               # Página de gestión de tablas
│   ├── Formulario.html           # Página de formularios
│   ├── Consultas.html            # Página de consultas
│   └── Informe.html              # Página de informes
│
└── settings/                     # Configuraciones y scripts
    ├── README_SETTINGS.md        # Documentación de configuración
    └── ejecutar/                 # Scripts de configuración y pruebas
        ├── README_EJECUTAR.md    # Documentación de scripts
        ├── setup_completo.sql    # Script SQL completo de configuración
        ├── crear_tablas.sql      # Creación de tablas
        ├── insertar_datos.sql    # Datos iniciales
        ├── configurar_rls.sql    # Políticas de seguridad
        ├── crear_indices.sql     # Índices de base de datos
        ├── crear_relaciones.sql  # Relaciones entre tablas
        ├── crear_triggers.sql    # Triggers para auditoría
        ├── test_supabase_connection.py    # Prueba de conexión
        ├── test_login_detallado.py        # Diagnóstico de login
        ├── verificar_tablas.py            # Verificación de tablas
        ├── probar_relaciones.py           # Prueba de relaciones
        └── limpiar_datos.py              # Limpieza de datos
```

## 🔧 Archivos Principales

### `app.py` - Aplicación Principal
- **Propósito**: Configuración de Flask y rutas principales
- **Funciones principales**:
  - Configuración de la aplicación Flask
  - Rutas de páginas web (`/`, `/tablas`, `/formularios`, etc.)
  - Rutas API para sesión (`/api/sesion/login`, `/api/sesion/logout`)
  - Rutas API para tablas (`/api/tablas/*`)
  - Rutas API para formularios (`/api/formularios/*`)
  - Rutas API para consultas (`/api/consultas/*`)
  - Rutas API para informes (`/api/informes/*`)
  - Manejo de errores (404, 500, 405)

### `sesion.py` - Gestión de Autenticación
- **Propósito**: Manejo de sesiones y autenticación
- **Funciones principales**:
  - `is_admin_by_name()`: Verificación de credenciales
  - `get_admin_role()`: Obtención de rol de usuario
  - `check_access()`: Verificación de acceso
  - `verificar_permiso()`: Verificación de permisos específicos
  - `registrar_cambio_historial()`: Auditoría de cambios
  - `validar_datos()`: Validación de datos de entrada

### `tablas.py` - Operaciones CRUD
- **Propósito**: Operaciones de base de datos para tablas principales
- **Tablas manejadas**:
  - `predicadores`: Gestión de predicadores
  - `reuniones`: Gestión de reuniones
  - `calendario`: Gestión de eventos del calendario
- **Funciones por tabla**:
  - `buscar_*_por_id()`: Búsqueda por ID
  - `obtener_ultima_id_y_registrar_*()`: Inserción con auto-incremento
  - `editar_*()`: Actualización de registros
  - `eliminar_*()`: Eliminación de registros

### `formularios.py` - Gestión de Formularios
- **Propósito**: Operaciones para formularios específicos
- **Formularios manejados**:
  - `bandeja`: Tareas y objetivos
  - `asistencias`: Control de asistencia
  - `jovenes`: Gestión de jóvenes
  - `finanzas`: Control financiero
- **Funciones**: CRUD completo para cada formulario

### `consultas.py` - Consultas Personalizadas
- **Propósito**: Consultas avanzadas y búsquedas
- **Funciones principales**:
  - `buscar_por_texto()`: Búsqueda de texto libre
  - `buscar_por_fecha()`: Búsqueda por rangos de fecha
  - `consulta_con_relaciones()`: Consultas con joins
  - `consulta_reuniones_predicador()`: Relación reuniones-predicador
  - `consulta_asistencias_joven()`: Relación asistencias-joven
  - `exportar_consulta()`: Exportación de resultados

### `informes.py` - Generación de Informes
- **Propósito**: Creación y gestión de informes
- **Funciones principales**:
  - `generar_informe_predicadores()`: Informes de predicadores
  - `generar_informe_finanzas()`: Informes financieros
  - `generar_informe_asistencias()`: Informes de asistencia
  - `vista_previa_informe()`: Vista previa de informes
  - `descargar_informe()`: Descarga de informes
  - `enviar_informe_email()`: Envío por correo

### `email.py` - Utilidades de Correo
- **Propósito**: Configuración y envío de correos
- **Funciones principales**:
  - `enviar_por_correo()`: Envío de correos
  - `verificar_configuracion_email()`: Verificación de configuración

## 🎨 Frontend (Static Files)

### CSS Files
- **`main.css`**: Estilos generales y layout
- **`tablas.css`**: Estilos específicos para tablas
- **`formularios.css`**: Estilos para formularios
- **`consultas.css`**: Estilos para página de consultas
- **`informes.css`**: Estilos para página de informes

### JavaScript Files
- **`sesion.js`**: Gestión de login/logout y verificación de sesión
- **`tablas_formularios.js`**: Funciones para CRUD de tablas y formularios
- **`consultas_select.js`**: Funciones para consultas y búsquedas
- **`formularios_insert.js`**: Inserción y validación de formularios
- **`informes_export.js`**: Generación y exportación de informes

## 📄 Templates HTML

### `base.html` - Plantilla Base
- **Propósito**: Plantilla base con navegación común
- **Incluye**: Header, navegación, footer, scripts comunes

### `index.html` - Página de Login
- **Propósito**: Formulario de autenticación
- **Características**: Formulario de login con nombre y código

### `Tablas.html` - Gestión de Tablas
- **Propósito**: Interfaz para gestionar tablas principales
- **Tablas**: Predicadores, Reuniones, Calendario
- **Funciones**: CRUD completo con modales

### `Formulario.html` - Formularios
- **Propósito**: Interfaz para formularios específicos
- **Formularios**: Bandeja, Asistencias, Jóvenes, Finanzas, Reuniones
- **Características**: Sistema de pestañas para diferentes formularios

### `Consultas.html` - Consultas
- **Propósito**: Interfaz para consultas personalizadas
- **Funciones**: Búsqueda por texto, fecha, relaciones

### `Informe.html` - Informes
- **Propósito**: Generación y gestión de informes
- **Funciones**: Crear, generar, descargar, compartir informes

## ⚙️ Configuración (Settings)

### Scripts SQL
- **`setup_completo.sql`**: Script completo de configuración
- **`crear_tablas.sql`**: Creación de todas las tablas
- **`insertar_datos.sql`**: Datos iniciales del sistema
- **`configurar_rls.sql`**: Políticas de seguridad RLS
- **`crear_indices.sql`**: Optimización de consultas
- **`crear_relaciones.sql`**: Relaciones entre tablas
- **`crear_triggers.sql`**: Triggers para auditoría

### Scripts Python de Prueba
- **`test_supabase_connection.py`**: Prueba de conexión a Supabase
- **`test_login_detallado.py`**: Diagnóstico completo de login
- **`verificar_tablas.py`**: Verificación de estructura de tablas
- **`probar_relaciones.py`**: Prueba de relaciones entre tablas
- **`limpiar_datos.py`**: Limpieza y mantenimiento de datos

## 🔗 Flujo de Datos

```
Frontend (HTML/JS) 
    ↓
API Routes (app.py)
    ↓
Business Logic (sesion.py, tablas.py, etc.)
    ↓
Supabase Database
```

## 🔐 Autenticación

1. **Login**: `index.html` → `sesion.js` → `/api/sesion/login`
2. **Verificación**: `is_admin_by_name()` en `sesion.py`
3. **Sesión**: Almacenada en `session['user_nombre']`
4. **Protección**: Verificación en cada endpoint protegido

## 📊 Base de Datos

### Tablas Principales
- **`administradores`**: Usuarios del sistema
- **`predicadores`**: Información de predicadores
- **`reuniones`**: Gestión de reuniones
- **`calendario`**: Eventos del calendario
- **`bandeja`**: Tareas y objetivos
- **`asistencias`**: Control de asistencia
- **`jovenes`**: Información de jóvenes
- **`finanzas`**: Control financiero
- **`historial_cambios`**: Auditoría de cambios

### Relaciones
- `asistencias` → `jovenes` (FK)
- `reuniones` → `predicadores` (FK)
- `finanzas` → `reuniones` (FK)

## 🚀 Despliegue

### Render Configuration
- **`render.yaml`**: Configuración de despliegue
- **Variables de entorno**: `SUPABASE_URL`, `SUPABASE_KEY`, `SECRET_KEY`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn app:app`

### Variables de Entorno Requeridas
```bash
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu-anon-key
SECRET_KEY=tu-secret-key
GMAIL_PASS=tu-contraseña-gmail (opcional)
``` 