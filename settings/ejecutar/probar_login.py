#!/usr/bin/env python3
"""
Script para probar el login con las credenciales reales
"""

import os
import sys
import hashlib
from supabase import create_client, Client

# Configuración Supabase
supabase_url = 'https://vztpbpontffuawntmixp.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6dHBicG9udGZmdWF3bnRtaXhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE1MTMwOTQsImV4cCI6MjA2NzA4OTA5NH0.6CbDGLtfr493dJFXRNPczMW2oGms9JOO7QLAsgakdvs'

supabase: Client = create_client(supabase_url, supabase_key)

def probar_login():
    """Probar el login con las credenciales de la base de datos"""
    
    print("🔐 Probando login con credenciales reales")
    print("=" * 50)
    
    try:
        # Obtener administradores de la base de datos
        response = supabase.table('administradores').select('*').execute()
        
        if response.data:
            admin = response.data[0]
            print(f"📋 Administrador encontrado:")
            print(f"   - Nombre: {admin['nombre']}")
            print(f"   - Código (encriptado): {admin['codigo']}")
            print(f"   - Estado: {admin['estado']}")
            
            # Probar diferentes códigos
            codigos_a_probar = ['123456', '123456789', 'admin', 'password', '1234']
            
            print(f"\n🔍 Probando códigos de acceso:")
            for codigo in codigos_a_probar:
                # Encriptar el código para comparar
                codigo_encriptado = hashlib.sha256(codigo.encode()).hexdigest()
                
                if codigo_encriptado == admin['codigo']:
                    print(f"✅ ¡CÓDIGO ENCONTRADO! '{codigo}' funciona")
                    print(f"   - Nombre: {admin['nombre']}")
                    print(f"   - Código: {codigo}")
                    return admin['nombre'], codigo
                else:
                    print(f"❌ Código '{codigo}' no coincide")
            
            print(f"\n⚠️  No se encontró el código correcto")
            print(f"   Código encriptado en BD: {admin['codigo']}")
            return None, None
            
        else:
            print("❌ No se encontraron administradores")
            return None, None
            
    except Exception as e:
        print(f"❌ Error al probar login: {str(e)}")
        return None, None

def probar_funcion_login(nombre, codigo):
    """Probar la función de login del sistema"""
    
    print(f"\n🧪 Probando función de login del sistema")
    print("=" * 50)
    
    try:
        # Importar las funciones de sesión
        from sesion import is_admin_by_name, get_admin_role
        
        # Probar autenticación
        es_admin = is_admin_by_name(nombre, codigo)
        rol = get_admin_role(nombre)
        
        print(f"📋 Resultados:")
        print(f"   - Nombre: {nombre}")
        print(f"   - Código: {codigo}")
        print(f"   - Es admin: {es_admin}")
        print(f"   - Rol: {rol}")
        
        if es_admin:
            print(f"✅ ¡LOGIN EXITOSO!")
            return True
        else:
            print(f"❌ Login falló")
            return False
            
    except Exception as e:
        print(f"❌ Error en función de login: {str(e)}")
        return False

def main():
    print("🚀 Prueba de Login del Sistema")
    print("=" * 60)
    
    # Probar login con credenciales reales
    nombre, codigo = probar_login()
    
    if nombre and codigo:
        # Probar función de login del sistema
        exito = probar_funcion_login(nombre, codigo)
        
        if exito:
            print(f"\n🎉 ¡SISTEMA LISTO!")
            print(f"   Puedes usar estas credenciales para hacer login:")
            print(f"   - Nombre: {nombre}")
            print(f"   - Código: {codigo}")
        else:
            print(f"\n⚠️  El sistema necesita ajustes adicionales")
    else:
        print(f"\n❌ No se pudieron obtener credenciales válidas")

if __name__ == "__main__":
    main() 