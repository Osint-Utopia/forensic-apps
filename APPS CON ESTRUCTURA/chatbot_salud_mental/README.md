# Chatbot de Salud Mental - Uli v2.0

Un chatbot inteligente para apoyo en salud mental que utiliza técnicas avanzadas de procesamiento de lenguaje natural y búsqueda semántica para proporcionar respuestas relevantes y útiles.

## 🌟 Características Principales

- **Búsqueda Semántica Avanzada**: Utiliza TF-IDF y similitud coseno para encontrar respuestas relevantes
- **Soporte Multiidioma**: Funciona en español e inglés
- **Interfaz Conversacional**: Chat intuitivo con historial de conversaciones
- **Procesamiento Inteligente**: Normalización de texto, eliminación de stop words y detección de idioma
- **Gestión de Conversaciones**: Historial persistente y estadísticas de uso
- **Exportación de Datos**: Guarda y carga conversaciones en formato JSON

## 📋 Requisitos del Sistema

- **Python 3.8+**
- **Sistema Operativo**: Windows, macOS, Linux
- **Memoria RAM**: Mínimo 2GB recomendado
- **Espacio en Disco**: 500MB para instalación completa

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Linux/macOS)
```bash
chmod +x install.sh
./install.sh
```

### Opción 2: Instalación Manual
```bash
# 1. Instalar dependencias
pip3 install -r requirements.txt

# 2. Instalar tkinter (si no está disponible)
# Ubuntu/Debian:
sudo apt-get install python3-tk

# 3. Ejecutar aplicación
python3 main.py
```

## 📁 Estructura del Proyecto

```
chatbot_salud_mental/
├── main.py                     # Punto de entrada principal
├── requirements.txt            # Dependencias de Python
├── README.md                   # Este archivo
├── test_chatbot.py            # Script de pruebas
├── build_executable.py        # Generador de ejecutable
├── install.sh                 # Script de instalación
├── core/                      # Componentes principales
│   ├── dataset_processor.py   # Procesamiento de datasets
│   ├── search_engine.py       # Motor de búsqueda semántica
│   └── conversation_manager.py # Gestión de conversaciones
├── ui/                        # Interfaz de usuario
│   ├── main_window.py         # Ventana principal
│   └── chat_widget.py         # Widget de chat
├── utils/                     # Utilidades
│   ├── config.py              # Configuraciones
│   └── text_processing.py     # Procesamiento de texto
└── data/                      # Datasets
    ├── simple_dataset.json    # Dataset en español
    └── combined_dataset.json  # Dataset en inglés
```

## 🎯 Uso de la Aplicación

### Inicio Rápido
1. **Ejecutar**: `python3 main.py`
2. **Esperar**: La aplicación cargará los datasets automáticamente
3. **Conversar**: Escribe tu pregunta en el área de texto
4. **Enviar**: Presiona Enter o haz clic en "Enviar"

### Funciones Principales

#### 💬 Chat Conversacional
- Escribe preguntas sobre salud mental
- Recibe respuestas basadas en datasets profesionales
- Ve el nivel de confianza de cada respuesta
- Mantén un historial de la conversación

#### 🌐 Cambio de Idioma
- **Español**: Configuración por defecto
- **Inglés**: Cambia desde el menú "Idioma" o la barra de herramientas

#### 💾 Gestión de Conversaciones
- **Guardar**: Menú → Archivo → Guardar conversación
- **Cargar**: Menú → Archivo → Cargar conversación
- **Exportar**: Menú → Archivo → Exportar chat

#### 📊 Estadísticas
- **Ver estadísticas**: Menú → Ayuda → Estadísticas
- Información sobre datasets cargados
- Métricas de la sesión actual
- Estadísticas del motor de búsqueda

## 🔧 Configuración Avanzada

### Ajustar Parámetros de Búsqueda
Edita `utils/config.py`:

```python
SEARCH_CONFIG = {
    'min_similarity_threshold': 0.1,  # Umbral mínimo de similitud
    'max_results': 5,                 # Máximo número de resultados
    'use_stemming': True,             # Usar stemming
    'remove_stopwords': True          # Eliminar stop words
}
```

