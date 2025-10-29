#!/bin/bash
# Instalador súper fácil para macOS - Chatbot de Salud Mental

# Configurar terminal
clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════╗"
echo "  ║                                                              ║"
echo "  ║           CHATBOT DE SALUD MENTAL - INSTALADOR FÁCIL         ║"
echo "  ║                                                              ║"
echo "  ║                    ¡Solo sigue los pasos!                   ║"
echo "  ║                                                              ║"
echo "  ╚══════════════════════════════════════════════════════════════╝"
echo ""
echo ""

# Cambiar al directorio del script
cd "$(dirname "$0")"

# Verificar macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este instalador es solo para macOS"
    echo ""
    echo "💡 Para Windows usa: INSTALAR_WINDOWS_FACIL.bat"
    read -p "Presiona Enter para cerrar..."
    exit 1
fi

echo "✅ Sistema macOS detectado"
echo ""

# Verificar Python3
echo "[PASO 1/3] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo ""
    echo "❌ Python 3 NO está instalado en tu Mac"
    echo ""
    echo "📥 NECESITAS INSTALAR PYTHON PRIMERO:"
    echo ""
    echo "   OPCIÓN 1 (Más Fácil):"
    echo "   1. Ve a: https://www.python.org/downloads/macos/"
    echo "   2. Descarga Python 3.11 o más nuevo"
    echo "   3. Instala normalmente (doble click en el .pkg)"
    echo "   4. Ejecuta este archivo otra vez"
    echo ""
    echo "   OPCIÓN 2 (Si tienes Homebrew):"
    echo "   1. Abre Terminal"
    echo "   2. Escribe: brew install python"
    echo "   3. Ejecuta este archivo otra vez"
    echo ""
    echo "💡 ¿Necesitas ayuda? Busca 'como instalar python mac' en YouTube"
    echo ""
    read -p "Presiona Enter para cerrar..."
    exit 1
fi

python3 --version
echo "✅ Python encontrado correctamente"
echo ""

# Verificar pip3
echo "[PASO 2/3] Verificando herramientas..."
if ! command -v pip3 &> /dev/null; then
    echo "⚠️  pip3 no encontrado, instalando..."
    python3 -m ensurepip --upgrade
fi

echo "✅ Herramientas listas"
echo ""

# Instalar dependencias
echo "[PASO 3/3] Instalando el chatbot..."
echo ""
echo "⏳ Esto puede tomar unos minutos..."
echo "⏳ NO cierres esta ventana..."
echo ""

# Actualizar pip
python3 -m pip install --upgrade pip > /dev/null 2>&1

# Instalar dependencias
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error instalando componentes"
    echo ""
    echo "🔧 POSIBLES SOLUCIONES:"
    echo "   1. Verifica tu conexión a internet"
    echo "   2. Si tienes problemas con tkinter:"
    echo "      brew install python-tk"
    echo "   3. O reinstala Python desde python.org"
    echo ""
    read -p "Presiona Enter para cerrar..."
    exit 1
fi

echo "✅ Chatbot instalado correctamente"
echo ""

# Crear accesos directos súper fáciles
echo "Creando accesos directos..."

# Ejecutar chatbot (SÚPER FÁCIL)
cat > "🤖 ABRIR CHATBOT.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
clear
echo ""
echo "⏳ Iniciando chatbot..."
echo "⏳ Se abrirá una ventana nueva..."
echo ""
python3 main.py
if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Error ejecutando chatbot"
    echo "💡 Ejecuta INSTALAR_MACOS_FACIL.command otra vez"
    read -p "Presiona Enter para cerrar..."
fi
EOF

# Probar chatbot (FÁCIL)
cat > "🧪 PROBAR CHATBOT.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
clear
echo ""
echo "⏳ Probando chatbot..."
echo ""
python3 test_chatbot.py
echo ""
echo "✅ Prueba completada"
read -p "Presiona Enter para cerrar..."
EOF

# Crear ejecutable (FÁCIL)
cat > "📦 CREAR APLICACION.command" << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
clear
echo ""
echo "⏳ Creando aplicación para macOS..."
echo "⏳ Esto puede tomar 5-10 minutos..."
echo "⏳ NO cierres esta ventana..."
echo ""
python3 build_executable_cross_platform.py
echo ""
echo "✅ Aplicación creada"
read -p "Presiona Enter para cerrar..."
EOF

