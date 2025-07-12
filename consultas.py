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

def ver_historial(tabla='', estado='', usuario=''):
    """Ver historial con filtros - convertido de verHistorial()"""
    try:
        # Construir consulta base
        query = supabase.table('Historial_Cambios').select('*')
        
        # Aplicar filtros si existen
        if tabla:
            query = query.eq('tabla', tabla)
        if estado:
            query = query.eq('estado', estado)
        if usuario:
            query = query.eq('usuario', usuario)
        
        # Ejecutar consulta
        response = query.execute()
        
        # Procesar resultados
        registros = []
        for fila in response.data:
            try:
                fecha = datetime.fromisoformat(fila['fecha'].replace('Z', '+00:00'))
            except:
                fecha = datetime.now()
            
            registro = {
                'id': fila['id'],
                'fecha': fecha.isoformat(),
                'usuario': fila['usuario'],
                'estado': fila['estado'],
                'tabla': fila['tabla'],
                'id_registro': fila['id_registro'],
                'datos_anteriores': fila['datos_anteriores'],
                'datos_nuevos': fila['datos_nuevos']
            }
            
            # Agregar información de botones disponibles
            registro['botones'] = {
                'revertir': registro['estado'] == 'Editado',
                'restaurar': registro['estado'] == 'Eliminado'
            }
            
            registros.append(registro)
        
        return registros

    except Exception as error:
        logger.error(f'Error en ver_historial: {str(error)}')
        return []

def obtener_registro_historial(id_historial):
    """Obtener registro específico del historial - convertido de obtenerRegistroHistorial()"""
    try:
        response = supabase.table('Historial_Cambios').select('*').eq('id', id_historial).execute()
        
        if not response.data:
            logger.info(f'No se encontró el registro con ID: {id_historial}')
            return None
        
        registro = response.data[0]
        
        return {
            'id': registro['id'],
            'fecha': registro['fecha'],
            'usuario': registro['usuario'],
            'estado': registro['estado'],
            'tabla': registro['tabla'],
            'id_registro': registro['id_registro'],
            'datos_anteriores': registro['datos_anteriores'],
            'datos_nuevos': registro['datos_nuevos']
        }

    except Exception as error:
        logger.error(f'Error en obtener_registro_historial: {str(error)}')
        return None

def revertir_edicion(id_historial):
    """Revertir una edición - convertido de revertirEdicion()"""
    try:
        # Obtener registro del historial
        registro_historial = obtener_registro_historial(id_historial)
        
        if not registro_historial:
            return {
                'success': False,
                'mensaje': 'No se encontró el registro en el historial'
            }
        
        tabla = registro_historial['tabla']
        id_registro = registro_historial['id_registro']
        datos_anteriores = registro_historial['datos_anteriores']
        
        # Verificar que tenemos los datos necesarios
        if not tabla or not id_registro or not datos_anteriores:
            return {
                'success': False,
                'mensaje': 'Datos insuficientes para revertir la edición'
            }
        
        # Actualizar el registro en la tabla correspondiente
        datos_actualizados = datos_anteriores.copy()
        datos_actualizados['estado'] = 'Revertido'
        datos_actualizados['fecha'] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        response = supabase.table(tabla).update(datos_actualizados).eq('id', id_registro).execute()
        
        if response.data:
            # Crear nuevo registro en el historial
            nuevo_registro_historial = {
                'fecha': datetime.now().isoformat(),
                'usuario': registro_historial['usuario'],
                'estado': 'Revertido',
                'tabla': tabla,
                'id_registro': id_registro,
                'datos_anteriores': datos_anteriores,
                'datos_nuevos': datos_anteriores
            }
            
            supabase.table('Historial_Cambios').insert(nuevo_registro_historial).execute()
            
            return {
                'success': True,
                'mensaje': 'Edición revertida exitosamente',
                'datos': datos_anteriores
            }
        
        return {
            'success': False,
            'mensaje': 'Error al revertir la edición'
        }
        
    except Exception as error:
        logger.error(f'Error en revertir_edicion: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error al revertir: {str(error)}'
        }

