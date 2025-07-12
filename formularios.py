from supabase import create_client, Client
import os
from datetime import datetime
import logging
from sesion import validar_datos, ESQUEMAS
from tablas import registrar_historial

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración Supabase
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def buscar_bandeja_por_id(id=None):
    """Buscar bandeja por ID - convertido de buscarBandejaPorId()"""
    try:
        if id:
            # Buscar tarea específica
            response = supabase.table('Bandeja').select('*').eq('id', id).execute()
            return response.data[0] if response.data else None
        else:
            # Obtener todas las tareas
            response = supabase.table('Bandeja').select('*').execute()
            return response.data
    except Exception as error:
        logger.error(f'Error en buscar_bandeja_por_id: {str(error)}')
        raise error

def obtener_ultima_id_y_registrar_bandeja(datos):
    """Registrar nueva tarea en bandeja - convertido de obtenerUltimaIdYRegistrarBandeja()"""
    try:
        # Validar datos
        validar_datos(datos, ESQUEMAS['Bandeja'])
        
        # Preparar datos
        datos['fecha'] = datetime.now().isoformat()
        datos['estado'] = 'creado'
        
        # Insertar en Supabase
        response = supabase.table('Bandeja').insert(datos).execute()
        
        if response.data:
            nueva_tarea = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'CREATE',
                'tabla': 'Bandeja',
                'id_registro': nueva_tarea['id'],
                'datos_nuevos': nueva_tarea
            })
            
            return nueva_tarea
        
        raise ValueError('Error al crear tarea')
    except Exception as error:
        logger.error(f'Error en obtener_ultima_id_y_registrar_bandeja: {str(error)}')
        raise error

def actualizar_estados_bandeja():
    """Actualizar estados de bandeja - convertido de actualizarEstadosBandeja()"""
    try:
        # Obtener todas las tareas sin estado
        response = supabase.table('Bandeja').select('*').is_('estado', 'null').execute()
        
        if response.data:
            for tarea in response.data:
                # Actualizar estado a 'creado'
                supabase.table('Bandeja').update({'estado': 'creado'}).eq('id', tarea['id']).execute()
        
        return True
    except Exception as error:
        logger.error(f'Error en actualizar_estados_bandeja: {str(error)}')
        raise error

def editar_bandeja(datos):
    """Editar tarea de bandeja - convertido de editarBandeja()"""
    try:
        # Obtener datos anteriores
        datos_anteriores = buscar_bandeja_por_id(datos['id'])
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {datos["id"]}')
        
        # Preparar datos actualizados
        datos['fecha'] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        response = supabase.table('Bandeja').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            tarea_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'UPDATE',
                'tabla': 'Bandeja',
                'id_registro': datos['id'],
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': tarea_actualizada
            })
            
            return tarea_actualizada
        
        raise ValueError('Error al actualizar tarea')
    except Exception as error:
        logger.error(f'Error en editar_bandeja: {str(error)}')
        raise error

def eliminar_bandeja(id):
    """Eliminar tarea de bandeja - convertido de eliminarBandeja()"""
    try:
        # Obtener datos antes de eliminar
        datos_anteriores = buscar_bandeja_por_id(id)
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {id}')
        
        # Eliminar de Supabase
        response = supabase.table('Bandeja').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_historial({
                'operacion': 'DELETE',
                'tabla': 'Bandeja',
                'id_registro': id,
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': None
            })
            
            return True
        
        raise ValueError('Error al eliminar tarea')
    except Exception as error:
        logger.error(f'Error al eliminar: {str(error)}')
        raise error

def buscar_asistencias_por_id(id=None):
    """Buscar asistencias por ID - convertido de buscarAsistenciasPorId()"""
    try:
        if id:
            # Buscar asistencia específica
            response = supabase.table('Asistencias').select('*').eq('id', id).execute()
            return response.data[0] if response.data else None
        else:
            # Obtener todas las asistencias
            response = supabase.table('Asistencias').select('*').execute()
            return response.data
    except Exception as error:
        logger.error(f'Error en buscar_asistencias_por_id: {str(error)}')
        raise error

def obtener_ultima_id_y_registrar_asistencias(datos):
    """Registrar nueva asistencia - convertido de obtenerUltimaIdYRegistrarAsistencias()"""
    try:
        # Preparar datos
        datos['fecha'] = datetime.now().isoformat()
        
        # Insertar en Supabase
        response = supabase.table('Asistencias').insert(datos).execute()
        
        if response.data:
            nueva_asistencia = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'CREATE',
                'tabla': 'Asistencias',
                'id_registro': nueva_asistencia['id'],
                'datos_nuevos': nueva_asistencia
            })
            
            return nueva_asistencia['id']
        
        raise ValueError('Error al crear asistencia')
    except Exception as error:
        logger.error(f'Error en obtener_ultima_id_y_registrar_asistencias: {str(error)}')
        raise error

def editar_asistencias(datos):
    """Editar asistencia - convertido de editarAsistencias()"""
    try:
        # Obtener datos anteriores
        datos_anteriores = buscar_asistencias_por_id(datos['id'])
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {datos["id"]}')
        
        # Preparar datos actualizados
        datos['fecha'] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        response = supabase.table('Asistencias').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            asistencia_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'UPDATE',
                'tabla': 'Asistencias',
                'id_registro': datos['id'],
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': asistencia_actualizada
            })
            
            return asistencia_actualizada
        
        raise ValueError('Error al actualizar asistencia')
    except Exception as error:
        logger.error(f'Error en editar_asistencias: {str(error)}')
        raise error