### Personalizar Mensajes
Modifica los mensajes en `utils/config.py` en la sección `UI_MESSAGES`.

## 🧪 Pruebas y Desarrollo

### Ejecutar Pruebas
```bash
python3 test_chatbot.py
```

Las pruebas verifican:
- ✅ Carga de datasets
- ✅ Funcionamiento del motor de búsqueda
- ✅ Procesamiento de texto
- ✅ Gestión de conversaciones

### Crear Ejecutable
```bash
python3 build_executable.py
```

Esto generará un archivo ejecutable independiente en la carpeta `dist/`.

## 📊 Datasets Incluidos

### Dataset Simple (Español)
- **Formato**: Conversaciones HUMAN/ASSISTANT
- **Contenido**: Preguntas y respuestas sobre salud mental en español
- **Tamaño**: Variable según el archivo proporcionado

### Dataset Combinado (Inglés)
- **Formato**: JSON con Context/Response
- **Contenido**: Conversaciones profesionales de terapia
- **Tamaño**: ~3,500 conversaciones
- **Fuente**: Hugging Face datasets

## 🔍 Ejemplos de Uso

### Preguntas en Español
- "¿Qué es la ansiedad?"
- "¿Cómo manejar el estrés?"
- "Síntomas de depresión"
- "Técnicas de relajación"

### Preguntas en Inglés
- "What is anxiety?"
- "How to manage stress?"
- "Depression symptoms"
- "Relaxation techniques"

## 🛠️ Solución de Problemas

### Error: "No module named 'tkinter'"
```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# macOS (con Homebrew)
brew install python-tk
```

### Error: Datasets no encontrados
- Verifica que los archivos JSON estén en la carpeta `data/`
- Asegúrate de que los nombres coincidan con la configuración

### Baja confianza en respuestas
- Ajusta `min_similarity_threshold` en la configuración
- Verifica que la pregunta esté en el idioma correcto
- Intenta reformular la pregunta

### Aplicación lenta
- Reduce `max_features` en el vectorizador TF-IDF
- Limita el número de conversaciones cargadas
- Considera usar un dataset más pequeño para pruebas

## 🤝 Contribución

### Agregar Nuevos Datasets
1. Coloca el archivo JSON en la carpeta `data/`
2. Modifica `dataset_processor.py` para incluir el nuevo formato
3. Actualiza la configuración en `utils/config.py`

### Mejorar el Motor de Búsqueda
- Experimenta con diferentes algoritmos de vectorización
- Ajusta los pesos de similitud entre preguntas y respuestas
- Implementa técnicas de NLP más avanzadas

## 📝 Notas Técnicas

### Arquitectura
- **Frontend**: tkinter (interfaz gráfica nativa)
- **Backend**: scikit-learn (TF-IDF, similitud coseno)
- **Procesamiento**: pandas, numpy, unidecode
- **Datos**: JSON datasets de conversaciones

### Rendimiento
- **Tiempo de carga**: 5-15 segundos (dependiendo del dataset)
- **Tiempo de respuesta**: <1 segundo por consulta
- **Memoria**: ~200-500MB durante ejecución

### Limitaciones
- Respuestas basadas únicamente en datasets existentes
- No genera contenido nuevo, solo busca similitudes
- Requiere datasets de calidad para mejores resultados

## 📄 Licencia

Este proyecto está desarrollado para uso educativo y de apoyo. No reemplaza la consulta profesional en salud mental.

## 🆘 Soporte

Para problemas técnicos o mejoras:
1. Revisa la sección de solución de problemas
2. Ejecuta las pruebas con `python3 test_chatbot.py`
3. Verifica los logs de error en la consola

---

**⚠️ Importante**: Este chatbot es una herramienta de apoyo y no reemplaza la atención profesional en salud mental. Si experimentas una crisis, busca ayuda profesional inmediata.

**Versión**: 2.0.0  
**Última actualización**: Enero 2025
