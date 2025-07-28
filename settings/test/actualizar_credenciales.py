#!/usr/bin/env python3
"""
Script para actualizar credenciales de forma segura
"""

import os
import sys
import bcrypt
from supabase import create_client, Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración Supabase
supabase_url = os.environ.get('SUPABASE_URL')
supabase_key = os.environ.get('SUPABASE_KEY')
supabase: Client = create_client(supabase_url, supabase_key)

def hash_password(password):
    """Generar hash seguro de contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def actualizar_credenciales():
    """Actualizar credenciales del administrador principal"""
    
    print("🔐 Actualizando credenciales de forma segura")
    print("=" * 50)
    
    try:
        # Buscar administrador principal
        response = supabase.table('administradores').select('*').eq('nombre', 'Administrador Principal').execute()
        
        if not response.data:
            print("❌ No se encontró el administrador principal")
            return False
        
        admin = response.data[0]
        print(f"📋 Administrador encontrado:")
        print(f"   - Nombre: {admin['nombre']}")
        print(f"   - Código actual: {admin['codigo']}")
        print(f"   - Estado: {admin['estado']}")
        
        # Generar nuevo hash seguro
        codigo_actual = "123456"  # Código actual en texto plano
        nuevo_hash = hash_password(codigo_actual)
        
        print(f"\n🔧 Actualizando código...")
        print(f"   - Código actual (texto plano): {codigo_actual}")
        print(f"   - Nuevo hash (bcrypt): {nuevo_hash[:20]}...")
        
        # Actualizar en la base de datos
        update_response = supabase.table('administradores').update({
            'codigo': nuevo_hash
        }).eq('nombre', 'Administrador Principal').execute()
        
        if update_response.data:
            print(f"✅ Credenciales actualizadas exitosamente")
            print(f"   - Usuario: Administrador Principal")
            print(f"   - Código: 123456")
            print(f"   - Hash: {nuevo_hash[:20]}...")
            return True
        else:
            print(f"❌ Error al actualizar credenciales")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def verificar_credenciales():
    """Verificar que las credenciales funcionan correctamente"""
    
    print(f"\n🧪 Verificando credenciales actualizadas")
    print("=" * 50)
    
    try:
        # Importar funciones de sesión
        sys.path.append('../../')
        from sesion import is_admin_by_name, get_admin_role
        
        # Probar autenticación
        nombre = "Administrador Principal"
        codigo = "123456"
        
        es_admin = is_admin_by_name(nombre, codigo)
        rol = get_admin_role(nombre)
        
        print(f"📋 Resultados:")
        print(f"   - Nombre: {nombre}")
        print(f"   - Código: {codigo}")
        print(f"   - Es admin: {es_admin}")
        print(f"   - Rol: {rol}")
        
        if es_admin:
            print(f"✅ ¡CREDENCIALES FUNCIONANDO CORRECTAMENTE!")
            return True
        else:
            print(f"❌ Las credenciales no funcionan")
            return False
            
    except Exception as e:
        print(f"❌ Error al verificar: {str(e)}")
        return False

def main():
    print("🚀 Actualización Segura de Credenciales")
    print("=" * 60)
    
    # Actualizar credenciales
    if actualizar_credenciales():
        # Verificar que funcionan
        if verificar_credenciales():
            print(f"\n🎉 ¡ACTUALIZACIÓN COMPLETADA EXITOSAMENTE!")
            print(f"   - Credenciales actualizadas con bcrypt")
            print(f"   - Sistema de autenticación seguro")
            print(f"   - Listo para usar en producción")
        else:
            print(f"\n⚠️  Credenciales actualizadas pero no funcionan")
    else:
        print(f"\n❌ Error en la actualización")

if __name__ == "__main__":
    main() 