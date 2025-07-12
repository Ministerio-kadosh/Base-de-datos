#!/usr/bin/env python3
"""
Script para verificar los nombres exactos de las columnas en cada tabla
"""

import os
import sys
from supabase import create_client, Client

# Configuración Supabase
supabase_url = 'https://vztpbpontffuawntmixp.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6dHBicG9udGZmdWF3bnRtaXhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE1MTMwOTQsImV4cCI6MjA2NzA4OTA5NH0.6CbDGLtfr493dJFXRNPczMW2oGms9JOO7QLAsgakdvs'

supabase: Client = create_client(supabase_url, supabase_key)

def verificar_columnas_tabla(tabla):
    """Verificar las columnas de una tabla específica"""
    try:
        response = supabase.table(tabla).select('*').limit(1).execute()
        
        if response.data:
            print(f"\n📋 Tabla '{tabla}':")
            print("   Columnas encontradas:")
            for columna, valor in response.data[0].items():
                print(f"     - {columna}: {type(valor).__name__} = {valor}")
        else:
            print(f"\n📋 Tabla '{tabla}' está vacía")
            
    except Exception as e:
        print(f"❌ Error al verificar '{tabla}': {str(e)}")

def main():
    print("🔍 Verificando columnas de todas las tablas")
    print("=" * 60)
    
    tablas = [
        'administradores',
        'predicadores', 
        'reuniones',
        'calendario',
        'bandeja',
        'asistencias',
        'jovenes',
        'finanzas',
        'historial_cambios',
        'informes'
    ]
    
    for tabla in tablas:
        verificar_columnas_tabla(tabla)
    
    print("\n🎯 Verificación completada")

if __name__ == "__main__":
    main() 