def restaurar_registro(id_historial):
    """Restaurar un registro eliminado - convertido de restaurarRegistro()"""
    try:
        # Obtener registro del historial
        registro_historial = obtener_registro_historial(id_historial)
        
        if not registro_historial:
            return {
                'success': False,
                'mensaje': 'No se encontró el registro en el historial'
            }
        
        tabla = registro_historial['tabla']
        id_registro = registro_historial['id_registro']
        estado = registro_historial['estado']
        
        # Determinar qué datos usar basado en el estado
        if estado == 'Eliminado':
            datos_para_restaurar = registro_historial['datos_anteriores']
        else:
            datos_para_restaurar = registro_historial['datos_nuevos']
        
        if not datos_para_restaurar:
            return {
                'success': False,
                'mensaje': 'No hay datos para restaurar'
            }
        
        # Preparar datos para restaurar
        datos_actualizados = datos_para_restaurar.copy()
        datos_actualizados['estado'] = 'Restaurado'
        datos_actualizados['fecha'] = datetime.now().isoformat()
        
        # Actualizar en Supabase
        response = supabase.table(tabla).update(datos_actualizados).eq('id', id_registro).execute()
        
        if response.data:
            # Crear nuevo registro en el historial
            nuevo_registro_historial = {
                'fecha': datetime.now().isoformat(),
                'usuario': registro_historial['usuario'],
                'estado': 'Restaurado',
                'tabla': tabla,
                'id_registro': id_registro,
                'datos_anteriores': datos_para_restaurar,
                'datos_nuevos': datos_para_restaurar
            }
            
            supabase.table('Historial_Cambios').insert(nuevo_registro_historial).execute()
            
            return {
                'success': True,
                'mensaje': 'Registro restaurado exitosamente',
                'datos': datos_para_restaurar
            }
        
        return {
            'success': False,
            'mensaje': 'Error al restaurar el registro'
        }
        
    except Exception as error:
        logger.error(f'Error en restaurar_registro: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error al restaurar: {str(error)}'
        }

def consulta_personalizada(tabla, filtros=None, ordenamiento=None, limite=None):
    """Ejecutar consulta personalizada con WHERE, ORDER BY, etc."""
    try:
        # Construir consulta base
        query = supabase.table(tabla).select('*')
        
        # Aplicar filtros WHERE
        if filtros:
            for campo, valor in filtros.items():
                if isinstance(valor, dict):
                    # Operadores especiales: {'gt': 10}, {'like': '%texto%'}
                    for operador, valor_op in valor.items():
                        if operador == 'gt':
                            query = query.gt(campo, valor_op)
                        elif operador == 'lt':
                            query = query.lt(campo, valor_op)
                        elif operador == 'gte':
                            query = query.gte(campo, valor_op)
                        elif operador == 'lte':
                            query = query.lte(campo, valor_op)
                        elif operador == 'neq':
                            query = query.neq(campo, valor_op)
                        elif operador == 'like':
                            query = query.ilike(campo, valor_op)
                        elif operador == 'in':
                            query = query.in_(campo, valor_op)
                else:
                    # Filtro simple de igualdad
                    query = query.eq(campo, valor)
        
        # Aplicar ordenamiento ORDER BY
        if ordenamiento:
            for campo, direccion in ordenamiento.items():
                if direccion.lower() == 'desc':
                    query = query.order(campo, desc=True)
                else:
                    query = query.order(campo, desc=False)
        
        # Aplicar límite
        if limite:
            query = query.limit(limite)
        
        # Ejecutar consulta
        response = query.execute()
        
        return response.data
        
    except Exception as error:
        logger.error(f'Error en consulta_personalizada: {str(error)}')
        raise error

