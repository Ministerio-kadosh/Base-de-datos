from flask import session, request, jsonify
from supabase.client import create_client, Client
import os
from datetime import datetime
import logging
import hashlib
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración Supabase
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def registrar_cambio_historial(tabla, id_registro, accion, datos_anteriores=None, datos_nuevos=None):
    """Registrar cambio en el historial"""
    try:
        nuevo_registro = {
            'tabla': tabla,
            'id_registro': id_registro,
            'accion': accion,
            'datos_anteriores': datos_anteriores,
            'datos_nuevos': datos_nuevos,
            'usuario': session.get('user_email', 'sistema'),
            'fecha_cambio': datetime.now().isoformat()
        }
        
        response = supabase.table('historial_cambios').insert(nuevo_registro).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error en registrar_cambio_historial: {e}")
        return None

# Esquemas de validación convertidos de JavaScript a Python
ESQUEMAS = {
    'Predicadores': {
        'Nombre': {'tipo': 'texto', 'requerido': True, 'maxLength': 50},
        'Apellido': {'tipo': 'texto', 'requerido': True, 'maxLength': 50},
        'Numero': {'tipo': 'numero', 'requerido': True}
    },
    'Administradores': {
        'email': {'tipo': 'email', 'requerido': True},
        'nombre': {'tipo': 'texto', 'requerido': True, 'maxLength': 50},
        'rol': {'tipo': 'texto', 'requerido': True},
        'codigo': {'tipo': 'texto', 'requerido': True}
    },
    'Bandeja': {
        'Objetivo': {'tipo': 'texto', 'requerido': True, 'maxLength': 100},
        'Descripcion': {'tipo': 'texto', 'requerido': True, 'maxLength': 500}
    }
}

def validar_datos(datos, esquema):
    """Validar datos según esquema - convertido de JavaScript"""
    try:
        if not datos or not isinstance(datos, dict):
            raise ValueError('Los datos proporcionados no son válidos')

        for campo, config in esquema.items():
            valor = datos.get(campo)
            
            # Verificar campos requeridos
            if config.get('requerido') and (valor is None or valor == ''):
                raise ValueError(f'El campo {campo} es requerido')

            # Verificar tipo de dato
            if valor is not None and valor != '':
                if config['tipo'] == 'numero':
                    try:
                        float(valor)
                    except (ValueError, TypeError):
                        raise ValueError(f'El campo {campo} debe ser un número')
                elif config['tipo'] == 'texto':
                    if not isinstance(valor, str):
                        raise ValueError(f'El campo {campo} debe ser texto')
                elif config['tipo'] == 'fecha':
                    try:
                        datetime.fromisoformat(valor.replace('Z', '+00:00'))
                    except ValueError:
                        raise ValueError(f'El campo {campo} debe ser una fecha válida')
                elif config['tipo'] == 'email':
                    import re
                    email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
                    if not re.match(email_regex, valor):
                        raise ValueError(f'El campo {campo} debe ser un email válido')

            # Verificar longitud máxima
            if config.get('maxLength') and valor and len(str(valor)) > config['maxLength']:
                raise ValueError(f'El campo {campo} no puede tener más de {config["maxLength"]} caracteres')

        return True
    except Exception as error:
        logger.error(f'Error en validar_datos: {str(error)}')
        raise error

def check_access():
    """Verificar si el usuario es administrador - convertido de checkAccess()"""
    try:
        user_email = session.get('user_email')
        if not user_email:
            return False
        
        # Buscar en tabla de administradores en Supabase
        response = supabase.table('administradores').select('*').eq('email', user_email).execute()
        
        if response.data:
            return True
        return False
    except Exception as e:
        logger.error(f'Error en check_access: {str(e)}')
        return False

def verificar_permiso(user_email, permiso):
    """Verificar si un usuario tiene un permiso específico - convertido de verificarPermiso()"""
    try:
        response = supabase.table('administradores').select('*').eq('email', user_email).execute()
        
        if response.data:
            admin = response.data[0]
            rol = admin.get('rol', 'Usuario')
            
            # Definir permisos por rol
            permisos_por_rol = {
                'Super Admin': ['agregarAdmin', 'eliminarAdmin', 'verHistorial', 'generarInformes'],
                'Admin': ['verHistorial', 'generarInformes'],
                'Usuario': []
            }
            
            return permiso in permisos_por_rol.get(rol, [])
        
        return False
    except Exception as e:
        print(f"Error en verificar_permiso: {e}")
        return False

