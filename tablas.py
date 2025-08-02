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
        logger.error(f"Error en registrar_cambio_historial: {e}")
        return None

# ===== FUNCIONES PARA PREDICADORES =====

def buscar_predicadores_por_id(id=None):
    """Buscar predicadores por ID o todos"""
    try:
        if id:
            response = supabase.table('predicadores').select('*').eq('id_predicador', id).execute()
        else:
            response = supabase.table('predicadores').select('*').execute()
        
        return response.data
    except Exception as e:
        logger.error(f"Error en buscar_predicadores_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_predicadores(datos):
    """Obtener última ID y registrar predicador"""
    try:
        # Preparar datos según nueva estructura
        datos_predicador = {
            'nombre': datos.get('nombre'),
            'apellido': datos.get('apellido'),
            'telefono': datos.get('telefono'),
            'fecha_registro': datetime.now().isoformat()
        }
        
        # Insertar predicador
        response = supabase.table('predicadores').insert(datos_predicador).execute()
        
        if response.data:
            predicador = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'predicadores',
                predicador['id_predicador'],
                'INSERT',
                None,
                predicador
            )
            
            return predicador
        else:
            raise ValueError('Error al registrar predicador')
            
    except Exception as e:
        logger.error(f"Error en obtener_ultima_id_y_registrar_predicadores: {e}")
        raise e

def editar_predicadores(datos):
    """Editar predicador"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('predicadores').select('*').eq('id_predicador', datos['id_predicador']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Preparar datos actualizados
        datos_actualizados = {
            'nombre': datos.get('nombre'),
            'apellido': datos.get('apellido'),
            'telefono': datos.get('telefono')
        }
        
        response = supabase.table('predicadores').update(datos_actualizados).eq('id_predicador', datos['id_predicador']).execute()
        
        if response.data:
            predicador_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'predicadores',
                predicador_actualizado['id_predicador'],
                'UPDATE',
                datos_anteriores,
                predicador_actualizado
            )
            
            return predicador_actualizado
        else:
            raise ValueError('Error al actualizar predicador')
            
    except Exception as e:
        logger.error(f"Error en editar_predicadores: {e}")
        raise e

def eliminar_predicadores(id):
    """Eliminar predicador (soft delete)"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('predicadores').select('*').eq('id_predicador', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar predicador
        response = supabase.table('predicadores').delete().eq('id_predicador', id).execute()
        
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
        logger.error(f"Error en eliminar_predicadores: {e}")
        raise e

# ===== FUNCIONES PARA REUNIONES =====

def buscar_reuniones_por_id(id=None):
    """Buscar reuniones por ID o todas"""
    try:
        if id:
            response = supabase.table('reuniones').select('*').eq('id_reunion', id).execute()
        else:
            response = supabase.table('reuniones').select('*').execute()
        
        return response.data
    except Exception as e:
        logger.error(f"Error en buscar_reuniones_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_reuniones(datos):
    """Obtener última ID y registrar reunión"""
    try:
        # Preparar datos según nueva estructura
        datos_reunion = {
            'director': datos.get('director'),
            'lectura': datos.get('lectura'),
            'cantos': datos.get('cantos'),
            'ofrenda': datos.get('ofrenda'),
            'predicador': datos.get('predicador'),
            'fecha_reunion': datos.get('fecha_reunion'),
            'fecha_registro': datetime.now().isoformat()
        }
        
        # Insertar reunión
        response = supabase.table('reuniones').insert(datos_reunion).execute()
        
        if response.data:
            reunion = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'reuniones',
                reunion['id_reunion'],
                'INSERT',
                None,
                reunion
            )
            
            return reunion['id_reunion']
        else:
            raise ValueError('Error al registrar reunión')
            
    except Exception as e:
        logger.error(f"Error en obtener_ultima_id_y_registrar_reuniones: {e}")
        raise e

