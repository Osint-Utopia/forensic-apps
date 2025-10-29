@echo off
REM Script de instalación para Windows - Chatbot de Salud Mental

echo ===============================================
echo INSTALADOR CHATBOT DE SALUD MENTAL - WINDOWS
echo ===============================================
echo.

REM Verificar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no está instalado o no está en PATH
    echo.
    echo Por favor instala Python 3.8+ desde:
    echo https://www.python.org/downloads/
    echo.
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)

echo ✓ Python encontrado: 
python --version

REM Verificar pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: pip no está disponible
    pause
    exit /b 1
)

echo ✓ pip encontrado

REM Actualizar pip
echo.
echo Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo.
echo Instalando dependencias de Python...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ERROR: Falló la instalación de dependencias
    echo.
    echo Intenta ejecutar manualmente:
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

echo ✓ Dependencias instaladas correctamente

REM Verificar tkinter (generalmente incluido en Windows Python)
echo.
echo Verificando tkinter...
python -c "import tkinter; print('✓ tkinter disponible')" 2>nul
if %errorlevel% neq 0 (
    echo ⚠️  tkinter no disponible
    echo Reinstala Python desde python.org con "tcl/tk and IDLE" habilitado
)

REM Crear accesos directos
echo.
echo Creando scripts de ejecución...

REM Script para ejecutar el chatbot
echo @echo off > ejecutar_chatbot.bat
echo cd /d "%~dp0" >> ejecutar_chatbot.bat
echo python main.py >> ejecutar_chatbot.bat
echo pause >> ejecutar_chatbot.bat

REM Script para ejecutar pruebas
echo @echo off > ejecutar_pruebas.bat
echo cd /d "%~dp0" >> ejecutar_pruebas.bat
echo python test_chatbot.py >> ejecutar_pruebas.bat
echo pause >> ejecutar_pruebas.bat

REM Script para crear ejecutable
echo @echo off > crear_ejecutable.bat
echo cd /d "%~dp0" >> crear_ejecutable.bat
echo python build_executable.py >> crear_ejecutable.bat
echo pause >> crear_ejecutable.bat

echo ✓ Scripts de ejecución creados

echo.
echo ===============================================
echo INSTALACIÓN COMPLETADA PARA WINDOWS
echo ===============================================
echo.
echo Para usar el chatbot:
echo   - Doble clic en: ejecutar_chatbot.bat
echo   - O desde cmd: python main.py
echo.
echo Para ejecutar pruebas:
echo   - Doble clic en: ejecutar_pruebas.bat
echo   - O desde cmd: python test_chatbot.py
echo.
echo Para crear ejecutable:
echo   - Doble clic en: crear_ejecutable.bat
echo.
echo ¡Disfruta usando el Chatbot de Salud Mental!
echo.
pause
