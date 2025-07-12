import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
from datetime import datetime
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enviar_por_correo(datos):
    """Enviar email - convertido de MailApp.sendEmail() a SMTP Python"""
    try:
        # Configuración de email
        gmail_user = os.environ.get('GMAIL_USER', 'tu_email@gmail.com')
        gmail_password = os.environ.get('GMAIL_PASS')
        
        if not gmail_password:
            raise ValueError('Contraseña de Gmail no configurada')
        
        # Extraer datos del email
        destinatarios = datos.get('destinatarios', [])
        asunto = datos.get('asunto', 'Informe del Sistema de Gestión')
        contenido = datos.get('contenido', '')
        descripcion = datos.get('descripcion', '')
        
        if not destinatarios:
            raise ValueError('No se especificaron destinatarios')
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = ', '.join(destinatarios) if isinstance(destinatarios, list) else destinatarios
        msg['Subject'] = asunto
        
        # Crear cuerpo del email
        cuerpo_email = f"""
        <html>
        <body>
            <h2>{asunto}</h2>
            <p><strong>Descripción:</strong> {descripcion}</p>
            <p><strong>Fecha de envío:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <h3>Contenido del Informe:</h3>
            <pre style="background-color: #f4f4f4; padding: 10px; border-radius: 5px; overflow-x: auto;">
{contenido}
            </pre>
            <hr>
            <p><em>Este email fue generado automáticamente por el Sistema de Gestión.</em></p>
        </body>
        </html>
        """
        
        # Adjuntar cuerpo HTML
        msg.attach(MIMEText(cuerpo_email, 'html'))
        
        # Configurar conexión SMTP
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(gmail_user, gmail_password)
            
            # Enviar email
            texto = msg.as_string()
            server.sendmail(gmail_user, destinatarios, texto)
        
        logger.info(f'Email enviado exitosamente a {destinatarios}')
        return {
            'success': True,
            'mensaje': 'Email enviado exitosamente',
            'destinatarios': destinatarios,
            'fecha_envio': datetime.now().isoformat()
        }
        
    except Exception as error:
        logger.error(f'Error al enviar email: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error al enviar email: {str(error)}',
            'error': str(error)
        }

def enviar_informe_por_correo(id_informe, destinatarios, asunto=None):
    """Enviar informe específico por correo"""
    try:
        from informes import generar_informe
        
        # Generar contenido del informe
        contenido = generar_informe(id_informe)
        
        # Preparar datos para envío
        datos_email = {
            'destinatarios': destinatarios,
            'asunto': asunto or f'Informe del Sistema de Gestión - {datetime.now().strftime("%Y-%m-%d")}',
            'contenido': contenido,
            'descripcion': 'Informe generado automáticamente por el sistema'
        }
        
        # Enviar email
        return enviar_por_correo(datos_email)
        
    except Exception as error:
        logger.error(f'Error al enviar informe por correo: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error al enviar informe: {str(error)}',
            'error': str(error)
        }

def enviar_notificacion(destinatarios, titulo, mensaje, tipo='info'):
    """Enviar notificación por correo"""
    try:
        # Preparar datos para envío
        datos_email = {
            'destinatarios': destinatarios,
            'asunto': f'Notificación: {titulo}',
            'contenido': mensaje,
            'descripcion': f'Notificación del sistema - Tipo: {tipo}'
        }
        
        # Enviar email
        return enviar_por_correo(datos_email)
        
    except Exception as error:
        logger.error(f'Error al enviar notificación: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error al enviar notificación: {str(error)}',
            'error': str(error)
        }

def enviar_email_con_adjunto(destinatarios, asunto, contenido, archivo_adjunto=None, nombre_archivo=None):
    """Enviar email con archivo adjunto"""
    try:
        # Configuración de email
        gmail_user = os.environ.get('GMAIL_USER', 'tu_email@gmail.com')
        gmail_password = os.environ.get('GMAIL_PASS')
        
        if not gmail_password:
            raise ValueError('Contraseña de Gmail no configurada')
        
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = gmail_user
        msg['To'] = ', '.join(destinatarios) if isinstance(destinatarios, list) else destinatarios
        msg['Subject'] = asunto
        
        # Cuerpo del email
        cuerpo_email = f"""
        <html>
        <body>
            <h2>{asunto}</h2>
            <p><strong>Fecha de envío:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <div>
                {contenido}
            </div>
            <hr>
            <p><em>Este email fue generado automáticamente por el Sistema de Gestión.</em></p>
        </body>
        </html>
        """
        
        msg.attach(MIMEText(cuerpo_email, 'html'))
        
        # Adjuntar archivo si se proporciona
        if archivo_adjunto and nombre_archivo:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(archivo_adjunto)
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {nombre_archivo}'
            )
            msg.attach(part)
        
        # Configurar conexión SMTP
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(gmail_user, gmail_password)
            
            # Enviar email
            texto = msg.as_string()
            server.sendmail(gmail_user, destinatarios, texto)
        
        logger.info(f'Email con adjunto enviado exitosamente a {destinatarios}')
        return {
            'success': True,
            'mensaje': 'Email con adjunto enviado exitosamente',
            'destinatarios': destinatarios,
            'archivo_adjunto': nombre_archivo,
            'fecha_envio': datetime.now().isoformat()
        }
        
    except Exception as error:
        logger.error(f'Error al enviar email con adjunto: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error al enviar email con adjunto: {str(error)}',
            'error': str(error)
        }

