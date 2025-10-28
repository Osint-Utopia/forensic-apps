# Explicación del Código de Embeddings Python

## ¿QUÉ HACE EL CÓDIGO?

### 1. Instalación de Sentence Transformers
```bash
pip install sentence-transformers
```
**Qué hace**: Instala la librería que convierte texto en vectores numéricos (embeddings).

### 2. Importar y Cargar Modelo
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
```
**Qué hace**: 
- Descarga un modelo de IA especializado en español (unos 400MB)
- Lo carga en memoria para procesar tus documentos
- Este modelo "entiende" el significado de frases en español

### 3. Ejemplo Básico de Uso
```python
# Tus documentos de ejemplo
documentos = [
    "El artículo 123 de la Constitución establece derechos laborales",
    "La grafoscopía es el análisis científico de la escritura",
    "El peritaje balístico examina armas y proyectiles"
]

# El modelo convierte cada documento en números
embeddings = model.encode(documentos)
print(f"Cada documento se convierte en {len(embeddings[0])} números")
```

## CÓMO USAR CON TUS PROPIOS DOCUMENTOS

### Paso 1: Preparar Estructura de Carpetas
```
Mi_Proyecto/
├── documentos/
│   ├── codigo_civil.pdf
│   ├── ley_amparo.pdf
│   ├── dictamen_grafoscopico.docx
│   └── jurisprudencia.txt
├── procesar_documentos.py
└── buscar_documentos.py
```

### Paso 2: Script Completo para Procesar TUS Documentos
```python
# Archivo: procesar_documentos.py
import os
import PyPDF2
import docx
from sentence_transformers import SentenceTransformer
import pickle

def procesar_mis_documentos():
    # 1. Cargar modelo (se descarga automáticamente la primera vez)
    print("Cargando modelo de IA...")
    model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
    
    # 2. Carpeta donde tienes TUS documentos
    carpeta_documentos = "./documentos"
    
    # 3. Leer todos tus archivos
    textos = []
    nombres_archivos = []
    
    for archivo in os.listdir(carpeta_documentos):
        ruta_archivo = os.path.join(carpeta_documentos, archivo)
        print(f"Procesando: {archivo}")
        
        # Leer según tipo de archivo
        if archivo.endswith('.pdf'):
            texto = leer_pdf(ruta_archivo)
        elif archivo.endswith('.docx'):
            texto = leer_word(ruta_archivo)
        elif archivo.endswith('.txt'):
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                texto = f.read()
        else:
            continue
        
        # Dividir en párrafos para mejor búsqueda
        parrafos = dividir_texto(texto)
        textos.extend(parrafos)
        nombres_archivos.extend([archivo] * len(parrafos))
    
    # 4. Convertir todos los textos en vectores numéricos
    print(f"Convirtiendo {len(textos)} fragmentos en embeddings...")
    embeddings = model.encode(textos, show_progress_bar=True)
    
    # 5. Guardar todo para uso posterior
    with open('mis_documentos_procesados.pkl', 'wb') as f:
        pickle.dump({
            'textos': textos,
            'embeddings': embeddings,
            'archivos': nombres_archivos
        }, f)
    
    print("¡Procesamiento completado!")
    print(f"Se procesaron {len(textos)} fragmentos de {len(set(nombres_archivos))} archivos")

def leer_pdf(ruta):
    with open(ruta, 'rb') as archivo:
        lector = PyPDF2.PdfReader(archivo)
        texto = ""
        for pagina in lector.pages:
            texto += pagina.extract_text()
    return texto

def leer_word(ruta):
    doc = docx.Document(ruta)
    texto = ""
    for parrafo in doc.paragraphs:
        texto += parrafo.text + "\n"
    return texto

def dividir_texto(texto, tamaño_chunk=300):
    """Divide texto en fragmentos de 300 palabras aprox."""
    palabras = texto.split()
    chunks = []
    
    for i in range(0, len(palabras), tamaño_chunk):
        chunk = " ".join(palabras[i:i + tamaño_chunk])
        if len(chunk.strip()) > 50:  # Solo chunks con contenido
            chunks.append(chunk.strip())
    
    return chunks

