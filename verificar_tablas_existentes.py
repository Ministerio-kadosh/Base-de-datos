#!/usr/bin/env python3
"""
Script para verificar qué tablas existen realmente en Supabase
"""

import os
import sys
from supabase import create_client, Client

# Configuración Supabase
supabase_url = 'https://vztpbpontffuawntmixp.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ6dHBicG9udGZmdWF3bnRtaXhwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTE1MTMwOTQsImV4cCI6MjA2NzA4OTA5NH0.6CbDGLtfr493dJFXRNPczMW2oGms9JOO7QLAsgakdvs'

supabase: Client = create_client(supabase_url, supabase_key)

def verificar_tablas():
    """Verificar qué tablas existen en la base de datos"""
    
    # Lista de todas las tablas que deberían existir
    tablas_esperadas = [
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
    
    print("🔍 Verificando tablas existentes en Supabase...")
    print("=" * 60)
    
    tablas_existentes = []
    tablas_faltantes = []
    
    for tabla in tablas_esperadas:
        try:
            response = supabase.table(tabla).select('*').limit(1).execute()
            print(f"✅ Tabla '{tabla}' - EXISTE")
            tablas_existentes.append(tabla)
            
        except Exception as e:
            error_msg = str(e)
            if "does not exist" in error_msg:
                print(f"❌ Tabla '{tabla}' - NO EXISTE")
                tablas_faltantes.append(tabla)
            else:
                print(f"⚠️  Tabla '{tabla}' - Error: {error_msg}")
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN:")
    print(f"✅ Tablas existentes: {len(tablas_existentes)}")
    print(f"❌ Tablas faltantes: {len(tablas_faltantes)}")
    
    if tablas_faltantes:
        print("\n🔧 Tablas que necesitan ser creadas:")
        for tabla in tablas_faltantes:
            print(f"   - {tabla}")
    
    return tablas_existentes, tablas_faltantes

def verificar_estructura_tabla(tabla):
    """Verificar la estructura de una tabla específica"""
    try:
        response = supabase.table(tabla).select('*').limit(1).execute()
        if response.data:
            print(f"\n📋 Estructura de tabla '{tabla}':")
            for columna, valor in response.data[0].items():
                print(f"   - {columna}: {type(valor).__name__}")
        else:
            print(f"\n📋 Tabla '{tabla}' está vacía")
    except Exception as e:
        print(f"❌ Error al verificar estructura de '{tabla}': {str(e)}")

def main():
    print("🚀 Verificación de tablas en Supabase")
    print("=" * 60)
    
    # Verificar tablas existentes
    existentes, faltantes = verificar_tablas()
    
    # Verificar estructura de algunas tablas importantes
    if 'administradores' in existentes:
        verificar_estructura_tabla('administradores')
    
    if 'predicadores' in existentes:
        verificar_estructura_tabla('predicadores')
    
    if 'reuniones' in existentes:
        verificar_estructura_tabla('reuniones')
    
    print("\n🎯 Verificación completada")

if __name__ == "__main__":
    main() 