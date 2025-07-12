from supabase import create_client, Client
import os
from datetime import datetime
import logging
from sesion import validar_datos, ESQUEMAS

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

def registrar_historial(datos):
    """Registrar cambios en el historial - convertido de registrarHistorial()"""
    try:
        # Mapear operación a estado
        estado_map = {
            'CREATE': 'Creado',
            'UPDATE': 'Editado',
            'DELETE': 'Eliminado'
        }

        estado = estado_map.get(datos['operacion'], datos['operacion'])
        
        # Crear nuevo registro
        nuevo_registro = {
            'fecha': datetime.now().isoformat(),
            'usuario': datos.get('usuario', 'sistema'),
            'estado': estado,
            'tabla': datos['tabla'],
            'id_registro': datos['id_registro'],
            'datos_anteriores': datos.get('datos_anteriores', {}),
            'datos_nuevos': datos.get('datos_nuevos', {})
        }
        
        # Insertar en tabla de historial
        response = supabase.table('Historial_Cambios').insert(nuevo_registro).execute()
        return response.data[0] if response.data else None
        
    except Exception as error:
        logger.error(f'Error al registrar en historial: {str(error)}')
        raise error

def buscar_predicadores_por_id(id=None):
    """Buscar predicadores por ID - convertido de buscarPredicadoresPorId()"""
    try:
        if id:
            # Buscar predicador específico
            response = supabase.table('Predicadores').select('*').eq('id', id).neq('estado', 'eliminado').execute()
            return response.data[0] if response.data else None
        else:
            # Obtener todos los predicadores activos
            response = supabase.table('Predicadores').select('*').neq('estado', 'eliminado').execute()
            return response.data
    except Exception as error:
        logger.error(f'Error en buscar_predicadores_por_id: {str(error)}')
        raise error

def obtener_ultima_id_y_registrar_predicadores(datos):
    """Registrar nuevo predicador - convertido de obtenerUltimaIdYRegistrarPredicadores()"""
    try:
        # Validar datos
        validar_datos(datos, ESQUEMAS['Predicadores'])
        
        # Preparar datos
        datos['fecha'] = datetime.now().isoformat()
        datos['estado'] = ESTADOS_HISTORIAL['CREADO']
        datos['usuario'] = datos.get('usuario', 'sistema')
        
        # Insertar en Supabase
        response = supabase.table('Predicadores').insert(datos).execute()
        
        if response.data:
            nuevo_predicador = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'CREATE',
                'tabla': 'Predicadores',
                'id_registro': nuevo_predicador['id'],
                'datos_nuevos': nuevo_predicador,
                'usuario': datos['usuario']
            })
            
            return nuevo_predicador
        
        raise ValueError('Error al crear predicador')
    except Exception as error:
        logger.error(f'Error en obtener_ultima_id_y_registrar_predicadores: {str(error)}')
        raise error

def editar_predicadores(datos):
    """Editar predicador - convertido de editarPredicadores()"""
    try:
        # Validar datos
        validar_datos(datos, ESQUEMAS['Predicadores'])
        
        # Obtener datos anteriores
        datos_anteriores = buscar_predicadores_por_id(datos['id'])
        if not datos_anteriores:
            raise ValueError('No se encontró el predicador a editar')
        
        # Preparar datos actualizados
        datos['fecha'] = datetime.now().isoformat()
        datos['estado'] = ESTADOS_HISTORIAL['EDITADO']
        datos['usuario'] = datos.get('usuario', 'sistema')
        
        # Actualizar en Supabase
        response = supabase.table('Predicadores').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            predicador_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'UPDATE',
                'tabla': 'Predicadores',
                'id_registro': datos['id'],
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': predicador_actualizado,
                'usuario': datos['usuario']
            })
            
            return predicador_actualizado
        
        raise ValueError('Error al actualizar predicador')
    except Exception as error:
        logger.error(f'Error en editar_predicadores: {str(error)}')
        raise error

def eliminar_predicadores(id):
    """Eliminar predicador (soft delete) - convertido de eliminarPredicadores()"""
    try:
        # Obtener datos actuales
        datos_actuales = buscar_predicadores_por_id(id)
        if not datos_actuales:
            raise ValueError('No se encontró el predicador a eliminar')
        
        # Soft delete - marcar como eliminado
        datos_actualizados = {
            'estado': ESTADOS_HISTORIAL['ELIMINADO'],
            'fecha': datetime.now().isoformat(),
            'usuario': datos_actuales.get('usuario', 'sistema')
        }
        
        # Actualizar en Supabase
        response = supabase.table('Predicadores').update(datos_actualizados).eq('id', id).execute()
        
        if response.data:
            predicador_eliminado = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'DELETE',
                'tabla': 'Predicadores',
                'id_registro': id,
                'datos_anteriores': datos_actuales,
                'datos_nuevos': predicador_eliminado,
                'usuario': datos_actualizados['usuario']
            })
            
            return True
        
        raise ValueError('Error al eliminar predicador')
    except Exception as error:
        logger.error(f'Error en eliminar_predicadores: {str(error)}')
        raise error

