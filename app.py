from flask import Flask, render_template, request, jsonify, session, send_file
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
from datetime import datetime, timedelta
import json
from io import BytesIO
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Importar módulos de backend
from sesion import *
from tablas import *
from informes import *
from email_utils import enviar_por_correo, verificar_configuracion_email
from formularios import *
from consultas import *

app = Flask(__name__)
CORS(app)

# Configuración
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-change-in-production')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['GMAIL_PASS'] = os.environ.get('GMAIL_PASS', '')
app.config['SUPABASE_URL'] = os.environ.get('SUPABASE_URL', '')
app.config['SUPABASE_KEY'] = os.environ.get('SUPABASE_KEY', '')

# Inicializar JWT
jwt = JWTManager(app)

# Inicializar Rate Limiter
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Verificar configuración de Supabase
if not app.config['SUPABASE_URL'] or not app.config['SUPABASE_KEY']:
    print("⚠️  ADVERTENCIA: Variables de entorno de Supabase no configuradas")
    print(f"SUPABASE_URL: {app.config['SUPABASE_URL']}")
    print(f"SUPABASE_KEY: {'Configurada' if app.config['SUPABASE_KEY'] else 'No configurada'}")
else:
    print("✅ Variables de entorno de Supabase configuradas correctamente")

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/health')
def health():
    """Endpoint de salud para verificar que el servidor esté funcionando"""
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'supabase_configured': bool(app.config['SUPABASE_URL'] and app.config['SUPABASE_KEY'])
    })

@app.route('/tablas')
def tablas():
    """Página de tablas"""
    return render_template('Tablas.html')

@app.route('/informes')
def informes():
    """Página de informes"""
    return render_template('Informe.html')

@app.route('/formularios')
def formularios():
    """Página de formularios"""
    return render_template('Formulario.html')

@app.route('/consultas')
def consultas():
    """Página de consultas"""
    return render_template('Consultas.html')

@app.route('/admin')
def admin():
    """Página de administradores"""
    return render_template('Tablas.html')

# ===== RUTAS API DE SESIÓN =====

