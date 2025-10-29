#!/usr/bin/env python3
"""
Script para generar ejecutables multiplataforma del chatbot de salud mental
Soporta Windows (.exe) y macOS (.app)
"""

import os
import sys
import subprocess
import shutil
import platform

def detect_platform():
    """Detecta la plataforma actual"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    elif system == "darwin":
        return "macos"
    elif system == "linux":
        return "linux"
    else:
        return "unknown"

def check_pyinstaller():
    """Verifica si PyInstaller está instalado"""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Instala PyInstaller"""
    print("📦 Instalando PyInstaller...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        return True
    except subprocess.CalledProcessError:
        return False

def create_windows_spec():
    """Crea archivo .spec para Windows"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

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
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
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
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
'''
    
    with open('chatbot_windows.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Archivo .spec para Windows creado")

def create_macos_spec():
    """Crea archivo .spec para macOS"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

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
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
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
    [],
    exclude_binaries=True,
    name='ChatbotSaludMental',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ChatbotSaludMental',
)

app = BUNDLE(
    coll,
    name='Chatbot Salud Mental.app',
    icon=None,
    bundle_identifier='com.saludmental.chatbot',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSAppleScriptEnabled': False,
        'CFBundleDocumentTypes': [
            {
                'CFBundleTypeName': 'My File Format',
                'CFBundleTypeIconFile': 'MyFileIcon.icns',
                'LSItemContentTypes': ['com.example.myformat'],
                'LSHandlerRank': 'Owner'
            }
        ]
    },
)
'''
    
    with open('chatbot_macos.spec', 'w') as f:
        f.write(spec_content)
    
    print("✓ Archivo .spec para macOS creado")

def build_windows_executable():
    """Construye ejecutable para Windows"""
    print("🔨 Construyendo ejecutable para Windows...")
    
    try:
        create_windows_spec()
        
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "chatbot_windows.spec"]
        subprocess.check_call(cmd)
        
        print("✅ Ejecutable para Windows creado exitosamente")
        print("📁 Ubicación: dist/ChatbotSaludMental.exe")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error construyendo ejecutable para Windows: {e}")
        return False

def build_macos_executable():
    """Construye ejecutable para macOS"""
    print("🔨 Construyendo aplicación para macOS...")
    
    try:
        create_macos_spec()
        
        cmd = [sys.executable, "-m", "PyInstaller", "--clean", "chatbot_macos.spec"]
        subprocess.check_call(cmd)
        
        print("✅ Aplicación para macOS creada exitosamente")
        print("📁 Ubicación: dist/Chatbot Salud Mental.app")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error construyendo aplicación para macOS: {e}")
        return False

def create_distribution_package():
    """Crea paquete de distribución"""
    current_platform = detect_platform()
    
    print(f"\n📦 Creando paquete de distribución para {current_platform}...")
    
    # Crear directorio de distribución
    dist_dir = f"ChatbotSaludMental_{current_platform}"
    if os.path.exists(dist_dir):
        shutil.rmtree(dist_dir)
    os.makedirs(dist_dir)
    
    # Copiar archivos necesarios
    files_to_copy = [
        'README.md',
        'requirements.txt',
        'MIGRATION_GUIDE.md',
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_dir)
    
    # Copiar ejecutable según plataforma
    if current_platform == "windows":
        if os.path.exists('dist/ChatbotSaludMental.exe'):
            shutil.copy2('dist/ChatbotSaludMental.exe', dist_dir)
            
            # Crear script de instalación
            with open(f'{dist_dir}/INSTALL.bat', 'w') as f:
                f.write('''@echo off
echo Chatbot de Salud Mental - Instalacion
echo =====================================
echo.
echo Este es un ejecutable portable.
echo No requiere instalacion adicional.
echo.
echo Para ejecutar:
echo   - Doble clic en ChatbotSaludMental.exe
echo.
echo Requisitos:
echo   - Windows 10 o superior
echo   - 4GB RAM minimo
echo.
pause
''')
    
    elif current_platform == "macos":
        if os.path.exists('dist/Chatbot Salud Mental.app'):
            shutil.copytree('dist/Chatbot Salud Mental.app', f'{dist_dir}/Chatbot Salud Mental.app')
            
            # Crear script de instalación
            with open(f'{dist_dir}/INSTALL.command', 'w') as f:
                f.write('''#!/bin/bash
