#!/usr/bin/env python3
"""
Script para generar ejecutable del chatbot de salud mental
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Verifica si PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Instala PyInstaller"""
    print("Instalando PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True
    except subprocess.CalledProcessError:
        return False

def create_spec_file():
    """Crea archivo .spec personalizado para PyInstaller"""
    spec_content = '''
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('data/*.json', 'data'),
        ('utils/*.py', 'utils'),
        ('core/*.py', 'core'),
        ('ui/*.py', 'ui'),
    ],
    hiddenimports=[
        'sklearn.utils._cython_blas',
        'sklearn.neighbors.typedefs',
        'sklearn.neighbors.quad_tree',
        'sklearn.tree._utils',
        'pandas._libs.tslibs.timedeltas',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.skiplist',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='ChatbotSaludMental',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('chatbot.spec', 'w') as f:
        f.write(spec_content)
    
    print("Archivo .spec creado")

def build_executable():
    """Construye el ejecutable"""
    print("Construyendo ejecutable...")
    
    try:
        # Usar el archivo .spec personalizado
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "chatbot.spec"]
        subprocess.check_call(cmd)
        
        print("✓ Ejecutable creado exitosamente")
        print("  Ubicación: dist/ChatbotSaludMental")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Error construyendo ejecutable: {e}")
        return False

def create_installer_script():
    """Crea script de instalación simple"""
    installer_content = '''#!/bin/bash
# Script de instalación para Chatbot de Salud Mental

echo "=== INSTALADOR CHATBOT DE SALUD MENTAL ==="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado"
    exit 1
fi

echo "✓ Python 3 encontrado"

# Instalar dependencias
echo "Instalando dependencias..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas"
else
    echo "✗ Error instalando dependencias"
    exit 1
fi

# Hacer ejecutable
chmod +x main.py

echo ""
echo "=== INSTALACIÓN COMPLETADA ==="
echo ""
echo "Para ejecutar el chatbot:"
echo "  python3 main.py"
echo ""
echo "O directamente:"
echo "  ./main.py"
echo ""
'''
    
    with open('install.sh', 'w') as f:
        f.write(installer_content)
    
    os.chmod('install.sh', 0o755)
    print("Script de instalación creado: install.sh")

def main():
    """Función principal"""
    print("GENERADOR DE EJECUTABLE - CHATBOT DE SALUD MENTAL")
    print("=" * 55)
    
    # Verificar PyInstaller
    if not check_pyinstaller():
        print("PyInstaller no está instalado.")
        response = input("¿Quieres instalarlo? (s/n): ")
        
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            if not install_pyinstaller():
                print("Error instalando PyInstaller")
                return
        else:
            print("PyInstaller es necesario para crear el ejecutable")
            return
    
    print("✓ PyInstaller disponible")
    
    # Crear archivos necesarios
    create_spec_file()
    create_installer_script()
    
    # Preguntar si crear ejecutable
    response = input("¿Quieres crear el ejecutable ahora? (s/n): ")
    
    if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
        if build_executable():
            print("\n🎉 ¡Ejecutable creado exitosamente!")
            print("\nArchivos generados:")
            print("  - dist/ChatbotSaludMental (ejecutable)")
            print("  - install.sh (script de instalación)")
            print("  - chatbot.spec (configuración PyInstaller)")
        else:
            print("\n❌ Error creando ejecutable")
    
    print("\nPara crear el ejecutable manualmente:")
    print("  pyinstaller --onefile --windowed main.py")

if __name__ == "__main__":
    main()
