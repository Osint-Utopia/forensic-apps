#!/usr/bin/env python3
"""
Chatbot de Salud Mental - Uli
Versión 2.0.0

Un chatbot inteligente para apoyo en salud mental que utiliza
técnicas de procesamiento de lenguaje natural y búsqueda semántica.

Autor: Desarrollado para el usuario
Fecha: 2025
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

# Añadir el directorio actual al path para importaciones
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    missing_packages = []
    
    try:
        import sklearn
    except ImportError:
        missing_packages.append('scikit-learn')
    
    try:
        import pandas
    except ImportError:
        missing_packages.append('pandas')
    
    try:
        import numpy
    except ImportError:
        missing_packages.append('numpy')
    
    try:
        from unidecode import unidecode
    except ImportError:
        missing_packages.append('unidecode')
    
    if missing_packages:
        error_msg = f"""
Faltan las siguientes dependencias:
{', '.join(missing_packages)}

Para instalarlas, ejecuta:
pip install {' '.join(missing_packages)}

O instala todas las dependencias con:
pip install -r requirements.txt
        """
        
        # Mostrar error en ventana si tkinter está disponible
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Dependencias faltantes", error_msg)
            root.destroy()
        except:
            pass
        
        print(error_msg)
        return False
    
    return True

def check_datasets():
    """Verifica que los datasets estén disponibles"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    
    required_files = [
        'simple_dataset.json',
        'combined_dataset.json'
    ]
    
    missing_files = []
    for file in required_files:
        file_path = os.path.join(data_dir, file)
        if not os.path.exists(file_path):
            missing_files.append(file)
    
    if missing_files:
        error_msg = f"""
Faltan los siguientes archivos de datos:
{', '.join(missing_files)}

Asegúrate de que los archivos JSON estén en el directorio 'data/'.
        """
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Archivos de datos faltantes", error_msg)
            root.destroy()
        except:
            pass
        
        print(error_msg)
        return False
    
    return True

def main():
    """Función principal de la aplicación"""
    print("Iniciando Chatbot de Salud Mental - Uli v2.0.0")
    print("=" * 50)
    
    # Verificar dependencias
    print("Verificando dependencias...")
    if not check_dependencies():
        print("Error: Dependencias faltantes. Saliendo.")
        sys.exit(1)
    
    # Verificar datasets
    print("Verificando archivos de datos...")
    if not check_datasets():
        print("Error: Archivos de datos faltantes. Saliendo.")
        sys.exit(1)
    
    print("Todas las verificaciones pasaron. Iniciando aplicación...")
    
    try:
        # Importar y ejecutar la aplicación
        from ui import MainWindow
        
        print("Creando ventana principal...")
        app = MainWindow()
        
        print("Aplicación lista. Mostrando interfaz...")
        app.run()
        
    except KeyboardInterrupt:
        print("\nAplicación interrumpida por el usuario.")
        sys.exit(0)
    
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        print(error_msg)
        
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("Error", error_msg)
            root.destroy()
        except:
            pass
        
        sys.exit(1)

if __name__ == "__main__":
    main()
