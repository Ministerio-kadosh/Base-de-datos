#!/usr/bin/env python3
"""
Script para verificar el estado de las tablas y crear datos de prueba
"""

import os
import sys
from datetime import datetime, timedelta

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_tables():
    """Verificar el estado de las tablas"""
    try:
        from supabase import create_client, Client
        
        # Configuración Supabase
        supabase_url = os.environ.get('SUPABASE_URL')
        supabase_key = os.environ.get('SUPABASE_KEY')
        
        if not supabase_url or not supabase_key:
            print("❌ Variables de entorno de Supabase no configuradas")
            return
        
        supabase: Client = create_client(supabase_url, supabase_key)
        
        print("🔍 Verificando estado de las tablas...")
        
        # Lista de tablas a verificar
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
            try:
                response = supabase.table(tabla).select('*').limit(1).execute()
                count = len(response.data)
                print(f"  {'✅' if count > 0 else '⚠️'} {tabla}: {count} registros")
                
                # Si la tabla está vacía, crear datos de prueba
                if count == 0:
                    create_test_data(supabase, tabla)
                    
            except Exception as e:
                print(f"  ❌ {tabla}: Error - {str(e)}")
        
        print("\n✅ Verificación completada")
        
    except Exception as e:
        print(f"❌ Error general: {str(e)}")

def create_test_data(supabase, tabla):
    """Crear datos de prueba para tablas vacías"""
    try:
        print(f"    📝 Creando datos de prueba para {tabla}...")
        
        if tabla == 'administradores':
            data = {
                'email': 'admin@test.com',
                'nombre': 'Administrador Test',
                'rol': 'Admin',
                'codigo': '123456',
                'fecha_creacion': datetime.now().isoformat()
            }
        elif tabla == 'predicadores':
            data = {
                'Nombre': 'Juan',
                'Apellido': 'Pérez',
                'Numero': '123456789',
                'estado': 'Activo',
                'fecha': datetime.now().isoformat()
            }
        elif tabla == 'reuniones':
            data = {
                'Dirige': 'Pastor Principal',
                'Lectura': 'Juan 3:16',
                'Cantos_alegre': 'Alabanzas',
                'Ofrenda': 'Diezmo',
                'Predica': 'El amor de Dios',
                'fecha': datetime.now().isoformat()
            }
        elif tabla == 'calendario':
            data = {
                'Evento': 'Reunión de Jóvenes',
                'Fecha': (datetime.now() + timedelta(days=7)).isoformat(),
                'Observaciones': 'Evento de prueba'
            }
        elif tabla == 'bandeja':
            data = {
                'Objetivo': 'Organizar evento',
                'Descripcion': 'Tarea de prueba para verificar funcionamiento',
                'estado': 'Pendiente',
                'fecha': datetime.now().isoformat()
            }
        elif tabla == 'asistencias':
            data = {
                'Nombre': 'María García',
                'Numero': '987654321',
                'unoviernes': 'Presente',
                'dosviernes': 'Presente',
                'tresViernes': 'Ausente',
                'cuatroviernes': 'Presente',
                'fecha': datetime.now().isoformat()
            }
        elif tabla == 'jovenes':
            data = {
                'Nombre': 'Carlos López',
                'Edad': '20',
                'Telefono': '555123456',
                'estado': 'Activo',
                'fecha': datetime.now().isoformat()
            }
        elif tabla == 'finanzas':
            data = {
                'Concepto': 'Diezmo',
                'Monto': '100.00',
                'Fecha': datetime.now().isoformat(),
                'Observaciones': 'Entrada de prueba'
            }
        elif tabla == 'informes':
            data = {
                'titulo': 'Informe de Prueba',
                'descripcion': 'Informe generado automáticamente para pruebas',
                'consultas': [],
                'formato': 'json',
                'fecha_creacion': datetime.now().isoformat(),
                'estado': 'activo'
            }
        else:
            print(f"    ⚠️ No se definieron datos de prueba para {tabla}")
            return
        
        # Insertar datos
        response = supabase.table(tabla).insert(data).execute()
        
        if response.data:
            print(f"    ✅ Datos de prueba creados para {tabla}")
        else:
            print(f"    ❌ Error al crear datos para {tabla}")
            
    except Exception as e:
        print(f"    ❌ Error creando datos para {tabla}: {str(e)}")

if __name__ == "__main__":
    test_tables() 