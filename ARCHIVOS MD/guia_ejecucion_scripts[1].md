# Guía Paso a Paso para Ejecutar Scripts de Procesamiento

## MÉTODO RECOMENDADO: CREAR ARCHIVOS .PY

### Paso 1: Preparar el Entorno
```bash
# 1. Abrir terminal/símbolo del sistema
# 2. Navegar a donde quieres crear tu proyecto
cd C:\Mi_Proyecto_RAG
# o en Linux/Mac:
cd ~/Mi_Proyecto_RAG

# 3. Crear carpeta para documentos
mkdir documentos

# 4. Instalar dependencias
pip install sentence-transformers PyPDF2 python-docx numpy
```

### Paso 2: Crear Archivo procesar_documentos.py
**NO escribas línea por línea en consola**. Crea un archivo de texto:

1. Abre tu editor favorito (Notepad++, VSCode, incluso Bloc de notas)
2. Copia y pega TODO el código siguiente:

```python
# Archivo: procesar_documentos.py
import os
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer
import pickle

def leer_pdf(ruta):
    try:
        with open(ruta, 'rb') as archivo:
            lector = PyPDF2.PdfReader(archivo)
            texto = ""
            for pagina in lector.pages:
                texto += pagina.extract_text()
        return texto
    except Exception as e:
        print(f"Error leyendo PDF {ruta}: {e}")
        return ""

def leer_word(ruta):
    try:
        doc = docx.Document(ruta)
        texto = ""
        for parrafo in doc.paragraphs:
            texto += parrafo.text + "\n"
        return texto
    except Exception as e:
        print(f"Error leyendo Word {ruta}: {e}")
        return ""

def dividir_texto(texto, tamaño_chunk=300):
    """Divide texto en fragmentos manejables"""
    if not texto.strip():
        return []
    
    palabras = texto.split()
    chunks = []
    
    for i in range(0, len(palabras), tamaño_chunk):
        chunk = " ".join(palabras[i:i + tamaño_chunk])
        if len(chunk.strip()) > 50:
            chunks.append(chunk.strip())
    
    return chunks

def procesar_documentos():
    print("=== PROCESADOR DE DOCUMENTOS LEGALES ===")
    
    # Configurar rutas
    carpeta_documentos = "./documentos"
    ruta_salida = "./mis_documentos_procesados.pkl"
    
    # Permitir ruta personalizada
    ruta_personalizada = input("¿Quieres guardar en otra ruta? (Enter para usar actual): ").strip()
    if ruta_personalizada:
        ruta_salida = ruta_personalizada
    
    print(f"Carpeta de documentos: {os.path.abspath(carpeta_documentos)}")
    print(f"Archivo de salida: {os.path.abspath(ruta_salida)}")
    
    # Verificar carpeta existe
    if not os.path.exists(carpeta_documentos):
        print(f"ERROR: No existe la carpeta {carpeta_documentos}")
        print("Crea la carpeta 'documentos' y pon tus archivos ahí")
        return
    
    # Listar archivos disponibles
    archivos = [f for f in os.listdir(carpeta_documentos) 
                if f.endswith(('.pdf', '.docx', '.txt'))]
    
    if not archivos:
        print("ERROR: No se encontraron archivos PDF, DOCX o TXT en la carpeta documentos")
        return
    
    print(f"\nArchivos encontrados: {len(archivos)}")
    for archivo in archivos:
        print(f"  - {archivo}")
    
    continuar = input("\n¿Continuar procesamiento? (s/n): ").lower()
    if continuar != 's':
        return
    
    # Cargar modelo
    print("\n1. Cargando modelo de IA (puede tardar en primera ejecución)...")
    try:
        model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
        print("   ✓ Modelo cargado exitosamente")
    except Exception as e:
        print(f"   ✗ Error cargando modelo: {e}")
        print("   Intentando modelo alternativo...")
        model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    # Procesar archivos
    print("\n2. Procesando documentos...")
    textos = []
    nombres_archivos = []
    
    for archivo in archivos:
        ruta_archivo = os.path.join(carpeta_documentos, archivo)
        print(f"   Procesando: {archivo}")
        
        try:
            if archivo.endswith('.pdf'):
                texto = leer_pdf(ruta_archivo)
            elif archivo.endswith('.docx'):
                texto = leer_word(ruta_archivo)
            elif archivo.endswith('.txt'):
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    texto = f.read()
            
            if texto.strip():
                parrafos = dividir_texto(texto)
                textos.extend(parrafos)
                nombres_archivos.extend([archivo] * len(parrafos))
                print(f"     → {len(parrafos)} fragmentos extraídos")
            else:
                print(f"     → Archivo vacío o no se pudo leer")
                
        except Exception as e:
            print(f"     ✗ Error procesando {archivo}: {e}")
    
    if not textos:
        print("ERROR: No se pudo extraer texto de ningún archivo")
        return
    
    # Crear embeddings
    print(f"\n3. Creando embeddings para {len(textos)} fragmentos...")
    try:
        embeddings = model.encode(textos, show_progress_bar=True)
        print("   ✓ Embeddings creados exitosamente")
    except Exception as e:
        print(f"   ✗ Error creando embeddings: {e}")
        return
    
    # Guardar datos
    print(f"\n4. Guardando datos en: {ruta_salida}")
    try:
        datos = {
            'textos': textos,
            'embeddings': embeddings,
            'archivos': nombres_archivos,
            'modelo_usado': model.get_sentence_embedding_dimension()
        }
        
        with open(ruta_salida, 'wb') as f:
            pickle.dump(datos, f)
        
        print("   ✓ Datos guardados exitosamente")
        
    except Exception as e:
        print(f"   ✗ Error guardando: {e}")
        return
    
    # Resumen
    print(f"\n=== PROCESAMIENTO COMPLETO ===")
    print(f"Archivos procesados: {len(set(nombres_archivos))}")
    print(f"Fragmentos creados: {len(textos)}")
    print(f"Tamaño del archivo: {os.path.getsize(ruta_salida) / 1024 / 1024:.1f} MB")
    print(f"Ubicación: {os.path.abspath(ruta_salida)}")

if __name__ == "__main__":
    procesar_documentos()
```

