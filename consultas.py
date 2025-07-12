from flask import session, request, jsonify
from supabase.client import create_client, Client
import os
from datetime import datetime
import logging
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

def ver_historial(tabla='', estado='', usuario=''):
    """Ver historial con filtros - convertido de verHistorial()"""
    try:
        # Construir consulta base
        query = supabase.table('historial_cambios').select('*')
        
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
        response = supabase.table('historial_cambios').select('*').eq('id', id_historial).execute()
        
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
            
            supabase.table('historial_cambios').insert(nuevo_registro_historial).execute()
            
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
            
            supabase.table('historial_cambios').insert(nuevo_registro_historial).execute()
            
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

def consulta_con_relaciones(tabla_principal, relaciones=None, filtros=None, ordenamiento=None, limite=None):
    """Realizar consulta con relaciones entre tablas"""
    try:
        query = supabase.table(tabla_principal).select('*')
        
        # Agregar relaciones si se especifican
        if relaciones:
            for relacion in relaciones:
                query = query.select(f'{relacion}.*')
        
        # Aplicar filtros
        if filtros:
            for campo, valor in filtros.items():
                if isinstance(valor, dict):
                    # Filtros complejos (rango, like, etc.)
                    for operador, valor_filtro in valor.items():
                        if operador == 'gte':
                            query = query.gte(campo, valor_filtro)
                        elif operador == 'lte':
                            query = query.lte(campo, valor_filtro)
                        elif operador == 'like':
                            query = query.like(campo, f'%{valor_filtro}%')
                        elif operador == 'in':
                            query = query.in_(campo, valor_filtro)
                else:
                    # Filtro simple
                    query = query.eq(campo, valor)
        
        # Aplicar ordenamiento
        if ordenamiento:
            for campo, direccion in ordenamiento.items():
                if direccion.lower() == 'desc':
                    query = query.order(campo, desc=True)
                else:
                    query = query.order(campo)
        
        # Aplicar límite
        if limite:
            query = query.limit(limite)
        
        response = query.execute()
        return response.data
        
    except Exception as e:
        print(f"Error en consulta_con_relaciones: {e}")
        raise e

def consulta_reuniones_con_predicador(filtros=None):
    """Consultar reuniones con información del predicador"""
    try:
        query = supabase.table('reuniones').select('*, predicadores(nombre, apellido, numero)')
        
        if filtros:
            for campo, valor in filtros.items():
                query = query.eq(campo, valor)
        
        response = query.execute()
        return response.data
        
    except Exception as e:
        print(f"Error en consulta_reuniones_con_predicador: {e}")
        raise e

def consulta_asistencias_con_joven(filtros=None):
    """Consultar asistencias con información del joven"""
    try:
        query = supabase.table('asistencias').select('*, jovenes(nombre, edad, telefono)')
        
        if filtros:
            for campo, valor in filtros.items():
                query = query.eq(campo, valor)
        
        response = query.execute()
        return response.data
        
    except Exception as e:
        print(f"Error en consulta_asistencias_con_joven: {e}")
        raise e

def consulta_finanzas_con_reunion(filtros=None):
    """Consultar finanzas con información de la reunión"""
    try:
        query = supabase.table('finanzas').select('*, reuniones(Dirige, fecha_reunion)')
        
        if filtros:
            for campo, valor in filtros.items():
                query = query.eq(campo, valor)
        
        response = query.execute()
        return response.data
        
    except Exception as e:
        print(f"Error en consulta_finanzas_con_reunion: {e}")
        raise e

def consulta_calendario_con_reunion(filtros=None):
    """Consultar calendario con información de la reunión"""
    try:
        query = supabase.table('calendario').select('*, reuniones(Dirige, fecha_reunion)')
        
        if filtros:
            for campo, valor in filtros.items():
                query = query.eq(campo, valor)
        
        response = query.execute()
        return response.data
        
    except Exception as e:
        print(f"Error en consulta_calendario_con_reunion: {e}")
        raise e