# Ejecutar procesamiento
if __name__ == "__main__":
    procesar_mis_documentos()
```

### Paso 3: Script para Buscar en TUS Documentos
```python
# Archivo: buscar_documentos.py
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

def buscar_en_mis_documentos():
    # 1. Cargar modelo y datos procesados
    model = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')
    
    with open('mis_documentos_procesados.pkl', 'rb') as f:
        datos = pickle.load(f)
    
    textos = datos['textos']
    embeddings = datos['embeddings']
    archivos = datos['archivos']
    
    print("Sistema de búsqueda listo!")
    print(f"Base de datos: {len(textos)} fragmentos de tus documentos")
    
    # 2. Búsqueda interactiva
    while True:
        consulta = input("\n¿Qué quieres buscar? (o 'salir' para terminar): ")
        
        if consulta.lower() == 'salir':
            break
        
        # Convertir consulta en vector
        consulta_embedding = model.encode([consulta])
        
        # Calcular similitudes con todos los documentos
        similitudes = np.dot(embeddings, consulta_embedding.T).flatten()
        
        # Obtener los 3 más similares
        indices_mejores = np.argsort(similitudes)[-3:][::-1]
        
        print(f"\n--- Resultados para: '{consulta}' ---")
        for i, idx in enumerate(indices_mejores, 1):
            print(f"\n{i}. Archivo: {archivos[idx]}")
            print(f"   Similitud: {similitudes[idx]:.3f}")
            print(f"   Texto: {textos[idx][:200]}...")

if __name__ == "__main__":
    buscar_en_mis_documentos()
```

## INSTRUCCIONES DE USO

### 1. Preparación (Solo una vez)
```bash
# Crear carpeta del proyecto
mkdir Mi_RAG_Legal
cd Mi_RAG_Legal

# Crear subcarpeta para documentos
mkdir documentos

# Instalar dependencias
pip install sentence-transformers PyPDF2 python-docx numpy
```

### 2. Colocar Tus Documentos
```bash
# Copiar tus archivos a la carpeta documentos/
cp /ruta/a/tus/archivos/* ./documentos/
```

### 3. Procesar Documentos (Solo una vez)
```bash
python procesar_documentos.py
```
**Qué pasa**: 
- Lee todos tus PDFs, Word y TXT
- Los convierte en vectores numéricos
- Guarda todo en un archivo .pkl

### 4. Buscar en Tus Documentos
```bash
python buscar_documentos.py
```
**Qué pasa**:
- Te permite hacer preguntas en español
- Encuentra los fragmentos más relevantes
- Te muestra de qué archivo vienen

## EJEMPLO PRÁCTICO

```
¿Qué quieres buscar? derechos del trabajador

--- Resultados para: 'derechos del trabajador' ---

1. Archivo: ley_federal_trabajo.pdf
   Similitud: 0.847
   Texto: Artículo 25. El escrito en que consten las condiciones de trabajo deberá contener: I. Nombre, nacionalidad, edad, sexo, estado civil, Clave Única de Registro de Población, domicilio del trabajador y del patrón...

2. Archivo: codigo_civil.pdf
   Similitud: 0.723
   Texto: Los contratos de trabajo se rigen por las disposiciones especiales de la materia y por las normas generales de este código...
```

## VENTAJAS DE ESTE SISTEMA

1. **Completamente local**: No envía datos a internet
2. **Funciona sin conexión**: Una vez instalado, no necesita internet
3. **Busca por significado**: No solo palabras exactas, entiende contexto
4. **Procesa cualquier formato**: PDF, Word, texto plano
5. **Rápido**: Búsquedas en milisegundos una vez procesado

¿Te queda más claro cómo funciona y cómo usarlo con tus propios documentos?