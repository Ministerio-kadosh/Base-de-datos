#!/usr/bin/env python3
"""
Script para crear un nuevo administrador con rol Super Admin
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
supabase_key = os.environ.get('SUPABASE_SERVICE_KEY', os.environ.get('SUPABASE_KEY'))
supabase: Client = create_client(supabase_url, supabase_key)

# Intentar usar la clave de servicio si está disponible
if not os.environ.get('SUPABASE_SERVICE_KEY'):
    print("⚠️ ADVERTENCIA: No se encontró SUPABASE_SERVICE_KEY en el archivo .env")
    print("   Es posible que las políticas RLS impidan la creación del administrador")
    print("   Considere agregar SUPABASE_SERVICE_KEY=<su_clave_de_servicio> al archivo .env")

def hash_password(password):
    """Generar hash seguro de contraseña usando bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def crear_super_admin():
    """Crear un nuevo administrador con rol Super Admin"""
    
    print("🔐 Creando nuevo Super Administrador")
    print("=" * 50)
    
    try:
        # Datos del nuevo administrador
        nombre_admin = "Darwin Garcia"
        rol_admin = "Super Admin"
        codigo_acceso = "adali-930"
        
        # Verificar si ya existe
        response = supabase.table('administradores').select('*').eq('nombre_admin', nombre_admin).execute()
        
        if response.data:
            print(f"❌ Ya existe un administrador con el nombre {nombre_admin}")
            return False
        
        # Generar hash seguro
        hash_codigo = hash_password(codigo_acceso)
        
        print(f"📋 Datos del nuevo administrador:")
        print(f"   - Nombre: {nombre_admin}")
        print(f"   - Rol: {rol_admin}")
        print(f"   - Código: {codigo_acceso}")
        print(f"   - Hash: {hash_codigo[:20]}...")
        
        # Intentar primero con el método estándar
        try:
            insert_response = supabase.table('administradores').insert({
                'nombre_admin': nombre_admin,
                'rol_admin': rol_admin,
                'codigo_acceso': hash_codigo
            }).execute()
            
            if insert_response.data:
                print(f"✅ Administrador creado exitosamente")
                print(f"   - Usuario: {nombre_admin}")
                print(f"   - Rol: {rol_admin}")
                print(f"   - Código: {codigo_acceso}")
                return True
        except Exception as e:
            print(f"⚠️ Error con método estándar: {str(e)}")
            print(f"   Intentando método alternativo...")
            
            # Método alternativo: SQL directo
            sql = f"""
            INSERT INTO administradores (nombre_admin, rol_admin, codigo_acceso) 
            VALUES ('{nombre_admin}', '{rol_admin}', '{hash_codigo}')
            RETURNING *;
            """
            
            try:
                # Ejecutar SQL directo
                rpc_response = supabase.rpc('ejecutar_sql_admin', {"sql": sql}).execute()
                
                if rpc_response.data:
                    print(f"✅ Administrador creado exitosamente (método alternativo)")
                    print(f"   - Usuario: {nombre_admin}")
                    print(f"   - Rol: {rol_admin}")
                    print(f"   - Código: {codigo_acceso}")
                    return True
                else:
                    print(f"❌ Error al crear administrador (método alternativo)")
                    print(f"   Consulte con el administrador de la base de datos")
                    print(f"   Puede ejecutar manualmente el siguiente SQL:")
                    print(f"   {sql}")
                    return False
            except Exception as sql_error:
                print(f"❌ Error con método alternativo: {str(sql_error)}")
                print(f"   Es posible que necesite:")
                print(f"   1. Usar una clave de servicio de Supabase")
                print(f"   2. Deshabilitar temporalmente RLS en la tabla administradores")
                print(f"   3. Crear una función RPC en Supabase para ejecutar SQL con privilegios")
                print(f"\n   SQL para crear manualmente:")
                print(f"   {sql}")
                return False
            
    except Exception as e:
        print(f"❌ Error general: {str(e)}")
        return False

def verificar_credenciales():
    """Verificar que las credenciales funcionan correctamente"""
    
    print(f"\n🧪 Verificando credenciales del nuevo administrador")
    print("=" * 50)
    
    try:
        # Importar funciones de sesión
        sys.path.append('./')
        from sesion import is_admin_by_name, get_admin_role
        
        # Probar autenticación
        nombre = "Darwin Garcia"
        codigo = "adali-930"
        
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
    print("🚀 Creación de Super Administrador")
    print("=" * 60)
    
    # Crear administrador
    if crear_super_admin():
        # Verificar que funcionan
        if verificar_credenciales():
            print(f"\n🎉 ¡CREACIÓN COMPLETADA EXITOSAMENTE!")
            print(f"   - Administrador creado con bcrypt")
            print(f"   - Sistema de autenticación seguro")
            print(f"   - Listo para usar en producción")
        else:
            print(f"\n⚠️  Administrador creado pero las credenciales no funcionan")
    else:
        print(f"\n❌ Error en la creación del administrador")

if __name__ == "__main__":
    main()