@app.route('/api/sesion/login', methods=['POST'])
@limiter.limit("5 per minute")
def api_login():
    """Login de usuario con JWT"""
    try:
        data = request.get_json()
        codigo = data.get('codigo')
        nombre = data.get('nombre')
        
        if is_admin_by_name(nombre, codigo):
            # Crear token JWT
            access_token = create_access_token(identity=nombre)
            
            # También mantener sesión para compatibilidad
            session['user_nombre'] = nombre
            
            return jsonify({
                'success': True,
                'message': 'Login exitoso',
                'user': {'nombre': nombre},
                'rol': get_admin_role(nombre),
                'access_token': access_token
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Credenciales inválidas'
            }), 401
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sesion/logout', methods=['POST'])
def api_logout():
    """Logout de usuario"""
    try:
        session.clear()
        return jsonify({'success': True, 'message': 'Logout exitoso'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/sesion/verificar', methods=['GET'])
def api_verificar_sesion():
    """Verificar sesión de usuario"""
    try:
        user_email = session.get('user_email')
        if user_email and check_access():
            return jsonify({
                'success': True,
                'authenticated': True,
                'user': {
                    'email': user_email,
                    'nombre': session.get('user_nombre'),
                    'is_super_admin': is_super_admin(user_email)
                }
            })
        else:
            return jsonify({
                'success': True,
                'authenticated': False
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== RUTAS API DE TABLAS =====

@app.route('/api/tablas/predicadores', methods=['GET'])
def api_obtener_predicadores():
    """Obtener predicadores"""
    try:
        id = request.args.get('id')
        print(f"🔍 Buscando predicadores - ID: {id}")
        predicadores = buscar_predicadores_por_id(id)
        print(f"✅ Predicadores encontrados: {len(predicadores)}")
        return jsonify({'success': True, 'data': predicadores})
    except Exception as e:
        print(f"❌ Error en api_obtener_predicadores: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/predicadores', methods=['POST'])
def api_crear_predicador():
    """Crear predicador"""
    try:
        data = request.get_json()
        data['usuario'] = session.get('user_email', 'sistema')
        predicador = obtener_ultima_id_y_registrar_predicadores(data)
        return jsonify({'success': True, 'data': predicador})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/predicadores/<int:id>', methods=['PUT'])
def api_actualizar_predicador(id):
    """Actualizar predicador"""
    try:
        data = request.get_json()
        data['id'] = id
        data['usuario'] = session.get('user_email', 'sistema')
        predicador = editar_predicadores(data)
        return jsonify({'success': True, 'data': predicador})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/predicadores/<int:id>', methods=['DELETE'])
def api_eliminar_predicador(id):
    """Eliminar predicador"""
    try:
        resultado = eliminar_predicadores(id)
        return jsonify({'success': True, 'message': 'Predicador eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/reuniones', methods=['GET'])
def api_obtener_reuniones():
    """Obtener reuniones"""
    try:
        id = request.args.get('id')
        reuniones = buscar_reuniones_por_id(id)
        return jsonify({'success': True, 'data': reuniones})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/reuniones', methods=['POST'])
def api_crear_reunion():
    """Crear reunión"""
    try:
        data = request.get_json()
        id_reunion = obtener_ultima_id_y_registrar_reuniones(data)
        return jsonify({'success': True, 'id': id_reunion})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/reuniones/<int:id>', methods=['PUT'])
def api_actualizar_reunion(id):
    """Actualizar reunión"""
    try:
        data = request.get_json()
        data['id'] = id
        reunion = editar_reuniones(data)
        return jsonify({'success': True, 'data': reunion})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/reuniones/<int:id>', methods=['DELETE'])
def api_eliminar_reunion(id):
    """Eliminar reunión"""
    try:
        resultado = eliminar_reuniones(id)
        return jsonify({'success': True, 'message': 'Reunión eliminada'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/calendario', methods=['GET'])
def api_obtener_calendario():
    """Obtener calendario"""
    try:
        id = request.args.get('id')
        eventos = buscar_calendario_por_id(id)
        return jsonify({'success': True, 'data': eventos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/calendario', methods=['POST'])
def api_crear_evento():
    """Crear evento"""
    try:
        data = request.get_json()
        id_evento = obtener_ultima_id_y_registrar_calendario(data)
        return jsonify({'success': True, 'id': id_evento})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/calendario/<int:id>', methods=['PUT'])
def api_actualizar_evento(id):
    """Actualizar evento"""
    try:
        data = request.get_json()
        data['id'] = id
        evento = editar_calendario(data)
        return jsonify({'success': True, 'data': evento})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/tablas/calendario/<int:id>', methods=['DELETE'])
def api_eliminar_evento(id):
    """Eliminar evento"""
    try:
        resultado = eliminar_calendario(id)
        return jsonify({'success': True, 'message': 'Evento eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== RUTAS API DE FORMULARIOS =====

@app.route('/api/formularios/bandeja', methods=['GET'])
def api_obtener_bandeja():
    """Obtener bandeja"""
    try:
        id = request.args.get('id')
        print(f"🔍 Buscando bandeja - ID: {id}")
        tareas = buscar_bandeja_por_id(id)
        print(f"✅ Tareas en bandeja encontradas: {len(tareas)}")
        return jsonify({'success': True, 'data': tareas})
    except Exception as e:
        print(f"❌ Error en api_obtener_bandeja: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/bandeja', methods=['POST'])
def api_crear_tarea():
    """Crear tarea en bandeja"""
    try:
        data = request.get_json()
        tarea = obtener_ultima_id_y_registrar_bandeja(data)
        return jsonify({'success': True, 'data': tarea})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/bandeja/<int:id>', methods=['PUT'])
def api_actualizar_tarea(id):
    """Actualizar tarea"""
    try:
        data = request.get_json()
        data['id'] = id
        tarea = editar_bandeja(data)
        return jsonify({'success': True, 'data': tarea})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/bandeja/<int:id>', methods=['DELETE'])
def api_eliminar_tarea(id):
    """Eliminar tarea"""
    try:
        resultado = eliminar_bandeja(id)
        return jsonify({'success': True, 'message': 'Tarea eliminada'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/asistencias', methods=['GET'])
def api_obtener_asistencias():
    """Obtener asistencias"""
    try:
        id = request.args.get('id')
        asistencias = buscar_asistencias_por_id(id)
        return jsonify({'success': True, 'data': asistencias})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/asistencias', methods=['POST'])
def api_crear_asistencia():
    """Crear asistencia"""
    try:
        data = request.get_json()
        id_asistencia = obtener_ultima_id_y_registrar_asistencias(data)
        return jsonify({'success': True, 'id': id_asistencia})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/asistencias/<int:id>', methods=['PUT'])
def api_actualizar_asistencia(id):
    """Actualizar asistencia"""
    try:
        data = request.get_json()
        data['id'] = id
        asistencia = editar_asistencias(data)
        return jsonify({'success': True, 'data': asistencia})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/asistencias/<int:id>', methods=['DELETE'])
def api_eliminar_asistencia(id):
    """Eliminar asistencia"""
    try:
        resultado = eliminar_asistencias(id)
        return jsonify({'success': True, 'message': 'Asistencia eliminada'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/jovenes', methods=['GET'])
def api_obtener_jovenes():
    """Obtener jóvenes"""
    try:
        id = request.args.get('id')
        jovenes = buscar_jovenes_por_id(id)
        return jsonify({'success': True, 'data': jovenes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/jovenes', methods=['POST'])
def api_crear_joven():
    """Crear joven"""
    try:
        data = request.get_json()
        id_joven = obtener_ultima_id_y_registrar_jovenes(data)
        return jsonify({'success': True, 'id': id_joven})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/jovenes/<int:id>', methods=['PUT'])
def api_actualizar_joven(id):
    """Actualizar joven"""
    try:
        data = request.get_json()
        data['id'] = id
        joven = editar_jovenes(data)
        return jsonify({'success': True, 'data': joven})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/jovenes/<int:id>', methods=['DELETE'])
def api_eliminar_joven(id):
    """Eliminar joven"""
    try:
        resultado = eliminar_jovenes(id)
        return jsonify({'success': True, 'message': 'Joven eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/finanzas', methods=['GET'])
def api_obtener_finanzas():
    """Obtener finanzas"""
    try:
        id = request.args.get('id')
        finanzas = buscar_finanzas_por_id(id)
        return jsonify({'success': True, 'data': finanzas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/finanzas', methods=['POST'])
def api_crear_finanza():
    """Crear registro financiero"""
    try:
        data = request.get_json()
        id_finanza = obtener_ultima_id_y_registrar_finanzas(data)
        return jsonify({'success': True, 'id': id_finanza})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/finanzas/<int:id>', methods=['PUT'])
def api_actualizar_finanza(id):
    """Actualizar registro financiero"""
    try:
        data = request.get_json()
        data['id'] = id
        finanza = editar_finanzas(data)
        return jsonify({'success': True, 'data': finanza})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/formularios/finanzas/<int:id>', methods=['DELETE'])
def api_eliminar_finanza(id):
    """Eliminar registro financiero"""
    try:
        resultado = eliminar_finanzas(id)
        return jsonify({'success': True, 'message': 'Registro financiero eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== RUTAS API DE CONSULTAS =====

@app.route('/api/consultas/historial', methods=['GET'])
def api_obtener_historial():
    """Obtener historial con filtros"""
    try:
        tabla = request.args.get('tabla', '')
        estado = request.args.get('estado', '')
        usuario = request.args.get('usuario', '')
        
        historial = ver_historial(tabla, estado, usuario)
        return jsonify({'success': True, 'data': historial})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/historial/<int:id>', methods=['GET'])
def api_obtener_registro_historial(id):
    """Obtener registro específico del historial"""
    try:
        registro = obtener_registro_historial(id)
        if registro:
            return jsonify({'success': True, 'data': registro})
        else:
            return jsonify({'success': False, 'message': 'Registro no encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/historial/<int:id>/revertir', methods=['POST'])
def api_revertir_edicion(id):
    """Revertir edición"""
    try:
        resultado = revertir_edicion(id)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/historial/<int:id>/restaurar', methods=['POST'])
def api_restaurar_registro(id):
    """Restaurar registro eliminado"""
    try:
        resultado = restaurar_registro(id)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/personalizada', methods=['POST'])
def api_consulta_personalizada():
    """Ejecutar consulta personalizada"""
    try:
        data = request.get_json()
        tabla = data.get('tabla')
        filtros = data.get('filtros', {})
        ordenamiento = data.get('ordenamiento', {})
        limite = data.get('limite')
        
        if not tabla:
            return jsonify({'success': False, 'error': 'Tabla requerida'}), 400
        
        resultados = consulta_personalizada(tabla, filtros, ordenamiento, limite)
        return jsonify({'success': True, 'data': resultados})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/buscar', methods=['POST'])
def api_buscar_por_texto():
    """Buscar por texto"""
    try:
        data = request.get_json()
        tabla = data.get('tabla')
        campo = data.get('campo')
        texto = data.get('texto')
        
        if not all([tabla, campo, texto]):
            return jsonify({'success': False, 'error': 'Tabla, campo y texto requeridos'}), 400
        
        resultados = buscar_por_texto(tabla, campo, texto)
        return jsonify({'success': True, 'data': resultados})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/fecha', methods=['POST'])
def api_buscar_por_fecha():
    """Buscar por rango de fechas"""
    try:
        data = request.get_json()
        tabla = data.get('tabla')
        campo_fecha = data.get('campo_fecha')
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        if not all([tabla, campo_fecha]):
            return jsonify({'success': False, 'error': 'Tabla y campo_fecha requeridos'}), 400
        
        resultados = buscar_por_fecha(tabla, campo_fecha, fecha_inicio, fecha_fin)
        return jsonify({'success': True, 'data': resultados})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/relaciones', methods=['POST'])
def api_consulta_con_relaciones():
    """Realizar consulta con relaciones entre tablas"""
    try:
        data = request.get_json()
        tabla_principal = data.get('tabla')
        relaciones = data.get('relaciones', [])
        filtros = data.get('filtros', {})
        ordenamiento = data.get('ordenamiento', {})
        limite = data.get('limite')
        
        from consultas import consulta_con_relaciones
        resultado = consulta_con_relaciones(tabla_principal, relaciones, filtros, ordenamiento, limite)
        
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/reuniones-predicador', methods=['POST'])
def api_consulta_reuniones_predicador():
    """Consultar reuniones con información del predicador"""
    try:
        data = request.get_json()
        filtros = data.get('filtros', {})
        
        from consultas import consulta_reuniones_con_predicador
        resultado = consulta_reuniones_con_predicador(filtros)
        
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/asistencias-joven', methods=['POST'])
def api_consulta_asistencias_joven():
    """Consultar asistencias con información del joven"""
    try:
        data = request.get_json()
        filtros = data.get('filtros', {})
        
        from consultas import consulta_asistencias_con_joven
        resultado = consulta_asistencias_con_joven(filtros)
        
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/finanzas-reunion', methods=['POST'])
def api_consulta_finanzas_reunion():
    """Consultar finanzas con información de la reunión"""
    try:
        data = request.get_json()
        filtros = data.get('filtros', {})
        
        from consultas import consulta_finanzas_con_reunion
        resultado = consulta_finanzas_con_reunion(filtros)
        
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/calendario-reunion', methods=['POST'])
def api_consulta_calendario_reunion():
    """Consultar calendario con información de la reunión"""
    try:
        data = request.get_json()
        filtros = data.get('filtros', {})
        
        from consultas import consulta_calendario_con_reunion
        resultado = consulta_calendario_con_reunion(filtros)
        
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/reunion-completa', methods=['POST'])
def api_consulta_reunion_completa():
    """Consulta completa de una reunión con todos sus datos relacionados"""
    try:
        data = request.get_json()
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        from consultas import consulta_completa_reunion
        resultado = consulta_completa_reunion(fecha_inicio, fecha_fin)
        
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/estadisticas-relacionadas', methods=['GET'])
def api_estadisticas_relacionadas():
    """Obtener estadísticas con relaciones"""
    try:
        from consultas import consulta_estadisticas_relacionadas
        resultado = consulta_estadisticas_relacionadas()
        
        return jsonify({'success': True, 'data': resultado})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/estadisticas/<tabla>', methods=['GET'])
def api_obtener_estadisticas(tabla):
    """Obtener estadísticas de una tabla"""
    try:
        campo_agrupacion = request.args.get('campo_agrupacion')
        estadisticas = obtener_estadisticas(tabla, campo_agrupacion)
        return jsonify({'success': True, 'data': estadisticas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/consultas/exportar', methods=['POST'])
def api_exportar_consulta():
    """Exportar consulta en diferentes formatos"""
    try:
        data = request.get_json()
        tabla = data.get('tabla')
        filtros = data.get('filtros', {})
        formato = data.get('formato', 'json')
        
        if not tabla:
            return jsonify({'success': False, 'error': 'Tabla requerida'}), 400
        
        contenido = exportar_consulta(tabla, filtros, formato)
        
        if formato.lower() == 'csv':
            # Devolver como archivo descargable
            buffer = BytesIO(contenido.encode('utf-8'))
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name=f"{tabla}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mimetype='text/csv'
            )
        else:
            return jsonify({'success': True, 'data': contenido})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== RUTAS API DE INFORMES =====

@app.route('/api/informes/<int:id>', methods=['GET'])
def api_obtener_informe_por_id(id):
    """Obtener un informe específico por ID"""
    try:
        from informes import obtener_informe_por_id
        informe = obtener_informe_por_id(id)
        if informe:
            return jsonify({'success': True, 'data': informe})
        else:
            return jsonify({'success': False, 'error': 'Informe no encontrado'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes', methods=['GET'])
def api_obtener_informes():
    """Obtener todos los informes"""
    try:
        informes = obtener_informes()
        return jsonify({'success': True, 'data': informes})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes', methods=['POST'])
def api_crear_informe():
    """Crear nuevo informe"""
    try:
        data = request.get_json()
        titulo = data.get('titulo')
        descripcion = data.get('descripcion')
        consultas = data.get('consultas', [])
        formato = data.get('formato', 'json')
        
        if not titulo:
            return jsonify({'success': False, 'error': 'Título requerido'}), 400
        
        informe = crear_informe(titulo, descripcion, consultas, formato)
        return jsonify({'success': True, 'data': informe})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/<int:id>', methods=['DELETE'])
def api_eliminar_informe(id):
    """Eliminar informe"""
    try:
        resultado = eliminar_informe(id)
        return jsonify({'success': True, 'message': 'Informe eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/<int:id>/generar', methods=['POST'])
def api_generar_informe(id):
    """Generar contenido del informe"""
    try:
        contenido = generar_informe(id)
        return jsonify({'success': True, 'data': contenido})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/<int:id>/descargar', methods=['POST'])
def api_descargar_informe(id):
    """Descargar informe en formato específico"""
    try:
        data = request.get_json()
        formato = data.get('formato', 'json')
        
        datos_descarga = descargar_informe(id, formato)
        
        if formato.lower() == 'csv':
            # Devolver como archivo descargable
            buffer = BytesIO(datos_descarga['contenido'].encode('utf-8'))
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name=datos_descarga['nombre_archivo'],
                mimetype='text/csv'
            )
        else:
            return jsonify({'success': True, 'data': datos_descarga})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/<int:id>/compartir', methods=['POST'])
def api_compartir_informe(id):
    """Compartir informe por email"""
    try:
        data = request.get_json()
        destinatarios = data.get('destinatarios', [])
        asunto = data.get('asunto')
        
        if not destinatarios:
            return jsonify({'success': False, 'error': 'Destinatarios requeridos'}), 400
        
        datos_email = compartir_informe(id, destinatarios, asunto)
        resultado = enviar_por_correo(datos_email)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/predicadores', methods=['POST'])
def api_generar_informe_predicadores():
    """Generar informe específico de predicadores"""
    try:
        data = request.get_json()
        filtros = data.get('filtros', {})
        
        informe = generar_informe_predicadores(filtros)
        return jsonify({'success': True, 'data': informe})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/finanzas', methods=['POST'])
def api_generar_informe_finanzas():
    """Generar informe financiero"""
    try:
        data = request.get_json()
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        informe = generar_informe_finanzas(fecha_inicio, fecha_fin)
        return jsonify({'success': True, 'data': informe})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/asistencias', methods=['POST'])
def api_generar_informe_asistencias():
    """Generar informe de asistencias"""
    try:
        data = request.get_json()
        fecha_inicio = data.get('fecha_inicio')
        fecha_fin = data.get('fecha_fin')
        
        informe = generar_informe_asistencias(fecha_inicio, fecha_fin)
        return jsonify({'success': True, 'data': informe})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/generar', methods=['POST'])
def api_generar_informe_dinamico():
    """Generar informe dinámico basado en parámetros"""
    try:
        data = request.get_json()
        tipo = data.get('tipo')
        periodo = data.get('periodo')
        fecha_inicio = data.get('fechaInicio')
        fecha_fin = data.get('fechaFin')
        filtros = data.get('filtros', {})
        formato = data.get('formato', 'pdf')
        
        # Generar informe según el tipo
        if tipo == 'resumen':
            informe = generar_informe_resumen_general(filtros)
        elif tipo == 'financiero':
            informe = generar_informe_finanzas(fecha_inicio, fecha_fin)
        elif tipo == 'asistencias':
            informe = generar_informe_asistencias(fecha_inicio, fecha_fin)
        elif tipo == 'actividades':
            informe = generar_informe_actividades(fecha_inicio, fecha_fin)
        else:
            return jsonify({'success': False, 'error': 'Tipo de informe no válido'}), 400
        
        # Agregar metadatos
        informe['tipo'] = tipo
        informe['formato'] = formato
        informe['fecha_generacion'] = datetime.now().isoformat()
        
        return jsonify({'success': True, 'data': informe})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/previa', methods=['POST'])
def api_vista_previa_informe():
    """Generar vista previa del informe"""
    try:
        data = request.get_json()
        tipo = data.get('tipo')
        periodo = data.get('periodo')
        fecha_inicio = data.get('fechaInicio')
        fecha_fin = data.get('fechaFin')
        filtros = data.get('filtros', {})
        
        # Generar vista previa (datos limitados)
        if tipo == 'resumen':
            informe = generar_informe_resumen_general(filtros, limite=10)
        elif tipo == 'financiero':
            informe = generar_informe_finanzas(fecha_inicio, fecha_fin, limite=10)
        elif tipo == 'asistencias':
            informe = generar_informe_asistencias(fecha_inicio, fecha_fin, limite=10)
        elif tipo == 'actividades':
            informe = generar_informe_actividades(fecha_inicio, fecha_fin, limite=10)
        else:
            return jsonify({'success': False, 'error': 'Tipo de informe no válido'}), 400
        
        informe['tipo'] = tipo
        informe['es_previa'] = True
        
        return jsonify({'success': True, 'data': informe})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/descargar/<int:id>', methods=['GET'])
def api_descargar_informe_get(id):
    """Descargar informe por GET (para compatibilidad con JavaScript)"""
    try:
        formato = request.args.get('formato', 'pdf')
        
        datos_descarga = descargar_informe(id, formato)
        
        if formato.lower() == 'csv':
            buffer = BytesIO(datos_descarga['contenido'].encode('utf-8'))
            buffer.seek(0)
            return send_file(
                buffer,
                as_attachment=True,
                download_name=datos_descarga['nombre_archivo'],
                mimetype='text/csv'
            )
        elif formato.lower() == 'excel':
            # Aquí se implementaría la generación de Excel
            return jsonify({'success': True, 'data': datos_descarga})
        else:
            return jsonify({'success': True, 'data': datos_descarga})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/informes/enviar-email', methods=['POST'])
def api_enviar_informe_email():
    """Enviar informe por email"""
    try:
        data = request.get_json()
        id_informe = data.get('idInforme')
        destinatario = data.get('destinatario')
        
        if not id_informe or not destinatario:
            return jsonify({'success': False, 'error': 'ID de informe y destinatario requeridos'}), 400
        
        datos_email = compartir_informe(id_informe, [destinatario])
        resultado = enviar_por_correo(datos_email)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== RUTAS API DE EMAIL =====

@app.route('/api/email/enviar', methods=['POST'])
def api_enviar_email():
    """Enviar email"""
    try:
        data = request.get_json()
        resultado = enviar_por_correo(data)
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/email/verificar', methods=['GET'])
def api_verificar_email():
    """Verificar configuración de email"""
    try:
        resultado = verificar_configuracion_email()
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== RUTAS API DE ADMINISTRADORES =====

@app.route('/api/admin/admins', methods=['GET'])
def api_obtener_admins():
    """Obtener lista de administradores"""
    try:
        admins = obtener_admins()
        return jsonify({'success': True, 'data': admins})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/admins', methods=['POST'])
def api_agregar_admin():
    """Agregar administrador"""
    try:
        data = request.get_json()
        nombre = data.get('nombre')
        rol = data.get('rol')
        codigo = data.get('codigo')
        
        if not all([nombre, rol, codigo]):
            return jsonify({'success': False, 'error': 'Todos los campos son requeridos'}), 400
        
        resultado = agregar_admin(nombre, rol, codigo)
        return jsonify({'success': True, 'message': 'Administrador agregado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/admin/admins/<nombre>', methods=['DELETE'])
def api_eliminar_admin(nombre):
    """Eliminar administrador"""
    try:
        resultado = eliminar_admin(nombre)
        return jsonify({'success': True, 'message': 'Administrador eliminado'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ===== MANEJADORES DE ERRORES =====

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Ruta no encontrada'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({'success': False, 'error': 'Método no permitido'}), 405

if __name__ == '__main__':
    # Configuración para desarrollo y producción
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"🚀 Iniciando servidor Flask en puerto {port}")
    print(f"📧 Email configurado: {'✅' if app.config['GMAIL_PASS'] else '❌'}")
    print(f"🗄️  Supabase configurado: {'✅' if app.config['SUPABASE_URL'] and app.config['SUPABASE_KEY'] else '❌'}")
    
    app.run(host='0.0.0.0', port=port, debug=debug) 