echo "Chatbot de Salud Mental - Instalación"
echo "===================================="
echo ""
echo "Para instalar:"
echo "1. Arrastra 'Chatbot Salud Mental.app' a /Applications"
echo "2. O ejecuta directamente desde aquí"
echo ""
echo "Requisitos:"
echo "  - macOS 10.14 o superior"
echo "  - 4GB RAM mínimo"
echo ""
echo "Si macOS bloquea la aplicación:"
echo "  Sistema > Privacidad y Seguridad > Permitir"
echo ""
read -p "Presiona Enter para continuar..."
''')
            os.chmod(f'{dist_dir}/INSTALL.command', 0o755)
    
    # Crear archivo ZIP
    archive_name = f"{dist_dir}.zip"
    shutil.make_archive(dist_dir.replace('.zip', ''), 'zip', dist_dir)
    
    print(f"✅ Paquete de distribución creado: {archive_name}")
    
    return archive_name

def test_executable():
    """Prueba el ejecutable creado"""
    current_platform = detect_platform()
    
    print(f"\n🧪 Probando ejecutable para {current_platform}...")
    
    if current_platform == "windows":
        exe_path = "dist/ChatbotSaludMental.exe"
        if os.path.exists(exe_path):
            print(f"✅ Ejecutable encontrado: {exe_path}")
            print(f"📊 Tamaño: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
            return True
    
    elif current_platform == "macos":
        app_path = "dist/Chatbot Salud Mental.app"
        if os.path.exists(app_path):
            print(f"✅ Aplicación encontrada: {app_path}")
            # Calcular tamaño de la aplicación
            total_size = 0
            for dirpath, dirnames, filenames in os.walk(app_path):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    total_size += os.path.getsize(filepath)
            print(f"📊 Tamaño: {total_size / (1024*1024):.1f} MB")
            return True
    
    print("❌ Ejecutable no encontrado")
    return False

def main():
    """Función principal"""
    current_platform = detect_platform()
    
    print("GENERADOR DE EJECUTABLES MULTIPLATAFORMA")
    print("=" * 50)
    print(f"🖥️  Plataforma detectada: {current_platform}")
    
    if current_platform == "unknown":
        print("❌ Plataforma no soportada")
        return
    
    # Verificar PyInstaller
    if not check_pyinstaller():
        print("📦 PyInstaller no está instalado.")
        response = input("¿Quieres instalarlo? (s/n): ")
        
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            if not install_pyinstaller():
                print("❌ Error instalando PyInstaller")
                return
        else:
            print("❌ PyInstaller es necesario para crear ejecutables")
            return
    
    print("✅ PyInstaller disponible")
    
    # Construir ejecutable según plataforma
    success = False
    
    if current_platform == "windows":
        success = build_windows_executable()
    elif current_platform == "macos":
        success = build_macos_executable()
    elif current_platform == "linux":
        print("ℹ️  En Linux, usa el script install.sh para distribución")
        success = True
    
    if success:
        # Probar ejecutable
        if current_platform in ["windows", "macos"]:
            test_executable()
        
        # Crear paquete de distribución
        response = input("\n¿Quieres crear un paquete de distribución? (s/n): ")
        if response.lower() in ['s', 'si', 'sí', 'y', 'yes']:
            package = create_distribution_package()
            print(f"\n🎉 ¡Paquete listo para distribución!")
            print(f"📦 Archivo: {package}")
        
        print(f"\n✅ ¡Ejecutable para {current_platform} creado exitosamente!")
        
        if current_platform == "windows":
            print("\n📋 Para distribuir en Windows:")
            print("   - Comparte: ChatbotSaludMental_windows.zip")
            print("   - El usuario solo necesita descomprimir y ejecutar")
            
        elif current_platform == "macos":
            print("\n📋 Para distribuir en macOS:")
            print("   - Comparte: ChatbotSaludMental_macos.zip")
            print("   - El usuario puede arrastrar la .app a /Applications")
    
    else:
        print(f"\n❌ Error creando ejecutable para {current_platform}")

if __name__ == "__main__":
    main()