def editar_reuniones(datos):
    """Editar reunión"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('reuniones').select('*').eq('id_reunion', datos['id_reunion']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Preparar datos actualizados
        datos_actualizados = {
            'director': datos.get('director'),
            'lectura': datos.get('lectura'),
            'cantos': datos.get('cantos'),
            'ofrenda': datos.get('ofrenda'),
            'predicador': datos.get('predicador'),
            'fecha_reunion': datos.get('fecha_reunion')
        }
        
        response = supabase.table('reuniones').update(datos_actualizados).eq('id_reunion', datos['id_reunion']).execute()
        
        if response.data:
            reunion_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'reuniones',
                reunion_actualizada['id_reunion'],
                'UPDATE',
                datos_anteriores,
                reunion_actualizada
            )
            
            return reunion_actualizada
        else:
            raise ValueError('Error al actualizar reunión')
            
    except Exception as e:
        logger.error(f"Error en editar_reuniones: {e}")
        raise e

def eliminar_reuniones(id):
    """Eliminar reunión"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('reuniones').select('*').eq('id_reunion', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar reunión
        response = supabase.table('reuniones').delete().eq('id_reunion', id).execute()
        
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
        logger.error(f"Error en eliminar_reuniones: {e}")
        raise e

# ===== FUNCIONES PARA CALENDARIO =====

def buscar_calendario_por_id(id=None):
    """Buscar calendario por ID o todo"""
    try:
        if id:
            response = supabase.table('calendario').select('*').eq('id_evento', id).execute()
        else:
            response = supabase.table('calendario').select('*').execute()
        
        return response.data
    except Exception as e:
        logger.error(f"Error en buscar_calendario_por_id: {e}")
        raise e

def obtener_ultima_id_y_registrar_calendario(datos):
    """Obtener última ID y registrar evento de calendario"""
    try:
        # Preparar datos según nueva estructura
        datos_evento = {
            'nombre_evento': datos.get('nombre_evento'),
            'objetivo_evento': datos.get('objetivo_evento'),
            'fecha_evento': datos.get('fecha_evento'),
            'observaciones': datos.get('observaciones'),
            'fecha_registro': datetime.now().isoformat()
        }
        
        # Insertar evento
        response = supabase.table('calendario').insert(datos_evento).execute()
        
        if response.data:
            evento = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'calendario',
                evento['id_evento'],
                'INSERT',
                None,
                evento
            )
            
            return evento['id_evento']
        else:
            raise ValueError('Error al registrar evento de calendario')
            
    except Exception as e:
        logger.error(f"Error en obtener_ultima_id_y_registrar_calendario: {e}")
        raise e

def editar_calendario(datos):
    """Editar evento de calendario"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('calendario').select('*').eq('id_evento', datos['id_evento']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Preparar datos actualizados
        datos_actualizados = {
            'nombre_evento': datos.get('nombre_evento'),
            'objetivo_evento': datos.get('objetivo_evento'),
            'fecha_evento': datos.get('fecha_evento'),
            'observaciones': datos.get('observaciones')
        }
        
        response = supabase.table('calendario').update(datos_actualizados).eq('id_evento', datos['id_evento']).execute()
        
        if response.data:
            evento_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'calendario',
                evento_actualizado['id_evento'],
                'UPDATE',
                datos_anteriores,
                evento_actualizado
            )
            
            return evento_actualizado
        else:
            raise ValueError('Error al actualizar evento de calendario')
            
    except Exception as e:
        logger.error(f"Error en editar_calendario: {e}")
        raise e

def eliminar_calendario(id):
    """Eliminar evento de calendario"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('calendario').select('*').eq('id_evento', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar evento
        response = supabase.table('calendario').delete().eq('id_evento', id).execute()
        
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
        logger.error(f"Error en eliminar_calendario: {e}")
        raise e

# ===== FUNCIONES PARA BANDEJA =====

def buscar_bandeja_por_id(id=None):
    """Buscar bandeja por ID o todas"""
    try:
        if id:
            response = supabase.table('bandeja').select('*').eq('id_bandeja', id).execute()
        else:
            response = supabase.table('bandeja').select('*').execute()
        
        return response.data
    except Exception as e:
        logger.error(f"Error en buscar_bandeja_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_bandeja(datos):
    """Obtener última ID y registrar tarea en bandeja"""
    try:
        # Preparar datos según nueva estructura
        datos_bandeja = {
            'objetivo': datos.get('objetivo'),
            'descripcion': datos.get('descripcion')
        }
        
        # Insertar tarea
        response = supabase.table('bandeja').insert(datos_bandeja).execute()
        
        if response.data:
            tarea = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'bandeja',
                tarea['id_bandeja'],
                'INSERT',
                None,
                tarea
            )
            
            return tarea['id_bandeja']
        else:
            raise ValueError('Error al registrar tarea en bandeja')
            
    except Exception as e:
        logger.error(f"Error en obtener_ultima_id_y_registrar_bandeja: {e}")
        raise e

