from flask import session, request, jsonify
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

def buscar_bandeja_por_id(id=None):
    """Buscar tarea en bandeja por ID o todas - convertido de buscarBandejaPorId()"""
    try:
        if id:
            response = supabase.table('bandeja').select('*').eq('id', id).execute()
        else:
            response = supabase.table('bandeja').select('*').execute()
        
        return response.data
    except Exception as e:
        print(f"Error en buscar_bandeja_por_id: {e}")
        raise e

def obtener_ultima_id_y_registrar_bandeja(datos):
    """Obtener última ID y registrar tarea en bandeja - convertido de obtenerUltimaIdYRegistrarBandeja()"""
    try:
        # Agregar metadatos
        datos['fecha_creacion'] = datetime.now().isoformat()
        datos['usuario'] = session.get('user_email', 'sistema')
        datos['estado'] = 'pendiente'
        
        # Insertar tarea
        response = supabase.table('bandeja').insert(datos).execute()
        
        if response.data:
            tarea = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'bandeja',
                tarea['id'],
                'INSERT',
                None,
                tarea
            )
            
            return tarea
        else:
            raise ValueError('Error al registrar tarea en bandeja')
            
    except Exception as e:
        print(f"Error en obtener_ultima_id_y_registrar_bandeja: {e}")
        raise e

def procesar_tareas_pendientes():
    """Procesar tareas pendientes en bandeja - convertido de procesarTareasPendientes()"""
    try:
        # Buscar tareas sin estado
        response = supabase.table('bandeja').select('*').is_('estado', 'null').execute()
        
        if response.data:
            for tarea in response.data:
                # Marcar como creado
                supabase.table('bandeja').update({'estado': 'creado'}).eq('id', tarea['id']).execute()
                
                # Registrar en historial
                registrar_cambio_historial(
                    'bandeja',
                    tarea['id'],
                    'PROCESS',
                    tarea,
                    {'estado': 'creado'}
                )
            
            return len(response.data)
        return 0
        
    except Exception as e:
        print(f"Error en procesar_tareas_pendientes: {e}")
        raise e

def editar_bandeja(datos):
    """Editar tarea en bandeja - convertido de editarBandeja()"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('bandeja').select('*').eq('id', datos['id']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Actualizar datos
        datos['usuario'] = session.get('user_email', 'sistema')
        datos['fecha_actualizacion'] = datetime.now().isoformat()
        
        response = supabase.table('bandeja').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            tarea_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'bandeja',
                tarea_actualizada['id'],
                'UPDATE',
                datos_anteriores,
                tarea_actualizada
            )
            
            return tarea_actualizada
        else:
            raise ValueError('Error al actualizar tarea en bandeja')
            
    except Exception as e:
        print(f"Error en editar_bandeja: {e}")
        raise e

def eliminar_bandeja(id):
    """Eliminar tarea de bandeja - convertido de eliminarBandeja()"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('bandeja').select('*').eq('id', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar tarea
        response = supabase.table('bandeja').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'bandeja',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar tarea de bandeja')
            
    except Exception as e:
        print(f"Error en eliminar_bandeja: {e}")
        raise e

def buscar_asistencias_por_id(id=None):
    """Buscar asistencia por ID o todas - convertido de buscarAsistenciasPorId()"""
    try:
        if id:
            response = supabase.table('asistencias').select('*').eq('id', id).execute()
        else:
            response = supabase.table('asistencias').select('*').execute()
        
        return response.data
    except Exception as e:
        print(f"Error en buscar_asistencias_por_id: {e}")
        raise e

def obtener_ultima_id_y_registrar_asistencias(datos):
    """Obtener última ID y registrar asistencia - convertido de obtenerUltimaIdYRegistrarAsistencias()"""
    try:
        # Agregar metadatos
        datos['fecha_registro'] = datetime.now().isoformat()
        datos['usuario'] = session.get('user_email', 'sistema')
        
        # Insertar asistencia
        response = supabase.table('asistencias').insert(datos).execute()
        
        if response.data:
            asistencia = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'asistencias',
                asistencia['id'],
                'INSERT',
                None,
                asistencia
            )
            
            return asistencia
        else:
            raise ValueError('Error al registrar asistencia')
            
    except Exception as e:
        print(f"Error en obtener_ultima_id_y_registrar_asistencias: {e}")
        raise e

def editar_asistencias(datos):
    """Editar asistencia - convertido de editarAsistencias()"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('asistencias').select('*').eq('id', datos['id']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Actualizar datos
        datos['usuario'] = session.get('user_email', 'sistema')
        datos['fecha_actualizacion'] = datetime.now().isoformat()
        
        response = supabase.table('asistencias').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            asistencia_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'asistencias',
                asistencia_actualizada['id'],
                'UPDATE',
                datos_anteriores,
                asistencia_actualizada
            )
            
            return asistencia_actualizada
        else:
            raise ValueError('Error al actualizar asistencia')
            
    except Exception as e:
        print(f"Error en editar_asistencias: {e}")
        raise e

def eliminar_asistencias(id):
    """Eliminar asistencia - convertido de eliminarAsistencias()"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('asistencias').select('*').eq('id', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar asistencia
        response = supabase.table('asistencias').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'asistencias',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar asistencia')
            
    except Exception as e:
        print(f"Error en eliminar_asistencias: {e}")
        raise e

