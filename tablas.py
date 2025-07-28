from flask import session, request, jsonify
from supabase.client import create_client, Client
import os
from datetime import datetime
import logging
from dotenv import load_dotenv
from sesion import validar_datos, ESQUEMAS

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración Supabase
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

# Estados del historial convertidos de JavaScript
ESTADOS_HISTORIAL = {
    'CREADO': 'Creado',
    'EDITADO': 'Editado',
    'ELIMINADO': 'Eliminado',
    'RESTAURADO': 'Restaurado',
    'REVERTIDO': 'Revertido',
    'INVALIDO': 'Inválido'
}

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

def buscar_predicadores_por_id(id=None):
    """Buscar predicadores por ID o todos - convertido de buscarPredicadoresPorId()"""
    try:
        if id:
            response = supabase.table('predicadores').select('*').eq('id', id).execute()
        else:
            response = supabase.table('predicadores').select('*').execute()
        
        return response.data
    except Exception as e:
        print(f"Error en buscar_predicadores_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_predicadores(datos):
    """Obtener última ID y registrar predicador - convertido de obtenerUltimaIdYRegistrarPredicadores()"""
    try:
        # Agregar metadatos
        datos['estado'] = 'Activo'
        datos['fecha'] = datetime.now().isoformat()
        datos['usuario'] = session.get('user_email', 'sistema')
        
        # Insertar predicador
        response = supabase.table('predicadores').insert(datos).execute()
        
        if response.data:
            predicador = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'predicadores',
                predicador['id'],
                'INSERT',
                None,
                predicador
            )
            
            return predicador
        else:
            raise ValueError('Error al registrar predicador')
            
    except Exception as e:
        print(f"Error en obtener_ultima_id_y_registrar_predicadores: {e}")
        raise e

def editar_predicadores(datos):
    """Editar predicador - convertido de editarPredicadores()"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('predicadores').select('*').eq('id', datos['id']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Actualizar datos
        datos['usuario'] = session.get('user_email', 'sistema')
        datos['fecha_actualizacion'] = datetime.now().isoformat()
        
        response = supabase.table('predicadores').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            predicador_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'predicadores',
                predicador_actualizado['id'],
                'UPDATE',
                datos_anteriores,
                predicador_actualizado
            )
            
            return predicador_actualizado
        else:
            raise ValueError('Error al actualizar predicador')
            
    except Exception as e:
        print(f"Error en editar_predicadores: {e}")
        raise e

def eliminar_predicadores(id):
    """Eliminar predicador (soft delete) - convertido de eliminarPredicadores()"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('predicadores').select('*').eq('id', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Soft delete
        datos_actualizados = {
            'estado': 'eliminado',
            'usuario': session.get('user_email', 'sistema'),
            'fecha_eliminacion': datetime.now().isoformat()
        }
        
        response = supabase.table('predicadores').update(datos_actualizados).eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'predicadores',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar predicador')
            
    except Exception as e:
        print(f"Error en eliminar_predicadores: {e}")
        raise e

def buscar_reuniones_por_id(id=None):
    """Buscar reuniones por ID o todas - convertido de buscarReunionesPorId()"""
    try:
        if id:
            response = supabase.table('reuniones').select('*').eq('id', id).execute()
        else:
            response = supabase.table('reuniones').select('*').execute()
        
        return response.data
    except Exception as e:
        print(f"Error en buscar_reuniones_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_reuniones(datos):
    """Obtener última ID y registrar reunión - convertido de obtenerUltimaIdYRegistrarReuniones()"""
    try:
        # Agregar metadatos
        datos['fecha'] = datetime.now().isoformat()
        datos['usuario'] = session.get('user_email', 'sistema')
        
        # Insertar reunión
        response = supabase.table('reuniones').insert(datos).execute()
        
        if response.data:
            reunion = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'reuniones',
                reunion['id'],
                'INSERT',
                None,
                reunion
            )
            
            return reunion['id']
        else:
            raise ValueError('Error al registrar reunión')
            
    except Exception as e:
        print(f"Error en obtener_ultima_id_y_registrar_reuniones: {e}")
        raise e

def editar_reuniones(datos):
    """Editar reunión - convertido de editarReuniones()"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('reuniones').select('*').eq('id', datos['id']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Actualizar datos
        datos['usuario'] = session.get('user_email', 'sistema')
        datos['fecha_actualizacion'] = datetime.now().isoformat()
        
        response = supabase.table('reuniones').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            reunion_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'reuniones',
                reunion_actualizada['id'],
                'UPDATE',
                datos_anteriores,
                reunion_actualizada
            )
            
            return reunion_actualizada
        else:
            raise ValueError('Error al actualizar reunión')
            
    except Exception as e:
        print(f"Error en editar_reuniones: {e}")
        raise e

def eliminar_reuniones(id):
    """Eliminar reunión - convertido de eliminarReuniones()"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('reuniones').select('*').eq('id', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar reunión
        response = supabase.table('reuniones').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'reuniones',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar reunión')
            
    except Exception as e:
        print(f"Error en eliminar_reuniones: {e}")
        raise e

def buscar_calendario_por_id(id=None):
    """Buscar calendario por ID o todo - convertido de buscarCalendarioPorId()"""
    try:
        if id:
            response = supabase.table('calendario').select('*').eq('id', id).execute()
        else:
            response = supabase.table('calendario').select('*').execute()
        
        return response.data
    except Exception as e:
        print(f"Error en buscar_calendario_por_id: {e}")
        raise e

def obtener_ultima_id_y_registrar_calendario(datos):
    """Obtener última ID y registrar evento de calendario - convertido de obtenerUltimaIdYRegistrarCalendario()"""
    try:
        # Agregar metadatos
        datos['fecha_creacion'] = datetime.now().isoformat()
        datos['usuario'] = session.get('user_email', 'sistema')
        
        # Insertar evento
        response = supabase.table('calendario').insert(datos).execute()
        
        if response.data:
            evento = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'calendario',
                evento['id'],
                'INSERT',
                None,
                evento
            )
            
            return evento['id']
        else:
            raise ValueError('Error al registrar evento de calendario')
            
    except Exception as e:
        print(f"Error en obtener_ultima_id_y_registrar_calendario: {e}")
        raise e

def editar_calendario(datos):
    """Editar evento de calendario - convertido de editarCalendario()"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('calendario').select('*').eq('id', datos['id']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Actualizar datos
        datos['usuario'] = session.get('user_email', 'sistema')
        datos['fecha_actualizacion'] = datetime.now().isoformat()
        
        response = supabase.table('calendario').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            evento_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'calendario',
                evento_actualizado['id'],
                'UPDATE',
                datos_anteriores,
                evento_actualizado
            )
            
            return evento_actualizado
        else:
            raise ValueError('Error al actualizar evento de calendario')
            
    except Exception as e:
        print(f"Error en editar_calendario: {e}")
        raise e

def eliminar_calendario(id):
    """Eliminar evento de calendario - convertido de eliminarCalendario()"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('calendario').select('*').eq('id', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar evento
        response = supabase.table('calendario').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'calendario',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar evento de calendario')
            
    except Exception as e:
        print(f"Error en eliminar_calendario: {e}")
        raise e