def enviar_informe_csv_por_correo(id_informe, destinatarios, asunto=None):
    """Enviar informe en formato CSV por correo"""
    try:
        from informes import generar_informe, descargar_informe
        
        # Generar informe en formato CSV
        datos_descarga = descargar_informe(id_informe, 'csv')
        
        # Preparar contenido del email
        contenido = f"""
        <h3>Informe CSV Generado</h3>
        <p>Se adjunta el informe en formato CSV.</p>
        <p><strong>Nombre del archivo:</strong> {datos_descarga['nombre_archivo']}</p>
        <p><strong>Fecha de generación:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        """
        
        # Enviar email con adjunto
        return enviar_email_con_adjunto(
            destinatarios=destinatarios,
            asunto=asunto or f'Informe CSV - {datetime.now().strftime("%Y-%m-%d")}',
            contenido=contenido,
            archivo_adjunto=datos_descarga['contenido'].encode('utf-8'),
            nombre_archivo=datos_descarga['nombre_archivo']
        )
        
    except Exception as error:
        logger.error(f'Error al enviar informe CSV por correo: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error al enviar informe CSV: {str(error)}',
            'error': str(error)
        }

def verificar_configuracion_email():
    """Verificar que la configuración de email esté correcta"""
    try:
        gmail_user = os.environ.get('GMAIL_USER')
        gmail_password = os.environ.get('GMAIL_PASS')
        
        if not gmail_user or not gmail_password:
            return {
                'success': False,
                'mensaje': 'Configuración de email incompleta',
                'detalles': {
                    'gmail_user': bool(gmail_user),
                    'gmail_password': bool(gmail_password)
                }
            }
        
        # Probar conexión SMTP
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(gmail_user, gmail_password)
        
        return {
            'success': True,
            'mensaje': 'Configuración de email correcta',
            'gmail_user': gmail_user
        }
        
    except Exception as error:
        logger.error(f'Error al verificar configuración de email: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error en configuración de email: {str(error)}',
            'error': str(error)
        }

def enviar_email_masivo(destinatarios, asunto, contenido, intervalo=1):
    """Enviar emails masivos con intervalo entre envíos"""
    try:
        resultados = []
        
        for i, destinatario in enumerate(destinatarios):
            try:
                # Enviar email individual
                resultado = enviar_por_correo({
                    'destinatarios': [destinatario],
                    'asunto': asunto,
                    'contenido': contenido,
                    'descripcion': 'Email masivo del sistema'
                })
                
                resultados.append({
                    'destinatario': destinatario,
                    'exitoso': resultado['success'],
                    'mensaje': resultado.get('mensaje', '')
                })
                
                # Esperar intervalo entre envíos (excepto el último)
                if i < len(destinatarios) - 1:
                    import time
                    time.sleep(interval)
                
            except Exception as e:
                resultados.append({
                    'destinatario': destinatario,
                    'exitoso': False,
                    'mensaje': str(e)
                })
        
        # Resumen
        exitosos = sum(1 for r in resultados if r['exitoso'])
        fallidos = len(resultados) - exitosos
        
        return {
            'success': True,
            'mensaje': f'Envío masivo completado: {exitosos} exitosos, {fallidos} fallidos',
            'total_enviados': len(destinatarios),
            'exitosos': exitosos,
            'fallidos': fallidos,
            'detalles': resultados
        }
        
    except Exception as error:
        logger.error(f'Error en envío masivo: {str(error)}')
        return {
            'success': False,
            'mensaje': f'Error en envío masivo: {str(error)}',
            'error': str(error)
        }
