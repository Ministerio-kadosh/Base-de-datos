#!/usr/bin/env python3
"""
Script de prueba para verificar la conexión con Supabase
y las operaciones básicas del sistema de gestión Flask
"""

import os
import sys
from datetime import datetime
from supabase import create_client, Client

def test_supabase_connection():
    """Probar conexión básica con Supabase"""
    print("🔍 Probando conexión con Supabase...")
    
    # Verificar variables de entorno
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        print("❌ Error: Variables de entorno SUPABASE_URL y SUPABASE_KEY no configuradas")
        print("   Configura las variables de entorno o crea un archivo .env")
        return False
    
    try:
        # Crear cliente Supabase
        supabase: Client = create_client(supabase_url, supabase_key)
        print("✅ Cliente Supabase creado exitosamente")
        
        # Probar conexión básica
        response = supabase.table('Administradores').select('count').execute()
        print("✅ Conexión con Supabase establecida correctamente")
        
        return True, supabase
        
    except Exception as e:
        print(f"❌ Error al conectar con Supabase: {str(e)}")
        return False, None

def test_table_operations(supabase: Client):
    """Probar operaciones básicas en las tablas"""
    print("\n🔍 Probando operaciones en tablas...")
    
    # Lista de tablas a probar
    tables = [
        'Administradores',
        'Predicadores', 
        'Reuniones',
        'Calendario',
        'Bandeja',
        'Asistencias',
        'Jovenes',
        'Finanzas',
        'Historial_Cambios',
        'Informes'
    ]
    
    for table in tables:
        try:
            # Probar SELECT básico
            response = supabase.table(table).select('*').limit(1).execute()
            print(f"✅ Tabla '{table}': Acceso correcto")
            
        except Exception as e:
            print(f"❌ Tabla '{table}': Error - {str(e)}")

def test_admin_operations(supabase: Client):
    """Probar operaciones específicas de administradores"""
    print("\n🔍 Probando operaciones de administradores...")
    
    try:
        # Verificar si existe el admin inicial
        response = supabase.table('Administradores').select('*').eq('email', 'admin@sistema.com').execute()
        
        if response.data:
            print("✅ Administrador inicial encontrado")
            admin = response.data[0]
            print(f"   - Email: {admin['email']}")
            print(f"   - Nombre: {admin['nombre']}")
            print(f"   - Rol: {admin['rol']}")
        else:
            print("⚠️  Administrador inicial no encontrado")
            print("   Ejecuta el script SQL para crear los datos iniciales")
            
    except Exception as e:
        print(f"❌ Error al verificar administradores: {str(e)}")

def test_predicadores_operations(supabase: Client):
    """Probar operaciones de predicadores"""
    print("\n🔍 Probando operaciones de predicadores...")
    
    try:
        # Obtener predicadores
        response = supabase.table('Predicadores').select('*').execute()
        print(f"✅ Predicadores encontrados: {len(response.data)}")
        
        if response.data:
            for predicador in response.data[:3]:  # Mostrar solo los primeros 3
                print(f"   - {predicador['Nombre']} {predicador['Apellido']}")
                
    except Exception as e:
        print(f"❌ Error al obtener predicadores: {str(e)}")

def test_insert_operation(supabase: Client):
    """Probar operación de inserción"""
    print("\n🔍 Probando operación de inserción...")
    
    try:
        # Datos de prueba
        test_data = {
            'Objetivo': 'Prueba de conexión',
            'Descripcion': 'Esta es una tarea de prueba para verificar la conexión con Supabase',
            'prioridad': 'baja',
            'estado': 'creado',
            'fecha': datetime.now().isoformat(),
            'usuario': 'sistema'
        }
        
        # Insertar en Bandeja
        response = supabase.table('Bandeja').insert(test_data).execute()
        
        if response.data:
            print("✅ Inserción exitosa")
            print(f"   - ID creado: {response.data[0]['id']}")
            
            # Limpiar - eliminar el registro de prueba
            supabase.table('Bandeja').delete().eq('id', response.data[0]['id']).execute()
            print("✅ Registro de prueba eliminado")
        else:
            print("❌ Error en la inserción")
            
    except Exception as e:
        print(f"❌ Error en operación de inserción: {str(e)}")

def test_views(supabase: Client):
    """Probar vistas de la base de datos"""
    print("\n🔍 Probando vistas...")
    
    try:
        # Probar vista de estadísticas generales
        response = supabase.table('Estadisticas_Generales').select('*').execute()
        if response.data:
            stats = response.data[0]
            print("✅ Vista Estadisticas_Generales:")
            print(f"   - Total predicadores: {stats.get('total_predicadores', 0)}")
            print(f"   - Total reuniones: {stats.get('total_reuniones', 0)}")
            print(f"   - Total jóvenes: {stats.get('total_jovenes', 0)}")
            print(f"   - Tareas pendientes: {stats.get('tareas_pendientes', 0)}")
        else:
            print("⚠️  Vista Estadisticas_Generales no disponible")
            
    except Exception as e:
        print(f"❌ Error al probar vistas: {str(e)}")

def main():
    """Función principal de pruebas"""
    print("=" * 60)
    print("🧪 PRUEBAS DE CONEXIÓN SUPABASE")
    print("=" * 60)
    
    # Cargar variables de entorno desde .env si existe
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Variables de entorno cargadas desde .env")
    except ImportError:
        print("⚠️  python-dotenv no instalado, usando variables del sistema")
    except Exception as e:
        print(f"⚠️  Error al cargar .env: {str(e)}")
    
    # Probar conexión
    success, supabase = test_supabase_connection()
    
    if not success:
        print("\n❌ No se pudo establecer conexión con Supabase")
        print("   Verifica:")
        print("   1. Las variables de entorno SUPABASE_URL y SUPABASE_KEY")
        print("   2. Que el proyecto de Supabase esté activo")
        print("   3. Que las credenciales sean correctas")
        return
    
    # Ejecutar pruebas
    test_table_operations(supabase)
    test_admin_operations(supabase)
    test_predicadores_operations(supabase)
    test_insert_operation(supabase)
    test_views(supabase)
    
    print("\n" + "=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 60)
    print("Si todas las pruebas pasaron, tu configuración está correcta.")
    print("Puedes ejecutar tu aplicación Flask con: python app.py")

if __name__ == "__main__":
    main() 