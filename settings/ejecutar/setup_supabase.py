#!/usr/bin/env python3
"""
Script de instalación rápida para configurar Supabase
Sistema de Gestión Flask
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Imprimir encabezado del script"""
    print("=" * 60)
    print("🚀 CONFIGURACIÓN RÁPIDA DE SUPABASE")
    print("   Sistema de Gestión Flask")
    print("=" * 60)

def check_python_version():
    """Verificar versión de Python"""
    print("🔍 Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def install_dependencies():
    """Instalar dependencias"""
    print("\n📦 Instalando dependencias...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def check_env_file():
    """Verificar archivo .env"""
    print("\n🔍 Verificando archivo .env...")
    env_file = Path(".env")
    
    if env_file.exists():
        print("✅ Archivo .env encontrado")
        return True
    else:
        print("⚠️  Archivo .env no encontrado")
        print("   Creando archivo .env desde env_example.txt...")
        
        example_file = Path("env_example.txt")
        if example_file.exists():
            try:
                with open(example_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                with open(env_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print("✅ Archivo .env creado")
                print("⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales de Supabase")
                return True
            except Exception as e:
                print(f"❌ Error al crear .env: {e}")
                return False
        else:
            print("❌ Archivo env_example.txt no encontrado")
            return False

def check_supabase_files():
    """Verificar archivos de configuración de Supabase"""
    print("\n🔍 Verificando archivos de configuración...")
    
    required_files = [
        "supabase_setup.sql",
        "test_supabase_connection.py",
        "SUPABASE_SETUP.md"
    ]
    
    missing_files = []
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - No encontrado")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Faltan {len(missing_files)} archivos de configuración")
        return False
    
    return True

def run_connection_test():
    """Ejecutar prueba de conexión"""
    print("\n🧪 Ejecutando prueba de conexión...")
    
    if not Path("test_supabase_connection.py").exists():
        print("❌ Archivo de prueba no encontrado")
        return False
    
    try:
        result = subprocess.run([sys.executable, "test_supabase_connection.py"], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Prueba de conexión exitosa")
            return True
        else:
            print("❌ Prueba de conexión falló")
            print("   Salida de error:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error al ejecutar prueba: {e}")
        return False

def show_next_steps():
    """Mostrar próximos pasos"""
    print("\n" + "=" * 60)
    print("📋 PRÓXIMOS PASOS")
    print("=" * 60)
    
    print("1. 🏗️  Crear proyecto en Supabase:")
    print("   - Ve a https://supabase.com")
    print("   - Crea un nuevo proyecto")
    print("   - Anota la URL y las claves API")
    
    print("\n2. ⚙️  Configurar credenciales:")
    print("   - Edita el archivo .env")
    print("   - Reemplaza las credenciales de ejemplo")
    
    print("\n3. 🗄️  Configurar base de datos:")
    print("   - Ve al SQL Editor en Supabase")
    print("   - Ejecuta el script supabase_setup.sql")
    
    print("\n4. 🧪 Probar conexión:")
    print("   - Ejecuta: python test_supabase_connection.py")
    
    print("\n5. 🚀 Ejecutar aplicación:")
    print("   - Ejecuta: python app.py")
    
    print("\n📖 Para más detalles, consulta SUPABASE_SETUP.md")

def main():
    """Función principal"""
    print_header()
    
    # Verificar Python
    if not check_python_version():
        return
    
    # Instalar dependencias
    if not install_dependencies():
        print("\n❌ No se pudieron instalar las dependencias")
        return
    
    # Verificar archivo .env
    if not check_env_file():
        print("\n❌ Problema con el archivo .env")
        return
    
    # Verificar archivos de configuración
    if not check_supabase_files():
        print("\n❌ Faltan archivos de configuración")
        return
    
    # Intentar prueba de conexión
    print("\n🔍 Intentando prueba de conexión...")
    if run_connection_test():
        print("\n🎉 ¡Configuración completada exitosamente!")
    else:
        print("\n⚠️  La prueba de conexión falló")
        print("   Esto es normal si aún no has configurado Supabase")
    
    # Mostrar próximos pasos
    show_next_steps()

if __name__ == "__main__":
    main() 