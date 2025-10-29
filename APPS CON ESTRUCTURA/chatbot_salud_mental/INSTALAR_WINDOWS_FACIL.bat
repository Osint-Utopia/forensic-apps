@echo off
title Chatbot de Salud Mental - Instalador Facil
color 0A

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                                                              ║
echo  ║           CHATBOT DE SALUD MENTAL - INSTALADOR FACIL         ║
echo  ║                                                              ║
echo  ║                    ¡Solo sigue los pasos!                   ║
echo  ║                                                              ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo.

REM Verificar si Python esta instalado
echo [PASO 1/3] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python NO esta instalado en tu computadora
    echo.
    echo 📥 NECESITAS INSTALAR PYTHON PRIMERO:
    echo.
    echo    1. Ve a: https://www.python.org/downloads/
    echo    2. Descarga Python 3.11 o mas nuevo
    echo    3. Durante la instalacion, marca: "Add Python to PATH"
    echo    4. Instala normalmente
    echo    5. Reinicia tu computadora
    echo    6. Ejecuta este archivo otra vez
    echo.
    echo 💡 ¿Necesitas ayuda? Busca "como instalar python windows" en YouTube
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python encontrado correctamente
echo.

REM Verificar pip
echo [PASO 2/3] Verificando herramientas...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: pip no funciona
    echo 💡 Reinstala Python desde python.org
    pause
    exit /b 1
)

echo ✅ Herramientas listas
echo.

REM Instalar dependencias
echo [PASO 3/3] Instalando el chatbot...
echo.
echo ⏳ Esto puede tomar unos minutos...
echo ⏳ NO cierres esta ventana...
echo.

pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error instalando componentes
    echo.
    echo 🔧 SOLUCION:
    echo    1. Verifica tu conexion a internet
    echo    2. Ejecuta como Administrador (click derecho)
    echo    3. O contacta soporte tecnico
    echo.
    pause
    exit /b 1
)

echo ✅ Chatbot instalado correctamente
echo.

REM Crear accesos directos super faciles
echo Creando accesos directos...

REM Ejecutar chatbot (SUPER FACIL)
echo @echo off > "🤖 ABRIR CHATBOT.bat"
echo title Chatbot de Salud Mental >> "🤖 ABRIR CHATBOT.bat"
echo cd /d "%~dp0" >> "🤖 ABRIR CHATBOT.bat"
echo echo. >> "🤖 ABRIR CHATBOT.bat"
echo echo ⏳ Iniciando chatbot... >> "🤖 ABRIR CHATBOT.bat"
echo echo ⏳ Se abrira una ventana nueva... >> "🤖 ABRIR CHATBOT.bat"
echo echo. >> "🤖 ABRIR CHATBOT.bat"
echo python main.py >> "🤖 ABRIR CHATBOT.bat"
echo if %%errorlevel%% neq 0 ( >> "🤖 ABRIR CHATBOT.bat"
echo     echo. >> "🤖 ABRIR CHATBOT.bat"
echo     echo ❌ Error ejecutando chatbot >> "🤖 ABRIR CHATBOT.bat"
echo     echo 💡 Ejecuta INSTALAR_WINDOWS_FACIL.bat otra vez >> "🤖 ABRIR CHATBOT.bat"
echo     pause >> "🤖 ABRIR CHATBOT.bat"
echo ^) >> "🤖 ABRIR CHATBOT.bat"

REM Probar chatbot (FACIL)
echo @echo off > "🧪 PROBAR CHATBOT.bat"
echo title Probando Chatbot >> "🧪 PROBAR CHATBOT.bat"
echo cd /d "%~dp0" >> "🧪 PROBAR CHATBOT.bat"
echo echo. >> "🧪 PROBAR CHATBOT.bat"
echo echo ⏳ Probando chatbot... >> "🧪 PROBAR CHATBOT.bat"
echo echo. >> "🧪 PROBAR CHATBOT.bat"
echo python test_chatbot.py >> "🧪 PROBAR CHATBOT.bat"
echo echo. >> "🧪 PROBAR CHATBOT.bat"
echo echo ✅ Prueba completada >> "🧪 PROBAR CHATBOT.bat"
echo pause >> "🧪 PROBAR CHATBOT.bat"

REM Crear ejecutable (FACIL)
echo @echo off > "📦 CREAR EJECUTABLE.bat"
echo title Creando Ejecutable >> "📦 CREAR EJECUTABLE.bat"
echo cd /d "%~dp0" >> "📦 CREAR EJECUTABLE.bat"
echo echo. >> "📦 CREAR EJECUTABLE.bat"
echo echo ⏳ Creando archivo ejecutable... >> "📦 CREAR EJECUTABLE.bat"
echo echo ⏳ Esto puede tomar 5-10 minutos... >> "📦 CREAR EJECUTABLE.bat"
echo echo ⏳ NO cierres esta ventana... >> "📦 CREAR EJECUTABLE.bat"
echo echo. >> "📦 CREAR EJECUTABLE.bat"
echo python build_executable_cross_platform.py >> "📦 CREAR EJECUTABLE.bat"
echo echo. >> "📦 CREAR EJECUTABLE.bat"
echo echo ✅ Ejecutable creado >> "📦 CREAR EJECUTABLE.bat"
echo pause >> "📦 CREAR EJECUTABLE.bat"