def consulta_completa_reunion(fecha_inicio=None, fecha_fin=None):
    """Consulta completa de una reunión con todos sus datos relacionados"""
    try:
        # Obtener reuniones en el rango de fechas
        query = supabase.table('reuniones').select('*')
        
        if fecha_inicio:
            query = query.gte('fecha_reunion', fecha_inicio)
        if fecha_fin:
            query = query.lte('fecha_reunion', fecha_fin)
        
        reuniones = query.execute().data
        
        resultado_completo = []
        
        for reunion in reuniones:
            reunion_id = reunion['id']
            
            # Obtener predicador
            predicador = None
            if reunion.get('predicador_id'):
                predicador_response = supabase.table('predicadores').select('*').eq('id', reunion['predicador_id']).execute()
                predicador = predicador_response.data[0] if predicador_response.data else None
            
            # Obtener asistencias
            asistencias_response = supabase.table('asistencias').select('*, jovenes(nombre, edad)').eq('reunion_id', reunion_id).execute()
            asistencias = asistencias_response.data
            
            # Obtener finanzas relacionadas
            finanzas_response = supabase.table('finanzas').select('*').eq('reunion_id', reunion_id).execute()
            finanzas = finanzas_response.data
            
            # Obtener eventos de calendario relacionados
            calendario_response = supabase.table('calendario').select('*').eq('reunion_id', reunion_id).execute()
            calendario = calendario_response.data
            
            reunion_completa = {
                'reunion': reunion,
                'predicador': predicador,
                'asistencias': asistencias,
                'finanzas': finanzas,
                'calendario': calendario,
                'total_asistencias': len(asistencias),
                'total_finanzas': len(finanzas),
                'monto_total': sum(float(f['Monto']) for f in finanzas if f.get('Monto'))
            }
            
            resultado_completo.append(reunion_completa)
        
        return resultado_completo
        
    except Exception as e:
        print(f"Error en consulta_completa_reunion: {e}")
        raise e

def consulta_estadisticas_relacionadas():
    """Obtener estadísticas con relaciones"""
    try:
        estadisticas = {}
        
        # Estadísticas de predicadores con reuniones
        predicadores_response = supabase.table('predicadores').select('id, nombre, apellido').execute()
        predicadores = predicadores_response.data
        
        for predicador in predicadores:
            reuniones_response = supabase.table('reuniones').select('id').eq('predicador_id', predicador['id']).execute()
            predicador['total_reuniones'] = len(reuniones_response.data)
        
        estadisticas['predicadores'] = predicadores
        
        # Estadísticas de jóvenes con asistencias
        jovenes_response = supabase.table('jovenes').select('id, nombre, edad').execute()
        jovenes = jovenes_response.data
        
        for joven in jovenes:
            asistencias_response = supabase.table('asistencias').select('*').eq('joven_id', joven['id']).execute()
            asistencias = asistencias_response.data
            
            joven['total_asistencias'] = len(asistencias)
            joven['asistencias_presente'] = sum(1 for a in asistencias if any(
                a.get('unoviernes') == 'Presente' or 
                a.get('dosviernes') == 'Presente' or 
                a.get('tresViernes') == 'Presente' or 
                a.get('cuatroviernes') == 'Presente'
            ))
        
        estadisticas['jovenes'] = jovenes
        
        # Estadísticas de finanzas por reunión
        finanzas_response = supabase.table('finanzas').select('*, reuniones(fecha_reunion)').execute()
        finanzas = finanzas_response.data
        
        estadisticas['finanzas_por_reunion'] = {}
        for finanza in finanzas:
            reunion_fecha = finanza.get('reuniones', {}).get('fecha_reunion')
            if reunion_fecha:
                if reunion_fecha not in estadisticas['finanzas_por_reunion']:
                    estadisticas['finanzas_por_reunion'][reunion_fecha] = 0
                estadisticas['finanzas_por_reunion'][reunion_fecha] += float(finanza.get('Monto', 0))
        
        return estadisticas
        
    except Exception as e:
        print(f"Error en consulta_estadisticas_relacionadas: {e}")
        raise e
