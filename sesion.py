from flask import session, request, jsonify
from supabase import create_client, Client
import os
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración Supabase
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

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
        response = supabase.table('Administradores').select('*').eq('email', user_email).execute()
        
        if response.data:
            return True
        return False
    except Exception as e:
        logger.error(f'Error en check_access: {str(e)}')
        return False

def is_admin(email, codigo, nombre):
    """Verificar si un email está en la lista de administradores - convertido de isAdmin()"""
    try:
        logger.info(f'Iniciando verificación para: {email}, {nombre}')
        
        # Buscar en Supabase
        response = supabase.table('Administradores').select('*').eq('email', email.lower()).execute()
        
        if not response.data:
            logger.info('No se encontró el usuario en Administradores')
            return False
        
        admin_data = response.data[0]
        logger.info(f'Datos encontrados: {admin_data}')
        
        # Verificar coincidencia completa
        if (admin_data.get('email', '').lower() == email.lower() and 
            admin_data.get('codigo') == codigo and
            admin_data.get('nombre', '').lower() == nombre.lower()):
            logger.info('¡Coincidencia encontrada! Acceso permitido')
            return True
        
        logger.info('No se encontró coincidencia. Acceso denegado')
        return False
    except Exception as e:
        logger.error(f'Error en verificación: {str(e)}')
        return False

def is_super_admin(email):
    """Verificar si un usuario es Super Admin - convertido de isSuperAdmin()"""
    try:
        response = supabase.table('Administradores').select('*').eq('email', email.lower()).eq('rol', 'Super Admin').execute()
        return len(response.data) > 0
    except Exception as e:
        logger.error(f'Error al verificar super admin: {str(e)}')
        return False

def verificar_rol(email):
    """Verificar rol del usuario - convertido de verificarRol()"""
    try:
        response = supabase.table('Administradores').select('rol').eq('email', email.lower()).execute()
        if response.data:
            return response.data[0].get('rol')
        return None
    except Exception as e:
        logger.error(f'Error al verificar rol: {str(e)}')
        raise ValueError(f'Error al verificar rol: {str(e)}')

def verificar_permiso(email, operacion):
    """Verificar permisos específicos - convertido de verificarPermiso()"""
    try:
        rol = verificar_rol(email)
        if not rol:
            return False

        permisos = {
            'Super Admin': ['CRUD_ADMINS', 'CRUD_ALL'],
            'Admin': ['CRUD_BASIC']
        }

        permisos_rol = permisos.get(rol, [])
        
        operaciones_permitidas = {
            'agregarAdmin': ['CRUD_ADMINS'],
            'eliminarAdmin': ['CRUD_ADMINS'],
            'editarAdmin': ['CRUD_ADMINS'],
            'verAdmins': ['CRUD_ADMINS'],
            'crud_basico': ['CRUD_BASIC', 'CRUD_ALL']
        }

        permisos_necesarios = operaciones_permitidas.get(operacion, [])
        return any(p in permisos_rol for p in permisos_necesarios)
    except Exception as e:
        logger.error(f'Error al verificar permiso: {str(e)}')
        return False

def obtener_admins():
    """Obtener lista de administradores - convertido de obtenerAdmins()"""
    try:
        user_email = session.get('user_email')
        if not is_super_admin(user_email):
            raise ValueError('Solo los Super Administradores pueden ver la lista de administradores')
        
        response = supabase.table('Administradores').select('email, nombre, rol, fecha_agregado').execute()
        
        return [{
            'email': row['email'],
            'nombre': row['nombre'],
            'rol': row['rol'],
            'fecha': row.get('fecha_agregado')
        } for row in response.data]
    except Exception as e:
        logger.error(f'Error al obtener admins: {str(e)}')
        raise e

def agregar_admin(email, nombre, rol, codigo):
    """Agregar administrador - convertido de agregarAdmin()"""
    try:
        user_email = session.get('user_email')
        if not verificar_permiso(user_email, 'agregarAdmin'):
            raise ValueError('No tienes permisos para agregar administradores')
        
        # Verificar si ya existe
        existing = supabase.table('Administradores').select('*').eq('email', email.lower()).execute()
        if existing.data:
            raise ValueError('Este email ya es administrador')
        
        # Insertar nuevo administrador
        data = {
            'email': email.lower(),
            'nombre': nombre,
            'rol': rol,
            'codigo': codigo,
            'fecha_agregado': datetime.now().isoformat()
        }
        
        response = supabase.table('Administradores').insert(data).execute()
        return True
    except Exception as e:
        logger.error(f'Error al agregar admin: {str(e)}')
        raise e

def eliminar_admin(email):
    """Eliminar administrador - convertido de eliminarAdmin()"""
    try:
        user_email = session.get('user_email')
        if not verificar_permiso(user_email, 'eliminarAdmin'):
            raise ValueError('No tienes permisos para eliminar administradores')
        
        # Verificar que no se elimine a sí mismo
        if email.lower() == user_email.lower():
            raise ValueError('No puedes eliminarte a ti mismo como administrador')
        
        # Verificar que no sea el último administrador
        total_admins = supabase.table('Administradores').select('*', count='exact').execute()
        if total_admins.count <= 1:
            raise ValueError('No se puede eliminar al último administrador')
        
        # Eliminar administrador
        response = supabase.table('Administradores').delete().eq('email', email.lower()).execute()
        
        if not response.data:
            raise ValueError('Administrador no encontrado')
        
        return True
    except Exception as e:
        logger.error(f'Error al eliminar admin: {str(e)}')
        raise e

def check_super_admin():
    """Verificar si el usuario actual es Super Admin - convertido de checkSuperAdmin()"""
    try:
        user_email = session.get('user_email')
        return is_super_admin(user_email)
    except Exception as e:
        logger.error(f'Error en check_super_admin: {str(e)}')
        return False