def eliminar_asistencias(id):
    """Eliminar asistencia - convertido de eliminarAsistencias()"""
    try:
        # Obtener datos antes de eliminar
        datos_anteriores = buscar_asistencias_por_id(id)
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {id}')
        
        # Eliminar de Supabase
        response = supabase.table('Asistencias').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_historial({
                'operacion': 'DELETE',
                'tabla': 'Asistencias',
                'id_registro': id,
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': None
            })
            
            return True
        
        raise ValueError('Error al eliminar asistencia')
    except Exception as error:
        logger.error(f'Error al eliminar: {str(error)}')
        raise error

def buscar_jovenes_por_id(id=None):
    """Buscar jóvenes por ID - convertido de buscarJovenesPorId()"""
    try:
        if id:
            # Buscar joven específico
            response = supabase.table('Jovenes').select('*').eq('id', id).execute()
            return response.data[0] if response.data else None
        else:
            # Obtener todos los jóvenes
            response = supabase.table('Jovenes').select('*').execute()
            return response.data
    except Exception as error:
        logger.error(f'Error en buscar_jovenes_por_id: {str(error)}')
        raise error

def obtener_ultima_id_y_registrar_jovenes(datos):
    """Registrar nuevo joven - convertido de obtenerUltimaIdYRegistrarJovenes()"""
    try:
        # Preparar datos
        datos['fecha'] = datetime.now().isoformat()
        
        # Insertar en Supabase
        response = supabase.table('Jovenes').insert(datos).execute()
        
        if response.data:
            nuevo_joven = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'CREATE',
                'tabla': 'Jovenes',
                'id_registro': nuevo_joven['id'],
                'datos_nuevos': nuevo_joven
            })
            
            return nuevo_joven['id']
        
        raise ValueError('Error al crear joven')
    except Exception as error:
        logger.error(f'Error en obtener_ultima_id_y_registrar_jovenes: {str(error)}')
        raise error

def editar_jovenes(datos):
    """Editar joven - convertido de editarJovenes()"""
    try:
        # Obtener datos anteriores
        datos_anteriores = buscar_jovenes_por_id(datos['id'])
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {datos["id"]}')
        
        # Preparar datos actualizados
        datos['fecha'] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        response = supabase.table('Jovenes').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            joven_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'UPDATE',
                'tabla': 'Jovenes',
                'id_registro': datos['id'],
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': joven_actualizado
            })
            
            return joven_actualizado
        
        raise ValueError('Error al actualizar joven')
    except Exception as error:
        logger.error(f'Error en editar_jovenes: {str(error)}')
        raise error

def eliminar_jovenes(id):
    """Eliminar joven - convertido de eliminarJovenes()"""
    try:
        # Obtener datos antes de eliminar
        datos_anteriores = buscar_jovenes_por_id(id)
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {id}')
        
        # Eliminar de Supabase
        response = supabase.table('Jovenes').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_historial({
                'operacion': 'DELETE',
                'tabla': 'Jovenes',
                'id_registro': id,
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': None
            })
            
            return True
        
        raise ValueError('Error al eliminar joven')
    except Exception as error:
        logger.error(f'Error al eliminar: {str(error)}')
        raise error

def buscar_finanzas_por_id(id=None):
    """Buscar finanzas por ID - convertido de buscarFinanzasPorId()"""
    try:
        if id:
            # Buscar registro financiero específico
            response = supabase.table('Finanzas').select('*').eq('id', id).execute()
            return response.data[0] if response.data else None
        else:
            # Obtener todos los registros financieros
            response = supabase.table('Finanzas').select('*').execute()
            return response.data
    except Exception as error:
        logger.error(f'Error en buscar_finanzas_por_id: {str(error)}')
        raise error

def obtener_ultima_id_y_registrar_finanzas(datos):
    """Registrar nuevo registro financiero - convertido de obtenerUltimaIdYRegistrarFinanzas()"""
    try:
        # Preparar datos
        datos['fecha_de_registro'] = datetime.now().isoformat()
        
        # Insertar en Supabase
        response = supabase.table('Finanzas').insert(datos).execute()
        
        if response.data:
            nuevo_registro = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'CREATE',
                'tabla': 'Finanzas',
                'id_registro': nuevo_registro['id'],
                'datos_nuevos': nuevo_registro
            })
            
            return nuevo_registro['id']
        
        raise ValueError('Error al crear registro financiero')
    except Exception as error:
        logger.error(f'Error en obtener_ultima_id_y_registrar_finanzas: {str(error)}')
        raise error

def editar_finanzas(datos):
    """Editar registro financiero - convertido de editarFinanzas()"""
    try:
        # Obtener datos anteriores
        datos_anteriores = buscar_finanzas_por_id(datos['id'])
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {datos["id"]}')
        
        # Preparar datos actualizados
        datos['fecha_de_registro'] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        response = supabase.table('Finanzas').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            registro_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_historial({
                'operacion': 'UPDATE',
                'tabla': 'Finanzas',
                'id_registro': datos['id'],
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': registro_actualizado
            })
            
            return registro_actualizado
        
        raise ValueError('Error al actualizar registro financiero')
    except Exception as error:
        logger.error(f'Error en editar_finanzas: {str(error)}')
        raise error

def eliminar_finanzas(id):
    """Eliminar registro financiero - convertido de eliminarFinanzas()"""
    try:
        # Obtener datos antes de eliminar
        datos_anteriores = buscar_finanzas_por_id(id)
        if not datos_anteriores:
            raise ValueError(f'No se encontró el registro con ID: {id}')
        
        # Eliminar de Supabase
        response = supabase.table('Finanzas').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_historial({
                'operacion': 'DELETE',
                'tabla': 'Finanzas',
                'id_registro': id,
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': None
            })
            
            return True
        
        raise ValueError('Error al eliminar registro financiero')
    except Exception as error:
        logger.error(f'Error al eliminar: {str(error)}')
        raise error
