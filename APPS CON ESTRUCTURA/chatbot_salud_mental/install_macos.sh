#!/bin/bash
# Script de instalación para macOS - Chatbot de Salud Mental

echo "==============================================="
echo "INSTALADOR CHATBOT DE SALUD MENTAL - macOS"
echo "==============================================="

echo ""

# Verificar si estamos en macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Este script es solo para macOS"
    exit 1
fi

echo "✓ Sistema macOS detectado"

# Verificar Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    echo ""
    echo "Opciones de instalación:"
    echo "1. Instalar desde python.org:"
    echo "   https://www.python.org/downloads/macos/"
    echo ""
    echo "2. Instalar con Homebrew:"
    echo "   brew install python"
    echo ""
    echo "3. Instalar con pyenv (recomendado para desarrolladores):"
    echo "   curl https://pyenv.run | bash"
    echo "   pyenv install 3.11.0"
    exit 1
fi

echo "✓ Python 3 encontrado: $(python3 --version)"

# Verificar pip3
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 no está instalado"
    echo "Instalando pip3..."
    python3 -m ensurepip --upgrade
fi

echo "✓ pip3 encontrado"

# Actualizar pip
echo ""
echo "Actualizando pip..."
python3 -m pip install --upgrade pip

# Instalar dependencias
echo ""
echo "Instalando dependencias de Python..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas correctamente"
else
    echo "❌ Error instalando dependencias"
    echo ""
    echo "Intenta ejecutar manualmente:"
    echo "pip3 install -r requirements.txt"
    echo ""
    echo "Si tienes problemas con tkinter en macOS:"
    echo "brew install python-tk"
    exit 1
fi

# Verificar tkinter
echo ""
echo "Verificando tkinter..."
python3 -c "import tkinter; print('✓ tkinter disponible')" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "⚠️  tkinter no disponible"
    echo ""
    echo "Para instalar tkinter en macOS:"
    echo ""
    echo "Opción 1 - Con Homebrew:"
    echo "  brew install python-tk"
    echo ""
    echo "Opción 2 - Reinstalar Python con tkinter:"
    echo "  Descarga Python desde python.org (incluye tkinter)"
    echo ""
    read -p "¿Quieres intentar instalar tkinter con Homebrew? (s/n): " install_tk
    
    if [[ $install_tk =~ ^[SsYy]$ ]]; then
        if command -v brew &> /dev/null; then
            echo "Instalando tkinter con Homebrew..."
            brew install python-tk
        else
            echo "Homebrew no está instalado. Instálalo desde:"
            echo "https://brew.sh"
        fi
    fi
else
    echo "✓ tkinter disponible"
fi

# Crear scripts de ejecución para macOS
echo ""
echo "Creando scripts de ejecución..."

# Script para ejecutar el chatbot
cat > ejecutar_chatbot.command << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 main.py
read -p "Presiona Enter para cerrar..."
EOF

# Script para ejecutar pruebas
cat > ejecutar_pruebas.command << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 test_chatbot.py
read -p "Presiona Enter para cerrar..."
EOF

# Script para crear ejecutable
cat > crear_ejecutable.command << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
python3 build_executable.py
read -p "Presiona Enter para cerrar..."
EOF

# Hacer ejecutables los scripts
chmod +x ejecutar_chatbot.command
chmod +x ejecutar_pruebas.command  
chmod +x crear_ejecutable.command
chmod +x main.py
chmod +x test_chatbot.py
chmod +x build_executable.py

echo "✓ Scripts de ejecución creados"

# Crear aplicación .app (opcional)
echo ""
read -p "¿Quieres crear una aplicación .app para macOS? (s/n): " create_app

if [[ $create_app =~ ^[SsYy]$ ]]; then
    echo "Creando aplicación macOS..."
    
    APP_NAME="Chatbot Salud Mental"
    APP_DIR="$APP_NAME.app"
    
    mkdir -p "$APP_DIR/Contents/MacOS"
    mkdir -p "$APP_DIR/Contents/Resources"
    
    # Info.plist
    cat > "$APP_DIR/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>chatbot</string>
    <key>CFBundleIdentifier</key>
    <string>com.saludmental.chatbot</string>
    <key>CFBundleName</key>
    <string>$APP_NAME</string>
    <key>CFBundleVersion</key>
    <string>2.0</string>
    <key>CFBundleShortVersionString</key>
    <string>2.0</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.14</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
EOF

    # Script ejecutable
    cat > "$APP_DIR/Contents/MacOS/chatbot" << EOF
#!/bin/bash
cd "\$(dirname "\$0")/../../../"
python3 main.py
EOF

    chmod +x "$APP_DIR/Contents/MacOS/chatbot"
    
    echo "✓ Aplicación $APP_DIR creada"
    echo "  Puedes arrastrarla a /Applications si quieres"
fi

echo ""
echo "==============================================="
echo "INSTALACIÓN COMPLETADA PARA macOS"
echo "==============================================="
echo ""
echo "Para usar el chatbot:"
echo "  - Doble clic en: ejecutar_chatbot.command"
echo "  - O desde terminal: python3 main.py"
echo ""
echo "Para ejecutar pruebas:"
echo "  - Doble clic en: ejecutar_pruebas.command"
echo "  - O desde terminal: python3 test_chatbot.py"
echo ""
echo "Para crear ejecutable:"
echo "  - Doble clic en: crear_ejecutable.command"
echo ""
if [[ $create_app =~ ^[SsYy]$ ]]; then
echo "Para usar la aplicación nativa:"
echo "  - Doble clic en: $APP_NAME.app"
echo ""
fi
echo "¡Disfruta usando el Chatbot de Salud Mental!"
echo ""
