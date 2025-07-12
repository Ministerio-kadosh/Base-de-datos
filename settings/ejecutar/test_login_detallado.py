#!/usr/bin/env python3
"""
Script para diagnosticar problemas de login
Verifica la configuración de la base de datos y las credenciales
"""

import os
import sys
import hashlib
from supabase.client import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Agregar el directorio padre al path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# Configuración Supabase
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')

if not supabase_url or not supabase_key:
    print("❌ ERROR: Variables de entorno SUPABASE_URL y SUPABASE_KEY no configuradas")
    print("Configura estas variables en tu entorno o en Render")
    sys.exit(1)

print(f"🔗 Conectando a Supabase: {supabase_url}")
supabase: Client = create_client(supabase_url, supabase_key)

def test_connection():
    """Probar conexión a Supabase"""
    try:
        print("\n🔍 Probando conexión a Supabase...")
        response = supabase.table('administradores').select('count').execute()
        print("✅ Conexión exitosa")
        return True
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return False

def check_table_structure():
    """Verificar estructura de la tabla administradores"""
    try:
        print("\n📋 Verificando estructura de tabla 'administradores'...")
        response = supabase.table('administradores').select('*').limit(1).execute()
        
        if response.data:
            print("✅ Tabla 'administradores' existe")
            print(f"📊 Columnas disponibles: {list(response.data[0].keys())}")
            return response.data[0].keys()
        else:
            print("⚠️  Tabla 'administradores' existe pero está vacía")
            return []
    except Exception as e:
        print(f"❌ Error al verificar tabla: {e}")
        return []

def check_admin_data():
    """Verificar datos de administradores"""
    try:
        print("\n👥 Verificando datos de administradores...")
        response = supabase.table('administradores').select('*').execute()
        
        if response.data:
            print(f"✅ Encontrados {len(response.data)} administradores:")
            for admin in response.data:
                print(f"   - Nombre: '{admin.get('nombre', 'N/A')}'")
                print(f"     Código: '{admin.get('codigo', 'N/A')}' (longitud: {len(str(admin.get('codigo', '')))})")
                print(f"     Estado: '{admin.get('estado', 'N/A')}'")
                print(f"     Rol: '{admin.get('rol', 'N/A')}'")
                print()
        else:
            print("⚠️  No hay administradores en la base de datos")
        return response.data
    except Exception as e:
        print(f"❌ Error al obtener administradores: {e}")
        return []

def test_login_methods():
    """Probar diferentes métodos de login"""
    print("\n🔐 Probando métodos de login...")
    
    # Credenciales de prueba
    nombre = "Administrador Principal"
    codigo = "123456"
    
    print(f"   Usando credenciales: '{nombre}' / '{codigo}'")
    
    # Método 1: Comparación directa (como en is_admin_by_name)
    try:
        print("\n   🔍 Método 1: Comparación directa (is_admin_by_name)")
        response = supabase.table('administradores').select('*').eq('nombre', nombre).eq('codigo', codigo).eq('estado', 'Activo').execute()
        print(f"   Resultado: {len(response.data)} registros encontrados")
        if response.data:
            print(f"   ✅ Login exitoso con comparación directa")
            return True
        else:
            print(f"   ❌ Login falló con comparación directa")
    except Exception as e:
        print(f"   ❌ Error en método 1: {e}")
    
    # Método 2: Comparación con código encriptado
    try:
        print("\n   🔍 Método 2: Comparación con código encriptado")
        codigo_encriptado = hashlib.sha256(codigo.encode()).hexdigest()
        print(f"   Código encriptado: {codigo_encriptado}")
        response = supabase.table('administradores').select('*').eq('nombre', nombre).eq('codigo', codigo_encriptado).eq('estado', 'Activo').execute()
        print(f"   Resultado: {len(response.data)} registros encontrados")
        if response.data:
            print(f"   ✅ Login exitoso con código encriptado")
            return True
        else:
            print(f"   ❌ Login falló con código encriptado")
    except Exception as e:
        print(f"   ❌ Error en método 2: {e}")
    
    # Método 3: Solo por nombre
    try:
        print("\n   🔍 Método 3: Solo por nombre")
        response = supabase.table('administradores').select('*').eq('nombre', nombre).execute()
        print(f"   Resultado: {len(response.data)} registros encontrados")
        if response.data:
            admin = response.data[0]
            print(f"   Código almacenado: '{admin.get('codigo', 'N/A')}'")
            print(f"   Estado: '{admin.get('estado', 'N/A')}'")
        else:
            print(f"   ❌ No se encontró administrador con ese nombre")
    except Exception as e:
        print(f"   ❌ Error en método 3: {e}")
    
    return False

def create_test_admin():
    """Crear un administrador de prueba"""
    try:
        print("\n🔧 Creando administrador de prueba...")
        
        # Verificar si ya existe
        response = supabase.table('administradores').select('*').eq('nombre', 'Test Admin').execute()
        if response.data:
            print("   ⚠️  Ya existe un administrador de prueba")
            return
        
        # Crear administrador con código en texto plano
        admin_data = {
            'nombre': 'Test Admin',
            'codigo': '123456',
            'rol': 'Super Admin',
            'estado': 'Activo',
            'fecha_creacion': '2024-01-01T00:00:00'
        }
        
        response = supabase.table('administradores').insert(admin_data).execute()
        if response.data:
            print("   ✅ Administrador de prueba creado exitosamente")
        else:
            print("   ❌ Error al crear administrador de prueba")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def main():
    """Función principal"""
    print("🚀 DIAGNÓSTICO DE LOGIN - SISTEMA DE GESTIÓN")
    print("=" * 50)
    
    # Probar conexión
    if not test_connection():
        return
    
    # Verificar estructura
    columns = check_table_structure()
    
    # Verificar datos
    admins = check_admin_data()
    
    # Probar métodos de login
    login_success = test_login_methods()
    
    # Si no hay éxito, crear admin de prueba
    if not login_success and not admins:
        print("\n🛠️  No se encontraron administradores válidos")
        create_test_admin()
        print("\n🔄 Probando login nuevamente...")
        test_login_methods()
    
    print("\n" + "=" * 50)
    print("📋 RESUMEN:")
    print("1. Verifica que las variables de entorno estén configuradas en Render")
    print("2. Asegúrate de que la tabla 'administradores' tenga datos")
    print("3. Los códigos deben estar en texto plano (no encriptados)")
    print("4. El estado debe ser 'Activo'")
    print("\n🔑 Credenciales de prueba: 'Administrador Principal' / '123456'")

if __name__ == "__main__":
    main() 