3. Guárdalo como `procesar_documentos.py` en tu carpeta del proyecto

### Paso 3: Ejecutar el Script
```bash
# En terminal/símbolo del sistema, desde la carpeta del proyecto:
python procesar_documentos.py
```

## PARA GUARDAR EN RUTA EXTERNA

### Opción 1: El script te pregunta
Cuando ejecutes el script, te preguntará:
```
¿Quieres guardar en otra ruta? (Enter para usar actual):
```

Puedes escribir:
```
D:\Mis_Embeddings\documentos_procesados.pkl
# o
/home/usuario/backup/mis_docs.pkl
```

### Opción 2: Modificar el script
Cambia esta línea en el código:
```python
# En lugar de:
ruta_salida = "./mis_documentos_procesados.pkl"

# Pon tu ruta específica:
ruta_salida = "D:/Mi_Backup/documentos_procesados.pkl"
```

## SCRIPT DE BÚSQUEDA (ARCHIVO SEPARADO)

Crea otro archivo llamado `buscar_documentos.py`:

```python
# Archivo: buscar_documentos.py
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer
import os

def buscar_documentos():
    print("=== BUSCADOR DE DOCUMENTOS LEGALES ===")
    
    # Buscar archivo de datos
    archivo_datos = "./mis_documentos_procesados.pkl"
    
    if not os.path.exists(archivo_datos):
        ruta_personalizada = input("Archivo no encontrado. Ingresa la ruta completa: ").strip()
        if os.path.exists(ruta_personalizada):
            archivo_datos = ruta_personalizada
        else:
            print("ERROR: Archivo no encontrado")
            return
    
    print(f"Cargando datos desde: {archivo_datos}")
    
    # Cargar datos
    try:
        with open(archivo_datos, 'rb') as f:
            datos = pickle.load(f)
        
        textos = datos['textos']
        embeddings = datos['embeddings']
        archivos = datos['archivos']
        
        print(f"✓ Base de datos cargada: {len(textos)} fragmentos")
        
    except Exception as e:
        print(f"ERROR cargando datos: {e}")
        return
    
    # Cargar modelo
    print("Cargando modelo de IA...")
    try:
        model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
    except:
        model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
    
    # Búsqueda interactiva
    print("\n=== SISTEMA DE BÚSQUEDA LISTO ===")
    print("Escribe tu consulta (o 'salir' para terminar)")
    
    while True:
        consulta = input("\n🔍 Buscar: ").strip()
        
        if consulta.lower() in ['salir', 'exit', 'quit']:
            break
        
        if not consulta:
            continue
        
        try:
            # Crear embedding de consulta
            consulta_embedding = model.encode([consulta])
            
            # Calcular similitudes
            similitudes = np.dot(embeddings, consulta_embedding.T).flatten()
            
            # Top 3 resultados
            indices_mejores = np.argsort(similitudes)[-3:][::-1]
            
            print(f"\n--- Resultados para: '{consulta}' ---")
            
            for i, idx in enumerate(indices_mejores, 1):
                if similitudes[idx] > 0.3:  # Umbral mínimo
                    print(f"\n{i}. 📄 {archivos[idx]}")
                    print(f"   🎯 Relevancia: {similitudes[idx]:.3f}")
                    print(f"   📝 Fragmento:")
                    print(f"   {textos[idx][:300]}...")
                else:
                    print(f"\n{i}. Sin resultados relevantes (similitud: {similitudes[idx]:.3f})")
            
        except Exception as e:
            print(f"Error en búsqueda: {e}")

if __name__ == "__main__":
    buscar_documentos()
```

## INTEGRACIÓN CON TU INTERFAZ DE IA

Si usas una interfaz gráfica para tu IA, puedes:

1. **Ejecutar los scripts por separado** para generar el archivo .pkl
2. **Importar las funciones** en tu interfaz:

```python
# En tu interfaz de IA, agregar:
import sys
sys.path.append('ruta/a/tus/scripts')

from buscar_documentos import buscar_documentos
```

¿Te ayudo con algún paso específico o tienes dudas sobre la ejecución?