def is_admin_by_name(nombre, codigo):
    """Verificar si es administrador por nombre y código"""
    try:
        # Comparar directamente el código (sin encriptar)
        response = supabase.table('administradores').select('*').eq('nombre', nombre).eq('codigo', codigo).eq('estado', 'Activo').execute()
        
        return len(response.data) > 0
    except Exception as e:
        print(f"Error en is_admin_by_name: {e}")
        return False

def get_admin_role(nombre):
    """Obtener el rol del administrador por nombre"""
    try:
        # Como la tabla no tiene columna 'rol', asignamos un rol por defecto
        # basado en el nombre del administrador
        if 'Principal' in nombre or 'Super' in nombre:
            return 'Super Admin'
        elif 'Admin' in nombre:
            return 'Admin'
        else:
            return 'Usuario'
    except Exception as e:
        print(f"Error en get_admin_role: {e}")
        return 'Usuario'

def is_admin(email, codigo, nombre):
    """Verificar si un email está en la lista de administradores - convertido de isAdmin()"""
    try:
        # Encriptar el código para comparar
        codigo_encriptado = hashlib.sha256(codigo.encode()).hexdigest()
        
        response = supabase.table('administradores').select('*').eq('email', email.lower()).eq('codigo', codigo_encriptado).eq('estado', 'Activo').execute()
        
        return len(response.data) > 0
    except Exception as e:
        print(f"Error en is_admin: {e}")
        return False

def is_super_admin(user_email):
    """Verificar si un usuario es super administrador - convertido de isSuperAdmin()"""
    try:
        response = supabase.table('administradores').select('*').eq('email', user_email.lower()).eq('rol', 'Super Admin').execute()
        
        return len(response.data) > 0
    except Exception as e:
        print(f"Error en is_super_admin: {e}")
        return False

def get_admin_role_by_email(user_email):
    """Obtener el rol de un administrador por email - convertido de getAdminRole()"""
    try:
        response = supabase.table('administradores').select('rol').eq('email', user_email.lower()).execute()
        
        if response.data:
            return response.data[0]['rol']
        return 'Usuario'
    except Exception as e:
        print(f"Error en get_admin_role_by_email: {e}")
        return 'Usuario'

def obtener_admins():
    """Obtener lista de administradores - convertido de obtenerAdmins()"""
    try:
        response = supabase.table('administradores').select('email, nombre, rol, fecha_creacion').execute()
        return response.data
    except Exception as e:
        print(f"Error en obtener_admins: {e}")
        raise e

def agregar_admin(nombre, rol, codigo):
    """Agregar un nuevo administrador"""
    try:
        # Encriptar el código
        codigo_encriptado = hashlib.sha256(codigo.encode()).hexdigest()
        
        # Verificar si ya existe un administrador con ese nombre
        response = supabase.table('administradores').select('*').eq('nombre', nombre).execute()
        
        if response.data:
            raise ValueError('Ya existe un administrador con ese nombre')
        
        # Insertar nuevo administrador
        datos_admin = {
            'nombre': nombre,
            'rol': rol,
            'codigo': codigo_encriptado,
            'fecha_creacion': datetime.now().isoformat(),
            'estado': 'Activo'
        }
        
        response = supabase.table('administradores').insert(datos_admin).execute()
        
        if response.data:
            return True
        else:
            raise ValueError('Error al agregar administrador')
            
    except Exception as e:
        print(f"Error en agregar_admin: {e}")
        raise e

def eliminar_admin(nombre):
    """Eliminar un administrador por nombre"""
    try:
        # Verificar si existe el administrador
        response = supabase.table('administradores').select('*').eq('nombre', nombre).execute()
        
        if not response.data:
            raise ValueError('Administrador no encontrado')
        
        # Soft delete - marcar como inactivo
        response = supabase.table('administradores').update({'estado': 'Inactivo'}).eq('nombre', nombre).execute()
        
        if response.data:
            return True
        else:
            raise ValueError('Error al eliminar administrador')
            
    except Exception as e:
        print(f"Error en eliminar_admin: {e}")
        raise e

def check_super_admin():
    """Verificar si el usuario actual es Super Admin - convertido de checkSuperAdmin()"""
    try:
        user_email = session.get('user_email')
        return is_super_admin(user_email)
    except Exception as e:
        logger.error(f'Error en check_super_admin: {str(e)}')
        return False
