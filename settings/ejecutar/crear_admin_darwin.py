#!/usr/bin/env python3
"""
Script simple para crear un administrador con rol Super Admin
"""

import os
import hashlib
import psycopg2
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def crear_super_admin():
    """Crear un nuevo administrador con rol Super Admin usando conexión directa a PostgreSQL"""
    
    print("🔐 Creando nuevo Super Administrador")
    print("=" * 50)
    
    try:
        # Datos del nuevo administrador
        nombre_admin = "Darwin Garcia"
        rol_admin = "Super Admin"
        codigo_acceso = "adali-930"
        
        # Generar hash SHA256
        hash_codigo = hashlib.sha256(codigo_acceso.encode()).hexdigest()
        
        print(f"📋 Datos del nuevo administrador:")
        print(f"   - Nombre: {nombre_admin}")
        print(f"   - Rol: {rol_admin}")
        print(f"   - Código: {codigo_acceso}")
        print(f"   - Hash: {hash_codigo[:20]}...")
        
        # Conectar directamente a PostgreSQL
        db_url = os.environ.get('DATABASE_URL')
        if not db_url:
            print("❌ Error: No se encontró DATABASE_URL en el archivo .env")
            return False
        
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Verificar si ya existe
        cursor.execute("SELECT COUNT(*) FROM administradores WHERE nombre_admin = %s", (nombre_admin,))
        count = cursor.fetchone()[0]
        
        if count > 0:
            print(f"❌ Ya existe un administrador con el nombre {nombre_admin}")
            conn.close()
            return False
        
        # Insertar nuevo administrador
        cursor.execute(
            "INSERT INTO administradores (nombre_admin, rol_admin, codigo_acceso) VALUES (%s, %s, %s) RETURNING id_admin",
            (nombre_admin, rol_admin, hash_codigo)
        )
        
        admin_id = cursor.fetchone()[0]
        conn.commit()
        conn.close()
        
        print(f"✅ Administrador creado exitosamente")
        print(f"   - ID: {admin_id}")
        print(f"   - Usuario: {nombre_admin}")
        print(f"   - Rol: {rol_admin}")
        print(f"   - Código: {codigo_acceso}")
        print(f"   - Método de encriptación: SHA256")
        return True
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("")
        print("Si el error es de conexión o permisos, puede:")
        print("1. Verificar que DATABASE_URL esté correctamente configurado en .env")
        print("2. Ejecutar el script SQL 'crear_admin_darwin.sql' directamente en la consola SQL de Supabase")
        return False

def main():
    print("🚀 Creación de Super Administrador")
    print("=" * 60)
    
    # Crear administrador
    if crear_super_admin():
        print(f"\n🎉 ¡CREACIÓN COMPLETADA EXITOSAMENTE!")
        print(f"   - Administrador creado con SHA256")
        print(f"   - Sistema de autenticación seguro")
        print(f"   - Listo para usar en producción")
    else:
        print(f"\n❌ Error en la creación del administrador")

if __name__ == "__main__":
    main()