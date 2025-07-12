#!/usr/bin/env python3
"""
Script de prueba para verificar que las tablas con minúsculas funcionan correctamente
"""

import os
import sys
from supabase import create_client, Client

# Configuración Supabase
supabase_url = 'https://vztpbpontffuawntmixp.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6dHBicG9udGZmdWF3bnRtaXhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE1MTMwOTQsImV4cCI6MjA2NzA4OTA5NH0.6CbDGLtfr493dJFXRNPczMW2oGms9JOO7QLAsgakdvs'

if not supabase_url or not supabase_key:
    print("❌ Error: Variables de entorno SUPABASE_URL y SUPABASE_KEY no configuradas")
    sys.exit(1)

supabase: Client = create_client(supabase_url, supabase_key)

def test_tablas_minusculas():
    """Probar que todas las tablas con minúsculas existen y funcionan"""
    
    tablas_a_probar = [
        'administradores',
        'predicadores', 
        'reuniones',
        'calendario',
        'bandeja',
        'asistencias',
        'jovenes',
        'finanzas',
        'historial_cambios',
        'informes',
        'informes_generados'
    ]
    
    print("🔍 Probando tablas con minúsculas...")
    print("=" * 50)
    
    for tabla in tablas_a_probar:
        try:
            print(f"📋 Probando tabla: {tabla}")
            
            # Intentar hacer una consulta simple
            response = supabase.table(tabla).select('*').limit(1).execute()
            
            if response.data is not None:
                print(f"✅ Tabla '{tabla}' - OK (registros: {len(response.data)})")
            else:
                print(f"⚠️  Tabla '{tabla}' - Sin datos")
                
        except Exception as e:
            print(f"❌ Tabla '{tabla}' - Error: {str(e)}")
    
    print("=" * 50)
    print("🎯 Prueba completada")

def test_login():
    """Probar el login con administradores"""
    print("\n🔐 Probando login...")
    print("=" * 30)
    
    try:
        # Buscar administradores
        response = supabase.table('administradores').select('*').limit(5).execute()
        
        if response.data:
            print(f"✅ Administradores encontrados: {len(response.data)}")
            for admin in response.data:
                print(f"   - {admin.get('nombre', 'N/A')} ({admin.get('rol', 'N/A')})")
        else:
            print("⚠️  No se encontraron administradores")
            
    except Exception as e:
        print(f"❌ Error al buscar administradores: {str(e)}")

def test_relaciones():
    """Probar las relaciones entre tablas"""
    print("\n🔗 Probando relaciones...")
    print("=" * 30)
    
    try:
        # Probar relación reuniones -> predicadores
        response = supabase.table('reuniones').select('*, predicadores(nombre, apellido)').limit(3).execute()
        print(f"✅ Relación reuniones->predicadores: {len(response.data)} registros")
        
        # Probar relación asistencias -> jóvenes
        response = supabase.table('asistencias').select('*, jovenes(nombre, edad)').limit(3).execute()
        print(f"✅ Relación asistencias->jóvenes: {len(response.data)} registros")
        
        # Probar relación finanzas -> reuniones
        response = supabase.table('finanzas').select('*, reuniones(fecha_reunion)').limit(3).execute()
        print(f"✅ Relación finanzas->reuniones: {len(response.data)} registros")
        
    except Exception as e:
        print(f"❌ Error al probar relaciones: {str(e)}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas de tablas con minúsculas")
    print("=" * 60)
    
    test_tablas_minusculas()
    test_login()
    test_relaciones()
    
    print("\n🎉 Pruebas completadas") 