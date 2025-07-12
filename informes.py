from flask import session, request, jsonify
from supabase import create_client, Client
import os
from datetime import datetime
import logging
import json
import csv
from io import StringIO
from consultas import consulta_personalizada, obtener_estadisticas

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración Supabase
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def crear_informe(titulo, descripcion, consultas, formato='json'):
    """Crear un nuevo informe - convertido de funciones de informes"""
    try:
        # Preparar datos del informe
        datos_informe = {
            'titulo': titulo,
            'descripcion': descripcion,
            'consultas': consultas,
            'formato': formato,
            'fecha_creacion': datetime.now().isoformat(),
            'estado': 'activo'
        }
        
        # Guardar en Supabase
        response = supabase.table('informes').insert(datos_informe).execute()
        
        if response.data:
            return response.data[0]
        
        raise ValueError('Error al crear informe')
    except Exception as error:
        logger.error(f'Error en crear_informe: {str(error)}')
        raise error

def obtener_informe_por_id(id_informe):
    """Obtener un informe específico por ID"""
    try:
        response = supabase.table('informes').select('*').eq('id', id_informe).eq('estado', 'activo').execute()
        
        if response.data:
            return response.data[0]
        
        return None
    except Exception as error:
        logger.error(f'Error en obtener_informe_por_id: {str(error)}')
        raise error

def obtener_informes():
    """Obtener todos los informes - convertido de funciones de informes"""
    try:
        response = supabase.table('informes').select('*').eq('estado', 'activo').execute()
        return response.data
    except Exception as error:
        logger.error(f'Error en obtener_informes: {str(error)}')
        raise error

def eliminar_informe(id_informe):
    """Eliminar informe - convertido de funciones de informes"""
    try:
        # Soft delete - marcar como inactivo
        response = supabase.table('informes').update({'estado': 'inactivo'}).eq('id', id_informe).execute()
        
        if response.data:
            return True
        
        raise ValueError('Error al eliminar informe')
    except Exception as error:
        logger.error(f'Error en eliminar_informe: {str(error)}')
        raise error

def generar_informe(id_informe):
    """Generar contenido del informe ejecutando las consultas"""
    try:
        # Obtener información del informe
        response = supabase.table('informes').select('*').eq('id', id_informe).execute()
        
        if not response.data:
            raise ValueError('Informe no encontrado')
        
        informe = response.data[0]
        consultas = informe.get('consultas', [])
        formato = informe.get('formato', 'json')
        
        # Ejecutar cada consulta
        resultados = {}
        for i, consulta in enumerate(consultas):
            try:
                tabla = consulta.get('tabla')
                filtros = consulta.get('filtros', {})
                ordenamiento = consulta.get('ordenamiento', {})
                limite = consulta.get('limite')
                
                # Ejecutar consulta
                datos = consulta_personalizada(tabla, filtros, ordenamiento, limite)
                
                # Obtener estadísticas
                estadisticas = obtener_estadisticas(tabla)
                
                resultados[f'consulta_{i+1}'] = {
                    'tabla': tabla,
                    'datos': datos,
                    'estadisticas': estadisticas,
                    'total_registros': len(datos)
                }
                
            except Exception as e:
                logger.error(f'Error en consulta {i+1}: {str(e)}')
                resultados[f'consulta_{i+1}'] = {
                    'error': str(e),
                    'tabla': consulta.get('tabla', 'Desconocida')
                }
        
        # Generar contenido según formato
        if formato.lower() == 'json':
            return json.dumps(resultados, indent=2, ensure_ascii=False)
        elif formato.lower() == 'csv':
            return generar_csv_informe(resultados)
        else:
            return json.dumps(resultados, indent=2, ensure_ascii=False)
        
    except Exception as error:
        logger.error(f'Error en generar_informe: {str(error)}')
        raise error