def editar_bandeja(datos):
    """Editar tarea en bandeja"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('bandeja').select('*').eq('id_bandeja', datos['id_bandeja']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Preparar datos actualizados
        datos_actualizados = {
            'objetivo': datos.get('objetivo'),
            'descripcion': datos.get('descripcion')
        }
        
        response = supabase.table('bandeja').update(datos_actualizados).eq('id_bandeja', datos['id_bandeja']).execute()
        
        if response.data:
            tarea_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'bandeja',
                tarea_actualizada['id_bandeja'],
                'UPDATE',
                datos_anteriores,
                tarea_actualizada
            )
            
            return tarea_actualizada
        else:
            raise ValueError('Error al actualizar tarea en bandeja')
            
    except Exception as e:
        logger.error(f"Error en editar_bandeja: {e}")
        raise e

def eliminar_bandeja(id):
    """Eliminar tarea de bandeja"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('bandeja').select('*').eq('id_bandeja', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar tarea
        response = supabase.table('bandeja').delete().eq('id_bandeja', id).execute()
        
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
        logger.error(f"Error en eliminar_bandeja: {e}")
        raise e

# ===== FUNCIONES PARA ASISTENCIA =====

def buscar_asistencia_por_id(id=None):
    """Buscar asistencia por ID o todas"""
    try:
        if id:
            response = supabase.table('asistencia').select('*').eq('id_asistencia', id).execute()
        else:
            response = supabase.table('asistencia').select('*').execute()
        
        return response.data
    except Exception as e:
        logger.error(f"Error en buscar_asistencia_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_asistencia(datos):
    """Obtener última ID y registrar asistencia"""
    try:
        # Preparar datos según nueva estructura
        datos_asistencia = {
            'id_joven': datos.get('id_joven'),
            'nombre_joven': datos.get('nombre_joven'),
            'fecha_reunion': datos.get('fecha_reunion'),
            'asistio': datos.get('asistio', False)
        }
        
        # Insertar asistencia
        response = supabase.table('asistencia').insert(datos_asistencia).execute()
        
        if response.data:
            asistencia = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'asistencia',
                asistencia['id_asistencia'],
                'INSERT',
                None,
                asistencia
            )
            
            return asistencia['id_asistencia']
        else:
            raise ValueError('Error al registrar asistencia')
            
    except Exception as e:
        logger.error(f"Error en obtener_ultima_id_y_registrar_asistencia: {e}")
        raise e