REM Ayuda (SUPER FACIL)
echo @echo off > "❓ AYUDA.bat"
echo title Ayuda - Chatbot >> "❓ AYUDA.bat"
echo color 0B >> "❓ AYUDA.bat"
echo echo. >> "❓ AYUDA.bat"
echo echo  ╔══════════════════════════════════════════════════════════════╗ >> "❓ AYUDA.bat"
echo echo  ║                                                              ║ >> "❓ AYUDA.bat"
echo echo  ║                    COMO USAR EL CHATBOT                     ║ >> "❓ AYUDA.bat"
echo echo  ║                                                              ║ >> "❓ AYUDA.bat"
echo echo  ╚══════════════════════════════════════════════════════════════╝ >> "❓ AYUDA.bat"
echo echo. >> "❓ AYUDA.bat"
echo echo 🤖 PARA USAR EL CHATBOT: >> "❓ AYUDA.bat"
echo echo    - Doble click en: 🤖 ABRIR CHATBOT.bat >> "❓ AYUDA.bat"
echo echo    - Se abre una ventana con el chatbot >> "❓ AYUDA.bat"
echo echo    - Escribe tu pregunta y presiona Enter >> "❓ AYUDA.bat"
echo echo. >> "❓ AYUDA.bat"
echo echo 🧪 PARA PROBAR QUE FUNCIONA: >> "❓ AYUDA.bat"
echo echo    - Doble click en: 🧪 PROBAR CHATBOT.bat >> "❓ AYUDA.bat"
echo echo. >> "❓ AYUDA.bat"
echo echo 📦 PARA CREAR EJECUTABLE: >> "❓ AYUDA.bat"
echo echo    - Doble click en: 📦 CREAR EJECUTABLE.bat >> "❓ AYUDA.bat"
echo echo    - Espera 5-10 minutos >> "❓ AYUDA.bat"
echo echo    - Se crea ChatbotSaludMental.exe >> "❓ AYUDA.bat"
echo echo. >> "❓ AYUDA.bat"
echo echo 🆘 SI TIENES PROBLEMAS: >> "❓ AYUDA.bat"
echo echo    - Ejecuta INSTALAR_WINDOWS_FACIL.bat otra vez >> "❓ AYUDA.bat"
echo echo    - Verifica tu conexion a internet >> "❓ AYUDA.bat"
echo echo    - Contacta soporte tecnico >> "❓ AYUDA.bat"
echo echo. >> "❓ AYUDA.bat"
echo pause >> "❓ AYUDA.bat"

echo ✅ Accesos directos creados
echo.

REM Probar instalacion
echo Probando instalacion...
python -c "import sys; sys.path.append('.'); from core.dataset_processor import DatasetProcessor; print('✅ Chatbot listo')" 2>nul

if %errorlevel% neq 0 (
    echo ⚠️  Advertencia: Puede haber un problema menor
    echo 💡 Prueba ejecutar: 🧪 PROBAR CHATBOT.bat
) else (
    echo ✅ Instalacion verificada correctamente
)

echo.
echo  ╔══════════════════════════════════════════════════════════════╗
echo  ║                                                              ║
echo  ║                    ¡INSTALACION COMPLETADA!                 ║
echo  ║                                                              ║
echo  ║  Ahora tienes estos archivos faciles de usar:               ║
echo  ║                                                              ║
echo  ║  🤖 ABRIR CHATBOT.bat     - Para usar el chatbot            ║
echo  ║  🧪 PROBAR CHATBOT.bat    - Para probar que funciona        ║
echo  ║  📦 CREAR EJECUTABLE.bat  - Para crear .exe                 ║
echo  ║  ❓ AYUDA.bat             - Para ver instrucciones          ║
echo  ║                                                              ║
echo  ║              ¡Solo haz doble click en cualquiera!           ║
echo  ║                                                              ║
echo  ╚══════════════════════════════════════════════════════════════╝
echo.
echo.
echo 🎉 ¡Listo para usar! Presiona cualquier tecla para continuar...
pause >nul

REM Preguntar si quiere abrir el chatbot ahora
echo.
set /p respuesta="¿Quieres abrir el chatbot ahora? (s/n): "
if /i "%respuesta%"=="s" (
    echo.
    echo ⏳ Abriendo chatbot...
    start "" "🤖 ABRIR CHATBOT.bat"
)

echo.
echo ¡Gracias por usar el Chatbot de Salud Mental!
echo.
pause