# Ayuda (SÚPER FÁCIL)
cat > "❓ AYUDA.command" << 'EOF'
#!/bin/bash
clear
echo ""
echo "  ╔══════════════════════════════════════════════════════════════╗"
echo "  ║                                                              ║"
echo "  ║                    COMO USAR EL CHATBOT                     ║"
echo "  ║                                                              ║"
echo "  ╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "🤖 PARA USAR EL CHATBOT:"
echo "   - Doble click en: 🤖 ABRIR CHATBOT.command"
echo "   - Se abre una ventana con el chatbot"
echo "   - Escribe tu pregunta y presiona Enter"
echo ""
echo "🧪 PARA PROBAR QUE FUNCIONA:"
echo "   - Doble click en: 🧪 PROBAR CHATBOT.command"
echo ""
echo "📦 PARA CREAR APLICACIÓN .APP:"
echo "   - Doble click en: 📦 CREAR APLICACION.command"
echo "   - Espera 5-10 minutos"
echo "   - Se crea Chatbot Salud Mental.app"
echo ""
echo "🆘 SI TIENES PROBLEMAS:"
echo "   - Ejecuta INSTALAR_MACOS_FACIL.command otra vez"
echo "   - Verifica tu conexión a internet"
echo "   - Contacta soporte técnico"
echo ""
read -p "Presiona Enter para cerrar..."
EOF

# Hacer ejecutables todos los scripts
chmod +x "🤖 ABRIR CHATBOT.command"
chmod +x "🧪 PROBAR CHATBOT.command"
chmod +x "📦 CREAR APLICACION.command"
chmod +x "❓ AYUDA.command"

echo "✅ Accesos directos creados"
echo ""

# Verificar tkinter
echo "Verificando tkinter..."
python3 -c "import tkinter; print('✅ tkinter disponible')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  tkinter no disponible"
    echo ""
    echo "🔧 PARA INSTALAR TKINTER:"
    echo ""
    echo "   Si tienes Homebrew:"
    echo "   brew install python-tk"
    echo ""
    echo "   O reinstala Python desde python.org"
    echo ""
    read -p "¿Quieres que intente instalar tkinter con Homebrew? (s/n): " install_tk
    
    if [[ $install_tk =~ ^[SsYy]$ ]]; then
        if command -v brew &> /dev/null; then
            echo "Instalando tkinter con Homebrew..."
            brew install python-tk
        else
            echo "Homebrew no está instalado."
            echo "Instálalo desde: https://brew.sh"
            echo "O reinstala Python desde python.org"
        fi
    fi
else
    echo "✅ tkinter disponible"
fi

echo ""

# Probar instalación
echo "Probando instalación..."
python3 -c "import sys; sys.path.append('.'); from core.dataset_processor import DatasetProcessor; print('✅ Chatbot listo')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  Advertencia: Puede haber un problema menor"
    echo "💡 Prueba ejecutar: 🧪 PROBAR CHATBOT.command"
else
    echo "✅ Instalación verificada correctamente"
fi

echo ""
echo "  ╔══════════════════════════════════════════════════════════════╗"
echo "  ║                                                              ║"
echo "  ║                    ¡INSTALACIÓN COMPLETADA!                 ║"
echo "  ║                                                              ║"
echo "  ║  Ahora tienes estos archivos fáciles de usar:               ║"
echo "  ║                                                              ║"
echo "  ║  🤖 ABRIR CHATBOT.command     - Para usar el chatbot        ║"
echo "  ║  🧪 PROBAR CHATBOT.command    - Para probar que funciona    ║"
echo "  ║  📦 CREAR APLICACION.command  - Para crear .app             ║"
echo "  ║  ❓ AYUDA.command             - Para ver instrucciones      ║"
echo "  ║                                                              ║"
echo "  ║              ¡Solo haz doble click en cualquiera!           ║"
echo "  ║                                                              ║"
echo "  ╚══════════════════════════════════════════════════════════════╝"
echo ""
echo ""
echo "🎉 ¡Listo para usar! Presiona cualquier tecla para continuar..."
read -n 1 -s

# Preguntar si quiere abrir el chatbot ahora
echo ""
read -p "¿Quieres abrir el chatbot ahora? (s/n): " respuesta
if [[ $respuesta =~ ^[SsYy]$ ]]; then
    echo ""
    echo "⏳ Abriendo chatbot..."
    open "🤖 ABRIR CHATBOT.command"
fi

echo ""
echo "¡Gracias por usar el Chatbot de Salud Mental!"
echo ""
read -p "Presiona Enter para cerrar..."
