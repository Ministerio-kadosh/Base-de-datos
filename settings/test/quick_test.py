#!/usr/bin/env python3
"""
Script de prueba rápida para verificar las mejoras implementadas
"""

import os
import sys
from supabase import create_client, Client
from dotenv import load_dotenv
import bcrypt

# Cargar variables de entorno
load_dotenv()

def test_bcrypt():
    """Probar funcionalidad de bcrypt"""
    print("🔍 Probando bcrypt...")
    try:
        password = "123456"
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        is_valid = bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        
        if is_valid:
            print("   ✅ bcrypt funcionando correctamente")
            return True
        else:
            print("   ❌ bcrypt no funciona")
            return False
    except Exception as e:
        print(f"   ❌ Error en bcrypt: {e}")
        return False

def test_supabase_connection():
    """Probar conexión a Supabase"""
    print("\n🔍 Probando conexión a Supabase...")
    try:
        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("   ❌ Variables de entorno no configuradas")
            return False
        
        supabase: Client = create_client(supabase_url, supabase_key)
        response = supabase.table('administradores').select('*').limit(1).execute()
        print("   ✅ Conexión a Supabase exitosa")
        return True
    except Exception as e:
        print(f"   ❌ Error de conexión: {e}")
        return False

def test_imports():
    """Probar imports de las nuevas dependencias"""
    print("\n🔍 Probando imports...")
    try:
        import bcrypt
        print("   ✅ bcrypt importado correctamente")
        
        # Intentar importar flask-limiter (solo si está instalado)
        try:
            from flask_limiter import Limiter
            print("   ✅ flask-limiter disponible")
        except ImportError:
            print("   ⚠️  flask-limiter no instalado (se instalará con requirements.txt)")
        
        # Intentar importar flask-jwt-extended (solo si está instalado)
        try:
            from flask_jwt_extended import JWTManager
            print("   ✅ flask-jwt-extended disponible")
        except ImportError:
            print("   ⚠️  flask-jwt-extended no instalado (se instalará con requirements.txt)")
        
        return True
    except Exception as e:
        print(f"   ❌ Error en imports: {e}")
        return False

def main():
    print("🧪 PRUEBA RÁPIDA DE MEJORAS")
    print("=" * 50)
    
    # Probar imports
    imports_ok = test_imports()
    
    # Probar bcrypt
    bcrypt_ok = test_bcrypt()
    
    # Probar Supabase
    supabase_ok = test_supabase_connection()
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN:")
    print(f"   Imports: {'✅ OK' if imports_ok else '❌ FALLO'}")
    print(f"   bcrypt: {'✅ OK' if bcrypt_ok else '❌ FALLO'}")
    print(f"   Supabase: {'✅ OK' if supabase_ok else '❌ FALLO'}")
    
    if imports_ok and bcrypt_ok and supabase_ok:
        print("\n🎉 ¡Todas las mejoras están funcionando correctamente!")
    else:
        print("\n⚠️  Algunas mejoras necesitan atención")

if __name__ == "__main__":
    main() 