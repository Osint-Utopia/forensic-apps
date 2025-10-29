# Guía de Migración: De PDF a JSON Datasets

Esta guía te ayudará a migrar desde tu chatbot anterior (basado en PDFs) al nuevo sistema con datasets JSON.

## 🔄 Principales Diferencias

### Versión Anterior (v1.0)
- **Fuente de datos**: Archivos PDF
- **Búsqueda**: Texto literal con PyMuPDF
- **Interfaz**: tkinter básico
- **Idioma**: Solo español
- **Respuestas**: Fragmentos de texto del PDF

### Nueva Versión (v2.0)
- **Fuente de datos**: Datasets JSON estructurados
- **Búsqueda**: Semántica con TF-IDF y similitud coseno
- **Interfaz**: tkinter mejorado con chat conversacional
- **Idiomas**: Español e inglés
- **Respuestas**: Conversaciones completas y contextuales

## 📊 Comparación de Funcionalidades

| Característica | v1.0 (PDF) | v2.0 (JSON) |
|----------------|------------|-------------|
| Fuente de datos | PDF estático | JSON dinámico |
| Tipo de búsqueda | Palabras clave | Semántica |
| Precisión | Básica | Alta |
| Velocidad | Lenta | Rápida |
| Escalabilidad | Limitada | Alta |
| Mantenimiento | Difícil | Fácil |
| Multiidioma | No | Sí |
| Historial | No | Sí |
| Exportación | No | Sí |

## 🚀 Ventajas del Nuevo Sistema

### 1. **Búsqueda Inteligente**
```python
# Antes (v1.0): Búsqueda literal
if query.lower() in text.lower():
    return text

# Ahora (v2.0): Búsqueda semántica
similarity_score = cosine_similarity(query_vector, document_vectors)
return best_match_with_confidence
```

### 2. **Mejor Experiencia de Usuario**
- Chat conversacional en tiempo real
- Indicadores de confianza en respuestas
- Historial de conversaciones
- Interfaz más moderna y responsiva

### 3. **Datos Estructurados**
```json
{
  "question": "¿Qué es la ansiedad?",
  "answer": "La ansiedad es una respuesta natural...",
  "language": "es",
  "confidence": 0.85
}
```

### 4. **Escalabilidad**
- Fácil agregar nuevos datasets
- Soporte para múltiples idiomas
- Arquitectura modular

## 📁 Migración de Datos

### Si Tienes PDFs Adicionales

1. **Extraer texto del PDF**:
```python
import fitz  # PyMuPDF

def extract_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)
    content = []
    
    for page in doc:
        text = page.get_text()
        content.append(text)
    
    return "\n".join(content)
```

2. **Convertir a formato JSON**:
```python
def create_json_dataset(pdf_content):
    # Dividir en secciones Q&A
    sections = split_into_qa_pairs(pdf_content)
    
    dataset = []
    for question, answer in sections:
        dataset.append({
            "question": question,
            "answer": answer,
            "language": "es",
            "source": "pdf_migration"
        })
    
    return dataset
```

3. **Integrar en el nuevo sistema**:
```python
# En dataset_processor.py
def load_custom_dataset(self, file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Procesar y añadir al sistema
    self.conversations.extend(data)
```

## 🛠️ Pasos de Migración

### Paso 1: Backup de la Versión Anterior
```bash
# Respaldar tu chatbot anterior
cp -r chatbot_anterior/ chatbot_backup/
```

### Paso 2: Instalar Nueva Versión
```bash
# Descomprimir nueva versión
tar -xzf chatbot_salud_mental_v2.tar.gz

# Instalar dependencias
cd chatbot_salud_mental/
pip3 install -r requirements.txt
```

### Paso 3: Migrar Configuraciones
Si tenías configuraciones personalizadas, actualiza `utils/config.py`:

```python
# Ejemplo de migración de configuraciones
APP_CONFIG = {
    'title': 'Tu Título Personalizado',
    'window_size': '1000x700',  # Si prefieres ventana más grande
}

UI_MESSAGES = {
    'es': {
        'welcome': 'Tu mensaje de bienvenida personalizado',
        # ... otros mensajes
    }
}
```

### Paso 4: Probar el Sistema
```bash
# Ejecutar pruebas
python3 test_chatbot.py

# Probar interfaz
python3 main.py
```

## 🔧 Personalización Avanzada

### Agregar Tus Propios Datos

1. **Crear dataset personalizado**:
```json
[
  {
    "question": "Tu pregunta específica",
    "answer": "Tu respuesta específica",
    "language": "es",
    "source": "custom_data"
  }
]
```

2. **Modificar el procesador**:
```python
# En core/dataset_processor.py
def load_custom_dataset(self, file_path):
    # Tu lógica de carga personalizada
    pass
```

### Ajustar Algoritmo de Búsqueda

```python
# En core/search_engine.py
class SemanticSearchEngine:
    def __init__(self):
        # Personalizar parámetros TF-IDF
        self.vectorizer_params = {
            'max_features': 10000,  # Más características
            'ngram_range': (1, 3),  # Incluir trigramas
            'min_df': 2,           # Frecuencia mínima
        }
```

## 📈 Mejoras de Rendimiento

### Optimizaciones Implementadas

1. **Vectorización Eficiente**:
   - Cache de vectores TF-IDF
   - Procesamiento por lotes
   - Índices optimizados

2. **Interfaz Responsiva**:
   - Procesamiento asíncrono
   - Indicadores de progreso
   - Threading para operaciones pesadas

3. **Gestión de Memoria**:
   - Carga lazy de datasets
   - Limpieza automática de cache
   - Optimización de estructuras de datos

## 🐛 Solución de Problemas Comunes

### Error: "Dataset no encontrado"
```bash
# Verificar archivos
ls -la data/
# Debe mostrar: simple_dataset.json, combined_dataset.json
```

### Error: "Baja confianza en respuestas"
```python
# Ajustar umbral en utils/config.py
SEARCH_CONFIG = {
    'min_similarity_threshold': 0.05,  # Reducir umbral
}
```

### Error: "Interfaz no responde"
```python
# Verificar threading en ui/chat_widget.py
# Asegurar que operaciones pesadas usen hilos separados
```

## 📚 Recursos Adicionales

### Documentación
- `README.md`: Guía completa de uso
- `test_chatbot.py`: Ejemplos de funcionamiento
- Comentarios en código: Explicaciones detalladas

### Comunidad y Soporte
- Ejecutar pruebas para diagnosticar problemas
- Revisar logs de error en consola
- Consultar documentación de dependencias

## 🎯 Próximos Pasos

### Después de la Migración

1. **Familiarízate** con la nueva interfaz
2. **Prueba** diferentes tipos de consultas
3. **Personaliza** configuraciones según tus necesidades
4. **Agrega** tus propios datasets si es necesario
5. **Crea** un ejecutable para distribución

### Futuras Mejoras Posibles

- Integración con APIs de IA (GPT, Claude)
- Soporte para más idiomas
- Interfaz web con Flask/Django
- Base de datos para persistencia
- Análisis de sentimientos
- Respuestas generativas

---

**¡Felicidades por migrar al nuevo sistema!** 🎉

El nuevo chatbot te proporcionará una experiencia mucho más rica y funcional. Si tienes preguntas durante la migración, consulta la documentación o ejecuta las pruebas para verificar que todo funcione correctamente.