def consulta_con_join(tabla_principal, tabla_secundaria, campos_join, campos_select=None):
    """Ejecutar consulta con JOIN entre tablas"""
    try:
        # En Supabase, los JOINs se manejan de manera diferente
        # Por ahora, haremos consultas separadas y las combinaremos en Python
        
        # Obtener datos de la tabla principal
        response_principal = supabase.table(tabla_principal).select('*').execute()
        datos_principal = response_principal.data
        
        # Obtener datos de la tabla secundaria
        response_secundaria = supabase.table(tabla_secundaria).select('*').execute()
        datos_secundaria = response_secundaria.data
        
        # Crear diccionario para búsqueda rápida
        secundaria_dict = {}
        for registro in datos_secundaria:
            clave = registro.get(campos_join['secundaria'])
            if clave:
                secundaria_dict[clave] = registro
        
        # Combinar datos
        resultado = []
        for registro_principal in datos_principal:
            clave_join = registro_principal.get(campos_join['principal'])
            registro_secundario = secundaria_dict.get(clave_join, {})
            
            # Combinar registros
            registro_combinado = {**registro_principal}
            for campo, valor in registro_secundario.items():
                registro_combinado[f'{tabla_secundaria}_{campo}'] = valor
            
            resultado.append(registro_combinado)
        
        return resultado
        
    except Exception as error:
        logger.error(f'Error en consulta_con_join: {str(error)}')
        raise error

def buscar_por_texto(tabla, campo, texto):
    """Buscar registros que contengan texto específico"""
    try:
        # Usar ILIKE para búsqueda insensible a mayúsculas/minúsculas
        response = supabase.table(tabla).select('*').ilike(campo, f'%{texto}%').execute()
        return response.data
    except Exception as error:
        logger.error(f'Error en buscar_por_texto: {str(error)}')
        raise error

def buscar_por_fecha(tabla, campo_fecha, fecha_inicio=None, fecha_fin=None):
    """Buscar registros por rango de fechas"""
    try:
        query = supabase.table(tabla).select('*')
        
        if fecha_inicio:
            query = query.gte(campo_fecha, fecha_inicio)
        
        if fecha_fin:
            query = query.lte(campo_fecha, fecha_fin)
        
        response = query.execute()
        return response.data
    except Exception as error:
        logger.error(f'Error en buscar_por_fecha: {str(error)}')
        raise error

def obtener_estadisticas(tabla, campo_agrupacion=None):
    """Obtener estadísticas básicas de una tabla"""
    try:
        # Obtener todos los registros
        response = supabase.table(tabla).select('*').execute()
        datos = response.data
        
        if not datos:
            return {'total': 0}
        
        estadisticas = {
            'total': len(datos),
            'ultima_actualizacion': max(d.get('fecha', '') for d in datos if d.get('fecha'))
        }
        
        # Agrupación por campo específico
        if campo_agrupacion:
            grupos = {}
            for registro in datos:
                valor = registro.get(campo_agrupacion, 'Sin especificar')
                grupos[valor] = grupos.get(valor, 0) + 1
            
            estadisticas['agrupacion'] = grupos
        
        return estadisticas
        
    except Exception as error:
        logger.error(f'Error en obtener_estadisticas: {str(error)}')
        raise error

def exportar_consulta(tabla, filtros=None, formato='json'):
    """Exportar resultados de consulta en diferentes formatos"""
    try:
        # Ejecutar consulta
        datos = consulta_personalizada(tabla, filtros)
        
        if formato.lower() == 'json':
            return datos
        elif formato.lower() == 'csv':
            # Convertir a CSV
            if not datos:
                return ''
            
            # Obtener encabezados
            headers = list(datos[0].keys())
            csv_lines = [','.join(headers)]
            
            # Agregar datos
            for registro in datos:
                fila = [str(registro.get(header, '')) for header in headers]
                csv_lines.append(','.join(fila))
            
            return '\n'.join(csv_lines)
        else:
            raise ValueError(f'Formato no soportado: {formato}')
        
    except Exception as error:
        logger.error(f'Error en exportar_consulta: {str(error)}')
        raise error