def buscar_jovenes_por_id(id=None):
    """Buscar joven por ID o todos - convertido de buscarJovenesPorId()"""
    try:
        if id:
            response = supabase.table('jovenes').select('*').eq('id', id).execute()
        else:
            response = supabase.table('jovenes').select('*').execute()
        
        return response.data
    except Exception as e:
        print(f"Error en buscar_jovenes_por_id: {e}")
        raise e

def obtener_ultima_id_y_registrar_jovenes(datos):
    """Obtener última ID y registrar joven - convertido de obtenerUltimaIdYRegistrarJovenes()"""
    try:
        # Agregar metadatos
        datos['fecha_registro'] = datetime.now().isoformat()
        datos['usuario'] = session.get('user_email', 'sistema')
        
        # Insertar joven
        response = supabase.table('jovenes').insert(datos).execute()
        
        if response.data:
            joven = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'jovenes',
                joven['id'],
                'INSERT',
                None,
                joven
            )
            
            return joven
        else:
            raise ValueError('Error al registrar joven')
            
    except Exception as e:
        print(f"Error en obtener_ultima_id_y_registrar_jovenes: {e}")
        raise e

def editar_jovenes(datos):
    """Editar joven - convertido de editarJovenes()"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('jovenes').select('*').eq('id', datos['id']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Actualizar datos
        datos['usuario'] = session.get('user_email', 'sistema')
        datos['fecha_actualizacion'] = datetime.now().isoformat()
        
        response = supabase.table('jovenes').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            joven_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'jovenes',
                joven_actualizado['id'],
                'UPDATE',
                datos_anteriores,
                joven_actualizado
            )
            
            return joven_actualizado
        else:
            raise ValueError('Error al actualizar joven')
            
    except Exception as e:
        print(f"Error en editar_jovenes: {e}")
        raise e

def eliminar_jovenes(id):
    """Eliminar joven - convertido de eliminarJovenes()"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('jovenes').select('*').eq('id', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar joven
        response = supabase.table('jovenes').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'jovenes',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar joven')
            
    except Exception as e:
        print(f"Error en eliminar_jovenes: {e}")
        raise e

def buscar_finanzas_por_id(id=None):
    """Buscar finanza por ID o todas - convertido de buscarFinanzasPorId()"""
    try:
        if id:
            response = supabase.table('finanzas').select('*').eq('id', id).execute()
        else:
            response = supabase.table('finanzas').select('*').execute()
        
        return response.data
    except Exception as e:
        print(f"Error en buscar_finanzas_por_id: {e}")
        raise e

def obtener_ultima_id_y_registrar_finanzas(datos):
    """Obtener última ID y registrar finanza - convertido de obtenerUltimaIdYRegistrarFinanzas()"""
    try:
        # Agregar metadatos
        datos['fecha_registro'] = datetime.now().isoformat()
        datos['usuario'] = session.get('user_email', 'sistema')
        
        # Insertar finanza
        response = supabase.table('finanzas').insert(datos).execute()
        
        if response.data:
            finanza = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'finanzas',
                finanza['id'],
                'INSERT',
                None,
                finanza
            )
            
            return finanza
        else:
            raise ValueError('Error al registrar finanza')
            
    except Exception as e:
        print(f"Error en obtener_ultima_id_y_registrar_finanzas: {e}")
        raise e

def editar_finanzas(datos):
    """Editar finanza - convertido de editarFinanzas()"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('finanzas').select('*').eq('id', datos['id']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Actualizar datos
        datos['usuario'] = session.get('user_email', 'sistema')
        datos['fecha_actualizacion'] = datetime.now().isoformat()
        
        response = supabase.table('finanzas').update(datos).eq('id', datos['id']).execute()
        
        if response.data:
            finanza_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'finanzas',
                finanza_actualizada['id'],
                'UPDATE',
                datos_anteriores,
                finanza_actualizada
            )
            
            return finanza_actualizada
        else:
            raise ValueError('Error al actualizar finanza')
            
    except Exception as e:
        print(f"Error en editar_finanzas: {e}")
        raise e

def eliminar_finanzas(id):
    """Eliminar finanza - convertido de eliminarFinanzas()"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('finanzas').select('*').eq('id', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar finanza
        response = supabase.table('finanzas').delete().eq('id', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'finanzas',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar finanza')
            
    except Exception as e:
        print(f"Error en eliminar_finanzas: {e}")
        raise e
