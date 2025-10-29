#!/bin/bash
# Script de instalación para Chatbot de Salud Mental

echo "=== INSTALADOR CHATBOT DE SALUD MENTAL ==="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado"
    echo "Por favor instala Python 3.8 o superior"
    exit 1
fi

echo "✓ Python 3 encontrado: $(python3 --version)"

# Verificar pip
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 no está instalado"
    exit 1
fi

echo "✓ pip3 encontrado"

# Instalar dependencias
echo ""
echo "Instalando dependencias de Python..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencias instaladas correctamente"
else
    echo "✗ Error instalando dependencias"
    echo "Intenta ejecutar manualmente: pip3 install -r requirements.txt"
    exit 1
fi

# Verificar tkinter (Linux)
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo ""
    echo "Verificando tkinter..."
    python3 -c "import tkinter" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo "⚠️  tkinter no está instalado"
        echo "Para instalarlo en Ubuntu/Debian:"
        echo "  sudo apt-get install python3-tk"
        echo ""
        echo "Para instalarlo en CentOS/RHEL:"
        echo "  sudo yum install tkinter"
        echo ""
        read -p "¿Quieres intentar instalarlo automáticamente? (s/n): " install_tk
        
        if [[ $install_tk =~ ^[SsYy]$ ]]; then
            if command -v apt-get &> /dev/null; then
                sudo apt-get update && sudo apt-get install -y python3-tk
            elif command -v yum &> /dev/null; then
                sudo yum install -y tkinter
            else
                echo "No se pudo instalar automáticamente. Instálalo manualmente."
            fi
        fi
    else
        echo "✓ tkinter disponible"
    fi
fi

# Hacer ejecutable el archivo principal
chmod +x main.py
chmod +x test_chatbot.py
chmod +x build_executable.py

echo ""
echo "=== INSTALACIÓN COMPLETADA ==="
echo ""
echo "Para ejecutar el chatbot:"
echo "  python3 main.py"
echo ""
echo "Para ejecutar pruebas:"
echo "  python3 test_chatbot.py"
echo ""
echo "Para crear ejecutable:"
echo "  python3 build_executable.py"
echo ""
echo "¡Disfruta usando el Chatbot de Salud Mental!"