def generar_csv_informe(resultados):
    """Generar CSV a partir de los resultados del informe"""
    try:
        output = StringIO()
        writer = csv.writer(output)
        
        # Escribir encabezado principal
        writer.writerow(['INFORME GENERADO'])
        writer.writerow(['Fecha:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
        writer.writerow([])
        
        for nombre_consulta, resultado in resultados.items():
            if 'error' in resultado:
                writer.writerow([f'ERROR EN {nombre_consulta.upper()}'])
                writer.writerow([resultado['error']])
                writer.writerow([])
                continue
            
            # Escribir encabezado de consulta
            writer.writerow([f'CONSULTA: {nombre_consulta.upper()}'])
            writer.writerow([f'Tabla: {resultado["tabla"]}'])
            writer.writerow([f'Total registros: {resultado["total_registros"]}'])
            writer.writerow([])
            
            # Escribir datos
            if resultado['datos']:
                # Encabezados de columnas
                headers = list(resultado['datos'][0].keys())
                writer.writerow(headers)
                
                # Datos
                for registro in resultado['datos']:
                    fila = [str(registro.get(header, '')) for header in headers]
                    writer.writerow(fila)
            
            writer.writerow([])
            writer.writerow([])
        
        return output.getvalue()
        
    except Exception as error:
        logger.error(f'Error en generar_csv_informe: {str(error)}')
        raise error

def descargar_informe(id_informe, formato='json'):
    """Descargar informe en formato específico"""
    try:
        contenido = generar_informe(id_informe)
        
        # Obtener información del informe
        response = supabase.table('informes').select('titulo').eq('id', id_informe).execute()
        titulo = response.data[0]['titulo'] if response.data else 'informe'
        
        # Generar nombre de archivo
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"{titulo}_{timestamp}.{formato.lower()}"
        
        return {
            'contenido': contenido,
            'nombre_archivo': nombre_archivo,
            'formato': formato
        }
        
    except Exception as error:
        logger.error(f'Error en descargar_informe: {str(error)}')
        raise error

def compartir_informe(id_informe, destinatarios, asunto=None):
    """Compartir informe por email - prepara datos para envío"""
    try:
        # Generar contenido del informe
        contenido = generar_informe(id_informe)
        
        # Obtener información del informe
        response = supabase.table('informes').select('titulo, descripcion').eq('id', id_informe).execute()
        informe = response.data[0] if response.data else {}
        
        # Preparar datos para envío
        datos_email = {
            'destinatarios': destinatarios,
            'asunto': asunto or f"Informe: {informe.get('titulo', 'Sin título')}",
            'contenido': contenido,
            'descripcion': informe.get('descripcion', ''),
            'fecha_envio': datetime.now().isoformat()
        }
        
        return datos_email
        
    except Exception as error:
        logger.error(f'Error en compartir_informe: {str(error)}')
        raise error

def generar_informe_predicadores(filtros=None):
    """Generar informe específico de predicadores"""
    try:
        # Consulta base de predicadores
        datos_predicadores = consulta_personalizada('predicadores', filtros)
        
        # Estadísticas
        total_predicadores = len(datos_predicadores)
        predicadores_activos = len([p for p in datos_predicadores if p.get('estado') != 'eliminado'])
        
        # Agrupar por estado
        estados = {}
        for predicador in datos_predicadores:
            estado = predicador.get('estado', 'Sin estado')
            estados[estado] = estados.get(estado, 0) + 1
        
        informe = {
            'titulo': 'Informe de Predicadores',
            'fecha_generacion': datetime.now().isoformat(),
            'resumen': {
                'total_predicadores': total_predicadores,
                'predicadores_activos': predicadores_activos,
                'predicadores_eliminados': total_predicadores - predicadores_activos
            },
            'estados': estados,
            'datos_detallados': datos_predicadores
        }
        
        return informe
        
    except Exception as error:
        logger.error(f'Error en generar_informe_predicadores: {str(error)}')
        raise error

def generar_informe_finanzas(fecha_inicio=None, fecha_fin=None, limite=None):
    """Generar informe financiero"""
    try:
        # Filtros de fecha
        filtros = {}
        if fecha_inicio:
            filtros['fecha'] = {'gte': fecha_inicio}
        if fecha_fin:
            filtros['fecha'] = filtros.get('fecha', {})
            filtros['fecha']['lte'] = fecha_fin
        
        # Obtener datos financieros
        datos_finanzas = consulta_personalizada('finanzas', filtros)
        
        # Aplicar límite si se especifica
        if limite:
            datos_finanzas = datos_finanzas[:limite]
        
        # Calcular totales
        total_ingresos = sum(float(f.get('ingreso_total', 0)) for f in datos_finanzas)
        total_gastos = sum(float(f.get('gasto', 0)) for f in datos_finanzas)
        total_ganancias = sum(float(f.get('ganancia', 0)) for f in datos_finanzas)
        total_perdidas = sum(float(f.get('perdida', 0)) for f in datos_finanzas)
        
        # Agrupar por actividad/producto
        actividades = {}
        for registro in datos_finanzas:
            actividad = registro.get('actividad_producto', 'Sin especificar')
            if actividad not in actividades:
                actividades[actividad] = {
                    'ingresos': 0,
                    'gastos': 0,
                    'ganancias': 0,
                    'perdidas': 0,
                    'registros': 0
                }
            
            actividades[actividad]['ingresos'] += float(registro.get('ingreso_total', 0))
            actividades[actividad]['gastos'] += float(registro.get('gasto', 0))
            actividades[actividad]['ganancias'] += float(registro.get('ganancia', 0))
            actividades[actividad]['perdidas'] += float(registro.get('perdida', 0))
            actividades[actividad]['registros'] += 1
        
        informe = {
            'titulo': 'Informe Financiero',
            'fecha_generacion': datetime.now().isoformat(),
            'periodo': {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            },
            'resumen': {
                'total_ingresos': total_ingresos,
                'total_gastos': total_gastos,
                'total_ganancias': total_ganancias,
                'total_perdidas': total_perdidas,
                'balance': total_ganancias - total_perdidas
            },
            'actividades': actividades,
            'datos_detallados': datos_finanzas
        }
        
        return informe
        
    except Exception as error:
        logger.error(f'Error en generar_informe_finanzas: {str(error)}')
        raise error

def generar_informe_asistencias(fecha_inicio=None, fecha_fin=None, limite=None):
    """Generar informe de asistencias"""
    try:
        # Filtros de fecha
        filtros = {}
        if fecha_inicio:
            filtros['fecha'] = {'gte': fecha_inicio}
        if fecha_fin:
            filtros['fecha'] = filtros.get('fecha', {})
            filtros['fecha']['lte'] = fecha_fin
        
        # Obtener datos de asistencias
        datos_asistencias = consulta_personalizada('asistencias', filtros)
        
        # Aplicar límite si se especifica
        if limite:
            datos_asistencias = datos_asistencias[:limite]
        
        # Calcular estadísticas
        total_personas = len(datos_asistencias)
        total_asistencias = 0
        
        for asistencia in datos_asistencias:
            total_asistencias += sum([
                asistencia.get('unoviernes', 0),
                asistencia.get('dosviernes', 0),
                asistencia.get('tresViernes', 0),
                asistencia.get('cuatroviernes', 0),
                asistencia.get('cincoviernes', 0)
            ])
        
        # Promedio de asistencia por persona
        promedio_asistencia = total_asistencias / total_personas if total_personas > 0 else 0
        
        informe = {
            'titulo': 'Informe de Asistencias',
            'fecha_generacion': datetime.now().isoformat(),
            'periodo': {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            },
            'resumen': {
                'total_personas': total_personas,
                'total_asistencias': total_asistencias,
                'promedio_asistencia_por_persona': round(promedio_asistencia, 2)
            },
            'datos_detallados': datos_asistencias
        }
        
        return informe
        
    except Exception as error:
        logger.error(f'Error en generar_informe_asistencias: {str(error)}')
        raise error

def guardar_informe_generado(informe_data, nombre_archivo=None):
    """Guardar informe generado en Supabase Storage o como registro"""
    try:
        # Crear registro del informe generado
        datos_guardado = {
            'titulo': informe_data.get('titulo', 'Informe sin título'),
            'contenido': json.dumps(informe_data, ensure_ascii=False),
            'fecha_generacion': datetime.now().isoformat(),
            'tipo': 'generado',
            'nombre_archivo': nombre_archivo or f"informe_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        }
        
        # Guardar en tabla de informes generados
        response = supabase.table('informes_generados').insert(datos_guardado).execute()
        
        if response.data:
            return response.data[0]
        
        raise ValueError('Error al guardar informe generado')
        
    except Exception as error:
        logger.error(f'Error en guardar_informe_generado: {str(error)}')
        raise error

def generar_informe_actividades(fecha_inicio=None, fecha_fin=None, limite=None):
    """Generar informe de actividades - convertido de funciones de informes"""
    try:
        # Obtener datos de actividades (reuniones y eventos del calendario)
        response_reuniones = supabase.table('reuniones').select('*').execute()
        response_calendario = supabase.table('calendario').select('*').execute()
        
        reuniones = response_reuniones.data if response_reuniones.data else []
        eventos = response_calendario.data if response_calendario.data else []
        
        # Combinar actividades
        actividades = []
        
        # Agregar reuniones
        for reunion in reuniones:
            actividades.append({
                'fecha': reunion.get('fecha'),
                'nombre': reunion.get('nombre', 'Reunión'),
                'estado': reunion.get('estado', 'programada'),
                'participantes': reunion.get('asistentes', 0),
                'tipo': 'reunion'
            })
        
        # Agregar eventos del calendario
        for evento in eventos:
            actividades.append({
                'fecha': evento.get('fecha'),
                'nombre': evento.get('titulo', 'Evento'),
                'estado': evento.get('estado', 'programado'),
                'participantes': evento.get('participantes', 0),
                'tipo': 'evento'
            })
        
        # Filtrar por fechas si se especifican
        if fecha_inicio or fecha_fin:
            actividades_filtradas = []
            for actividad in actividades:
                fecha_actividad = actividad.get('fecha')
                if fecha_actividad:
                    if fecha_inicio and fecha_actividad < fecha_inicio:
                        continue
                    if fecha_fin and fecha_actividad > fecha_fin:
                        continue
                    actividades_filtradas.append(actividad)
            actividades = actividades_filtradas
        
        # Aplicar límite si se especifica
        if limite:
            actividades = actividades[:limite]
        
        # Calcular estadísticas
        total_actividades = len(actividades)
        actividades_completadas = len([a for a in actividades if a.get('estado') == 'completada'])
        
        # Preparar resultado
        resultado = {
            'total_actividades': total_actividades,
            'actividades_completadas': actividades_completadas,
            'actividades': actividades,
            'periodo': {
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin
            }
        }
        
        return resultado
        
    except Exception as error:
        logger.error(f'Error en generar_informe_actividades: {str(error)}')
        raise error

def generar_informe_resumen_general(filtros=None, limite=None):
    """Generar informe de resumen general - convertido de funciones de informes"""
    try:
        # Obtener estadísticas de todas las tablas principales
        estadisticas = {}
        
        # Predicadores
        response_predicadores = supabase.table('predicadores').select('*').execute()
        total_predicadores = len(response_predicadores.data) if response_predicadores.data else 0
        estadisticas['predicadores'] = total_predicadores
        
        # Jóvenes
        response_jovenes = supabase.table('jovenes').select('*').execute()
        total_jovenes = len(response_jovenes.data) if response_jovenes.data else 0
        estadisticas['jovenes'] = total_jovenes
        
        # Reuniones
        response_reuniones = supabase.table('reuniones').select('*').execute()
        total_reuniones = len(response_reuniones.data) if response_reuniones.data else 0
        estadisticas['reuniones'] = total_reuniones
        
        # Asistencias
        response_asistencias = supabase.table('asistencias').select('*').execute()
        total_asistencias = len(response_asistencias.data) if response_asistencias.data else 0
        estadisticas['asistencias'] = total_asistencias
        
        # Finanzas
        response_finanzas = supabase.table('finanzas').select('*').execute()
        total_finanzas = len(response_finanzas.data) if response_finanzas.data else 0
        estadisticas['finanzas'] = total_finanzas
        
        # Preparar resultado
        resultado = {
            'totalPredicadores': total_predicadores,
            'totalJovenes': total_jovenes,
            'totalReuniones': total_reuniones,
            'totalAsistencias': total_asistencias,
            'totalFinanzas': total_finanzas,
            'estadisticas': estadisticas,
            'fecha_generacion': datetime.now().isoformat()
        }
        
        return resultado
        
    except Exception as error:
        logger.error(f'Error en generar_informe_resumen_general: {str(error)}')
        raise error
