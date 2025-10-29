# Diseño del Chatbot de Salud Mental Mejorado

## Análisis de Requisitos

### Situación Actual
- **Chatbot anterior**: Búsqueda simple en PDFs con tkinter
- **Limitaciones**: Búsqueda básica por palabras clave, interfaz simple
- **Nuevos recursos**: Datasets JSON ricos en conversaciones de salud mental

### Objetivos del Nuevo Chatbot
1. **Búsqueda semántica inteligente** en lugar de búsqueda por palabras clave
2. **Interfaz moderna** con mejor experiencia de usuario
3. **Soporte multiidioma** (español e inglés)
4. **Respuestas contextuales** basadas en similitud semántica
5. **Arquitectura modular** para fácil mantenimiento

## Arquitectura Propuesta

### Componentes Principales

#### 1. **Procesador de Datasets**
- **Función**: Cargar y procesar los datasets JSON
- **Responsabilidades**:
  - Parsear archivos JSON
  - Normalizar formato de conversaciones
  - Crear índice de búsqueda
  - Manejar múltiples idiomas

#### 2. **Motor de Búsqueda Semántica**
- **Función**: Encontrar respuestas relevantes basadas en similitud
- **Tecnologías**:
  - TF-IDF para vectorización básica
  - Similitud coseno para ranking
  - Preprocesamiento de texto (stemming, stop words)

#### 3. **Interfaz de Usuario**
- **Tecnología**: Tkinter mejorado con elementos modernos
- **Características**:
  - Chat conversacional
  - Historial de conversación
  - Configuraciones de idioma
  - Indicadores de confianza en respuestas

#### 4. **Gestor de Conversación**
- **Función**: Mantener contexto y flujo de conversación
- **Responsabilidades**:
  - Historial de mensajes
  - Contexto de conversación
  - Sugerencias de seguimiento

### Flujo de Datos

```
Usuario Input → Preprocesamiento → Motor Búsqueda → Ranking Respuestas → Interfaz Usuario
     ↑                                                                        ↓
     ←─────────────────── Historial Conversación ←─────────────────────────────
```

## Estructura de Archivos

```
chatbot_salud_mental/
├── main.py                 # Punto de entrada principal
├── core/
│   ├── __init__.py
│   ├── dataset_processor.py    # Procesamiento de datasets
│   ├── search_engine.py        # Motor de búsqueda semántica
│   └── conversation_manager.py # Gestión de conversaciones
├── ui/
│   ├── __init__.py
│   ├── main_window.py          # Ventana principal
│   └── chat_widget.py          # Widget de chat
├── data/
│   ├── simple_dataset.json     # Dataset en español
│   └── combined_dataset.json   # Dataset en inglés
├── utils/
│   ├── __init__.py
│   ├── text_processing.py      # Utilidades de procesamiento de texto
│   └── config.py               # Configuraciones
└── requirements.txt            # Dependencias
```

## Tecnologías y Librerías

### Librerías Principales
- **tkinter**: Interfaz gráfica (ya incluida en Python)
- **scikit-learn**: TF-IDF y similitud coseno
- **nltk**: Procesamiento de lenguaje natural
- **pandas**: Manipulación de datos
- **json**: Procesamiento de datasets

### Librerías Adicionales
- **unidecode**: Normalización de texto
- **re**: Expresiones regulares
- **threading**: Para operaciones asíncronas

## Características Técnicas

### 1. **Búsqueda Semántica**
- Vectorización TF-IDF de preguntas y respuestas
- Cálculo de similitud coseno
- Ranking por relevancia
- Umbral de confianza configurable

### 2. **Procesamiento de Texto**
- Normalización de caracteres especiales
- Eliminación de stop words
- Stemming/lemmatización
- Manejo de múltiples idiomas

### 3. **Interfaz de Usuario**
- Chat en tiempo real
- Historial persistente
- Indicadores de carga
- Configuraciones de usuario

### 4. **Gestión de Datos**
- Carga eficiente de datasets
- Caché de vectorizaciones
- Índices optimizados
- Respaldo de conversaciones

## Ventajas del Nuevo Diseño

1. **Escalabilidad**: Fácil agregar nuevos datasets
2. **Precisión**: Búsqueda semántica vs. palabras clave
3. **Usabilidad**: Interfaz conversacional moderna
4. **Mantenibilidad**: Arquitectura modular
5. **Extensibilidad**: Base para futuras mejoras (IA, ML)

## Próximos Pasos

1. Implementar procesador de datasets
2. Desarrollar motor de búsqueda semántica
3. Crear interfaz de usuario mejorada
4. Integrar componentes y testing
5. Empaquetado como ejecutable

Este diseño proporciona una base sólida para un chatbot de salud mental más inteligente y útil, manteniendo la simplicidad de uso pero mejorando significativamente las capacidades técnicas.
