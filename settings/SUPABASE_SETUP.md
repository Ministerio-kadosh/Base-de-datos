# 🚀 Configuración de Base de Datos en Supabase

Este documento te guiará paso a paso para configurar tu base de datos en Supabase para el sistema de gestión Flask.

## 📋 Tabla de Contenidos

1. [Crear Proyecto en Supabase](#crear-proyecto-en-supabase)
2. [Configurar Base de Datos](#configurar-base-de-datos)
3. [Configurar Autenticación](#configurar-autenticación)
4. [Configurar Variables de Entorno](#configurar-variables-de-entorno)
5. [Probar Conexión](#probar-conexión)
6. [Estructura de Tablas](#estructura-de-tablas)
7. [Políticas de Seguridad](#políticas-de-seguridad)
8. [Solución de Problemas](#solución-de-problemas)

## 🏗️ Crear Proyecto en Supabase

### Paso 1: Crear Cuenta
1. Ve a [https://supabase.com](https://supabase.com)
2. Haz clic en "Start your project"
3. Inicia sesión con GitHub, Google o crea una cuenta

### Paso 2: Crear Proyecto
1. Haz clic en "New Project"
2. Selecciona tu organización
3. Completa la información:
   - **Name**: `sistema-gestion-flask` (o el nombre que prefieras)
   - **Database Password**: Genera una contraseña segura
   - **Region**: Selecciona la región más cercana
4. Haz clic en "Create new project"

### Paso 3: Esperar Configuración
- El proyecto tardará unos minutos en configurarse
- Verás un mensaje "Your project is ready" cuando termine

## 🗄️ Configurar Base de Datos

### Paso 1: Acceder al SQL Editor
1. En el dashboard de Supabase, ve a **SQL Editor**
2. Haz clic en **New Query**

### Paso 2: Ejecutar Script SQL
1. Copia todo el contenido del archivo `supabase_setup.sql`
2. Pégalo en el editor SQL
3. Haz clic en **Run** para ejecutar el script

### Paso 3: Verificar Tablas
1. Ve a **Table Editor** en el menú lateral
2. Verifica que se crearon todas las tablas:
   - Administradores
   - Predicadores
   - Reuniones
   - Calendario
   - Bandeja
   - Asistencias
   - Jovenes
   - Finanzas
   - Historial_Cambios
   - Informes

## 🔐 Configurar Autenticación

### Paso 1: Configuración General
1. Ve a **Authentication** > **Settings**
2. Configura:
   - **Site URL**: `http://localhost:5000` (para desarrollo)
   - **Redirect URLs**: `http://localhost:5000/**`
   - **Enable email confirmations**: Desactivado (para desarrollo)

### Paso 2: Configurar Proveedores
1. Ve a **Authentication** > **Providers**
2. **Email**: Mantén habilitado
3. **Google/GitHub**: Opcional, según tus necesidades

### Paso 3: Configurar Políticas RLS
Las políticas de Row Level Security ya están configuradas en el script SQL, pero puedes ajustarlas según tus necesidades en **Authentication** > **Policies**.

## ⚙️ Configurar Variables de Entorno

### Paso 1: Obtener Credenciales
1. Ve a **Settings** > **API**
2. Copia:
   - **Project URL**: `https://tu-proyecto.supabase.co`
   - **anon public**: Clave pública para operaciones del cliente
   - **service_role secret**: Clave secreta para operaciones del servidor

### Paso 2: Crear Archivo .env
1. Copia el archivo `env_example.txt` como `.env`
2. Reemplaza los valores con tus credenciales reales:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_KEY=tu_anon_key_aqui
SUPABASE_SERVICE_KEY=tu_service_role_key_aqui
SECRET_KEY=tu_secret_key_muy_segura_aqui
```

### Paso 3: Instalar Dependencias
```bash
pip install python-dotenv supabase
```

## 🧪 Probar Conexión

### Ejecutar Script de Prueba
```bash
python test_supabase_connection.py
```

Este script verificará:
- ✅ Conexión con Supabase
- ✅ Acceso a todas las tablas
- ✅ Operaciones básicas (SELECT, INSERT)
- ✅ Datos iniciales
- ✅ Vistas de estadísticas

## 📊 Estructura de Tablas

### Administradores
```sql
- id (UUID, Primary Key)
- email (VARCHAR, Unique)
- nombre (VARCHAR)
- rol (VARCHAR) -- 'Admin', 'Super Admin'
- codigo (VARCHAR)
- activo (BOOLEAN)
- fecha_agregado (TIMESTAMP)
- fecha_actualizacion (TIMESTAMP)
```

### Predicadores
```sql
- id (UUID, Primary Key)
- Nombre (VARCHAR)
- Apellido (VARCHAR)
- Numero (VARCHAR)
- estado (VARCHAR)
- fecha (TIMESTAMP)
- usuario (VARCHAR)
```

### Reuniones
```sql
- id (UUID, Primary Key)
- titulo (VARCHAR)
- descripcion (TEXT)
- fecha_reunion (TIMESTAMP)
- lugar (VARCHAR)
- tipo (VARCHAR)
- estado (VARCHAR)
- fecha (TIMESTAMP)
- usuario (VARCHAR)
```

### Calendario
```sql
- id (UUID, Primary Key)
- titulo (VARCHAR)
- descripcion (TEXT)
- fecha_inicio (TIMESTAMP)
- fecha_fin (TIMESTAMP)
- tipo_evento (VARCHAR)
- lugar (VARCHAR)
- estado (VARCHAR)
- fecha (TIMESTAMP)
- usuario (VARCHAR)
```

### Bandeja
```sql
- id (UUID, Primary Key)
- Objetivo (VARCHAR)
- Descripcion (VARCHAR)
- prioridad (VARCHAR)
- estado (VARCHAR)
- fecha_limite (TIMESTAMP)
- fecha (TIMESTAMP)
- usuario (VARCHAR)
```

### Asistencias
```sql
- id (UUID, Primary Key)
- nombre_persona (VARCHAR)
- fecha_asistencia (DATE)
- tipo_reunion (VARCHAR)
- presente (BOOLEAN)
- observaciones (TEXT)
- fecha (TIMESTAMP)
- usuario (VARCHAR)
```

### Jóvenes
```sql
- id (UUID, Primary Key)
- nombre (VARCHAR)
- apellido (VARCHAR)
- edad (INTEGER)
- telefono (VARCHAR)
- email (VARCHAR)
- direccion (TEXT)
- fecha_registro (DATE)
- estado (VARCHAR)
- fecha (TIMESTAMP)
- usuario (VARCHAR)
```

### Finanzas
```sql
- id (UUID, Primary Key)
- concepto (VARCHAR)
- monto (DECIMAL)
- tipo (VARCHAR) -- 'ingreso', 'gasto'
- categoria (VARCHAR)
- fecha_transaccion (DATE)
- descripcion (TEXT)
- estado (VARCHAR)
- fecha (TIMESTAMP)
- usuario (VARCHAR)
```

### Historial_Cambios
```sql
- id (UUID, Primary Key)
- fecha (TIMESTAMP)
- usuario (VARCHAR)
- estado (VARCHAR)
- tabla (VARCHAR)
- id_registro (UUID)
- datos_anteriores (JSONB)
- datos_nuevos (JSONB)
```

### Informes
```sql
- id (UUID, Primary Key)
- titulo (VARCHAR)
- descripcion (TEXT)
- consultas (JSONB)
- formato (VARCHAR)
- estado (VARCHAR)
- fecha_creacion (TIMESTAMP)
- fecha_actualizacion (TIMESTAMP)
- usuario (VARCHAR)
```

## 🔒 Políticas de Seguridad

### Row Level Security (RLS)
Todas las tablas tienen RLS habilitado con políticas que permiten:

- **Lectura**: Todos los usuarios autenticados
- **Escritura**: Solo usuarios autenticados
- **Administradores**: Solo Super Admins pueden gestionar administradores

### Políticas Específicas
- **Administradores**: Solo Super Admins pueden CRUD
- **Historial**: Solo lectura para auditoría
- **Otras tablas**: CRUD para usuarios autenticados

## 🚨 Solución de Problemas

### Error: "Connection failed"
- Verifica que las credenciales sean correctas
- Asegúrate de que el proyecto esté activo
- Revisa la URL del proyecto

### Error: "Table not found"
- Ejecuta el script SQL completo
- Verifica que las tablas se crearon en **Table Editor**

### Error: "RLS policy violation"
- Verifica que estés autenticado
- Revisa las políticas en **Authentication** > **Policies**

### Error: "Permission denied"
- Verifica que tengas los permisos correctos
- Asegúrate de usar la clave correcta (anon vs service_role)

### Variables de Entorno no Cargadas
```bash
# Instalar python-dotenv
pip install python-dotenv

# Verificar que el archivo .env existe
ls -la .env
```

## 📈 Monitoreo y Mantenimiento

### Dashboard de Supabase
- **Database**: Monitorear uso de almacenamiento
- **API**: Ver estadísticas de uso
- **Logs**: Revisar errores y actividad

### Backups
- Supabase realiza backups automáticos
- Puedes configurar backups manuales si es necesario

### Escalabilidad
- Supabase se escala automáticamente
- Considera actualizar el plan según el uso

## 🎯 Próximos Pasos

1. ✅ Ejecutar el script SQL
2. ✅ Configurar variables de entorno
3. ✅ Probar conexión
4. ✅ Ejecutar la aplicación Flask
5. 🔄 Personalizar según necesidades específicas
6. 🔄 Configurar autenticación avanzada si es necesario
7. 🔄 Implementar funciones específicas del negocio

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en el dashboard de Supabase
2. Consulta la [documentación oficial](https://supabase.com/docs)
3. Verifica que todas las tablas y políticas estén configuradas correctamente

---

**¡Tu base de datos Supabase está lista para usar! 🎉** 