def editar_asistencia(datos):
    """Editar asistencia"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('asistencia').select('*').eq('id_asistencia', datos['id_asistencia']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Preparar datos actualizados
        datos_actualizados = {
            'id_joven': datos.get('id_joven'),
            'nombre_joven': datos.get('nombre_joven'),
            'fecha_reunion': datos.get('fecha_reunion'),
            'asistio': datos.get('asistio', False)
        }
        
        response = supabase.table('asistencia').update(datos_actualizados).eq('id_asistencia', datos['id_asistencia']).execute()
        
        if response.data:
            asistencia_actualizada = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'asistencia',
                asistencia_actualizada['id_asistencia'],
                'UPDATE',
                datos_anteriores,
                asistencia_actualizada
            )
            
            return asistencia_actualizada
        else:
            raise ValueError('Error al actualizar asistencia')
            
    except Exception as e:
        logger.error(f"Error en editar_asistencia: {e}")
        raise e

def eliminar_asistencia(id):
    """Eliminar asistencia"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('asistencia').select('*').eq('id_asistencia', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar asistencia
        response = supabase.table('asistencia').delete().eq('id_asistencia', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'asistencia',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar asistencia')
            
    except Exception as e:
        logger.error(f"Error en eliminar_asistencia: {e}")
        raise e

# ===== FUNCIONES PARA JÓVENES =====

def buscar_jovenes_por_id(id=None):
    """Buscar jóvenes por ID o todos"""
    try:
        if id:
            response = supabase.table('jovenes').select('*').eq('id_joven', id).execute()
        else:
            response = supabase.table('jovenes').select('*').execute()
        
        return response.data
    except Exception as e:
        logger.error(f"Error en buscar_jovenes_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_jovenes(datos):
    """Obtener última ID y registrar joven"""
    try:
        # Preparar datos según nueva estructura
        datos_joven = {
            'nombre': datos.get('nombre'),
            'apellido': datos.get('apellido'),
            'telefono': datos.get('telefono'),
            'fecha_registro': datetime.now().isoformat()
        }
        
        # Insertar joven
        response = supabase.table('jovenes').insert(datos_joven).execute()
        
        if response.data:
            joven = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'jovenes',
                joven['id_joven'],
                'INSERT',
                None,
                joven
            )
            
            return joven['id_joven']
        else:
            raise ValueError('Error al registrar joven')
            
    except Exception as e:
        logger.error(f"Error en obtener_ultima_id_y_registrar_jovenes: {e}")
        raise e

def editar_jovenes(datos):
    """Editar joven"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('jovenes').select('*').eq('id_joven', datos['id_joven']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Preparar datos actualizados
        datos_actualizados = {
            'nombre': datos.get('nombre'),
            'apellido': datos.get('apellido'),
            'telefono': datos.get('telefono')
        }
        
        response = supabase.table('jovenes').update(datos_actualizados).eq('id_joven', datos['id_joven']).execute()
        
        if response.data:
            joven_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'jovenes',
                joven_actualizado['id_joven'],
                'UPDATE',
                datos_anteriores,
                joven_actualizado
            )
            
            return joven_actualizado
        else:
            raise ValueError('Error al actualizar joven')
            
    except Exception as e:
        logger.error(f"Error en editar_jovenes: {e}")
        raise e

def eliminar_jovenes(id):
    """Eliminar joven"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('jovenes').select('*').eq('id_joven', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar joven
        response = supabase.table('jovenes').delete().eq('id_joven', id).execute()
        
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
        logger.error(f"Error en eliminar_jovenes: {e}")
        raise e

# ===== FUNCIONES PARA MOVIMIENTOS FINANCIEROS =====

def buscar_movimientos_financieros_por_id(id=None):
    """Buscar movimientos financieros por ID o todos"""
    try:
        if id:
            response = supabase.table('movimientos_financieros').select('*').eq('id_movimiento', id).execute()
        else:
            response = supabase.table('movimientos_financieros').select('*').execute()
        
        return response.data
    except Exception as e:
        logger.error(f"Error en buscar_movimientos_financieros_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_movimientos_financieros(datos):
    """Obtener última ID y registrar movimiento financiero"""
    try:
        # Preparar datos según nueva estructura
        datos_movimiento = {
            'tipo_movimiento': datos.get('tipo_movimiento'),
            'concepto': datos.get('concepto'),
            'monto': datos.get('monto'),
            'id_entidad': datos.get('id_entidad'),
            'id_producto': datos.get('id_producto'),
            'registrado_por': datos.get('registrado_por'),
            'fecha_registro': datetime.now().isoformat()
        }
        
        # Insertar movimiento
        response = supabase.table('movimientos_financieros').insert(datos_movimiento).execute()
        
        if response.data:
            movimiento = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'movimientos_financieros',
                movimiento['id_movimiento'],
                'INSERT',
                None,
                movimiento
            )
            
            return movimiento['id_movimiento']
        else:
            raise ValueError('Error al registrar movimiento financiero')
            
    except Exception as e:
        logger.error(f"Error en obtener_ultima_id_y_registrar_movimientos_financieros: {e}")
        raise e

def editar_movimientos_financieros(datos):
    """Editar movimiento financiero"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('movimientos_financieros').select('*').eq('id_movimiento', datos['id_movimiento']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Preparar datos actualizados
        datos_actualizados = {
            'tipo_movimiento': datos.get('tipo_movimiento'),
            'concepto': datos.get('concepto'),
            'monto': datos.get('monto'),
            'id_entidad': datos.get('id_entidad'),
            'id_producto': datos.get('id_producto'),
            'registrado_por': datos.get('registrado_por')
        }
        
        response = supabase.table('movimientos_financieros').update(datos_actualizados).eq('id_movimiento', datos['id_movimiento']).execute()
        
        if response.data:
            movimiento_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'movimientos_financieros',
                movimiento_actualizado['id_movimiento'],
                'UPDATE',
                datos_anteriores,
                movimiento_actualizado
            )
            
            return movimiento_actualizado
        else:
            raise ValueError('Error al actualizar movimiento financiero')
            
    except Exception as e:
        logger.error(f"Error en editar_movimientos_financieros: {e}")
        raise e

def eliminar_movimientos_financieros(id):
    """Eliminar movimiento financiero"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('movimientos_financieros').select('*').eq('id_movimiento', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar movimiento
        response = supabase.table('movimientos_financieros').delete().eq('id_movimiento', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'movimientos_financieros',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar movimiento financiero')
            
    except Exception as e:
        logger.error(f"Error en eliminar_movimientos_financieros: {e}")
        raise e

# ===== FUNCIONES PARA ADMINISTRADORES =====

def buscar_administradores_por_id(id=None):
    """Buscar administradores por ID o todos"""
    try:
        if id:
            response = supabase.table('administradores').select('*').eq('id_admin', id).execute()
        else:
            response = supabase.table('administradores').select('*').execute()
        
        return response.data
    except Exception as e:
        logger.error(f"Error en buscar_administradores_por_id: {e}")
        return []

def obtener_ultima_id_y_registrar_administradores(datos):
    """Obtener última ID y registrar administrador"""
    try:
        # Preparar datos según nueva estructura
        datos_admin = {
            'nombre_admin': datos.get('nombre_admin'),
            'rol_admin': datos.get('rol_admin'),
            'codigo_acceso': datos.get('codigo_acceso'),
            'fecha_registro': datetime.now().isoformat()
        }
        
        # Insertar administrador
        response = supabase.table('administradores').insert(datos_admin).execute()
        
        if response.data:
            admin = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'administradores',
                admin['id_admin'],
                'INSERT',
                None,
                admin
            )
            
            return admin['id_admin']
        else:
            raise ValueError('Error al registrar administrador')
            
    except Exception as e:
        logger.error(f"Error en obtener_ultima_id_y_registrar_administradores: {e}")
        raise e

def editar_administradores(datos):
    """Editar administrador"""
    try:
        # Obtener datos anteriores para historial
        response_anterior = supabase.table('administradores').select('*').eq('id_admin', datos['id_admin']).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Preparar datos actualizados
        datos_actualizados = {
            'nombre_admin': datos.get('nombre_admin'),
            'rol_admin': datos.get('rol_admin'),
            'codigo_acceso': datos.get('codigo_acceso')
        }
        
        response = supabase.table('administradores').update(datos_actualizados).eq('id_admin', datos['id_admin']).execute()
        
        if response.data:
            admin_actualizado = response.data[0]
            
            # Registrar en historial
            registrar_cambio_historial(
                'administradores',
                admin_actualizado['id_admin'],
                'UPDATE',
                datos_anteriores,
                admin_actualizado
            )
            
            return admin_actualizado
        else:
            raise ValueError('Error al actualizar administrador')
            
    except Exception as e:
        logger.error(f"Error en editar_administradores: {e}")
        raise e

def eliminar_administradores(id):
    """Eliminar administrador"""
    try:
        # Obtener datos para historial
        response_anterior = supabase.table('administradores').select('*').eq('id_admin', id).execute()
        datos_anteriores = response_anterior.data[0] if response_anterior.data else None
        
        # Eliminar administrador
        response = supabase.table('administradores').delete().eq('id_admin', id).execute()
        
        if response.data:
            # Registrar en historial
            registrar_cambio_historial(
                'administradores',
                id,
                'DELETE',
                datos_anteriores,
                None
            )
            
            return True
        else:
            raise ValueError('Error al eliminar administrador')
            
    except Exception as e:
        logger.error(f"Error en eliminar_administradores: {e}")
        raise e