def buscar_reuniones_por_id(id=None):
    """Buscar reuniones por ID - convertido de buscarReunionesPorId()"""
    try:
        if id:
            # Buscar reunión específica
            response = supabase.table('Reuniones').select('*').eq('id', id).execute()
            return response.data[0] if response.data else None
        else:
            # Obtener todas las reuniones
            response = supabase.table('Reuniones').select('*').execute()
            return response.data
    except Exception as error:
        logger.error(f'Error en buscar_reuniones_por_id: {str(error)}')
        raise error

def obtener_ultima_id_y_registrar_reuniones(datos):
    """Registrar nueva reunión - convertido de obtenerUltimaIdYRegistrarReuniones()"""
    try:
        # Preparar datos
        datos['fecha'] = datetime.now().isoformat()
        
        # Insertar en Supabase
        response = supabase.table('Reuniones').insert(datos).execute()
        
        if response.data:
            nueva_reunion = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'CREATE',
                'tabla': 'Reuniones',
                'id_registro': nueva_reunion['id'],
                'datos_nuevos': nueva_reunion
            })
            
            return nueva_reunion['id']
        
        raise ValueError('Error al crear reunión')
    except Exception as error:
        logger.error(f'Error en obtener_ultima_id_y_registrar_reuniones: {str(error)}')
        raise error

def editar_reuniones(datos):
    """Editar reunión - convertido de editarReuniones()"""
    try:
        # Obtener datos anteriores
        datos_anteriores = buscar_reuniones_por_id(datos['id'])
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {datos["id"]}')
        
        # Preparar datos actualizados
        datos['fecha'] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        response = supabase.table('Reuniones').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            reunion_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'UPDATE',
                'tabla': 'Reuniones',
                'id_registro': datos['id'],
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': reunion_actualizada
            })
            
            return reunion_actualizada
        
        raise ValueError('Error al actualizar reunión')
    except Exception as error:
        logger.error(f'Error en editar_reuniones: {str(error)}')
        raise error

def eliminar_reuniones(id):
    """Eliminar reunión - convertido de eliminarReuniones()"""
    try:
        # Obtener datos antes de eliminar
        datos_anteriores = buscar_reuniones_por_id(id)
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {id}')
        
        # Eliminar de Supabase
        response = supabase.table('Reuniones').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_historial({
                'operacion': 'DELETE',
                'tabla': 'Reuniones',
                'id_registro': id,
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': None
            })
            
            return True
        
        raise ValueError('Error al eliminar reunión')
    except Exception as error:
        logger.error(f'Error al eliminar: {str(error)}')
        raise error

def buscar_calendario_por_id(id=None):
    """Buscar calendario por ID - convertido de buscarCalendarioPorId()"""
    try:
        if id:
            # Buscar evento específico
            response = supabase.table('Calendario').select('*').eq('id', id).execute()
            return response.data[0] if response.data else None
        else:
            # Obtener todos los eventos
            response = supabase.table('Calendario').select('*').execute()
            return response.data
    except Exception as error:
        logger.error(f'Error en buscar_calendario_por_id: {str(error)}')
        raise error

def obtener_ultima_id_y_registrar_calendario(datos):
    """Registrar nuevo evento - convertido de obtenerUltimaIdYRegistrarCalendario()"""
    try:
        # Preparar datos
        datos['fecha_de_registro'] = datetime.now().isoformat()
        
        # Insertar en Supabase
        response = supabase.table('Calendario').insert(datos).execute()
        
        if response.data:
            nuevo_evento = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'CREATE',
                'tabla': 'Calendario',
                'id_registro': nuevo_evento['id'],
                'datos_nuevos': nuevo_evento
            })
            
            return nuevo_evento['id']
        
        raise ValueError('Error al crear evento')
    except Exception as error:
        logger.error(f'Error en obtener_ultima_id_y_registrar_calendario: {str(error)}')
        raise error

def editar_calendario(datos):
    """Editar evento - convertido de editarCalendario()"""
    try:
        # Obtener datos anteriores
        datos_anteriores = buscar_calendario_por_id(datos['id'])
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {datos["id"]}')
        
        # Preparar datos actualizados
        datos['fecha_de_registro'] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        response = supabase.table('Calendario').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            evento_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'UPDATE',
                'tabla': 'Calendario',
                'id_registro': datos['id'],
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': evento_actualizado
            })
            
            return evento_actualizado
        
        raise ValueError('Error al actualizar evento')
    except Exception as error:
        logger.error(f'Error en editar_calendario: {str(error)}')
        raise error

def eliminar_calendario(id):
    """Eliminar evento - convertido de eliminarCalendario()"""
    try:
        # Obtener datos antes de eliminar
        datos_anteriores = buscar_calendario_por_id(id)
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {id}')
        
        # Eliminar de Supabase
        response = supabase.table('Calendario').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_historial({
                'operacion': 'DELETE',
                'tabla': 'Calendario',
                'id_registro': id,
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': None
            })
            
            return True
        
        raise ValueError('Error al eliminar evento')
    except Exception as error:
        logger.error(f'Error al eliminar: {str(error)}')
        raise error
