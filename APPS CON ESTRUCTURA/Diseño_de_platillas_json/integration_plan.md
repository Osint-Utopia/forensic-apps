## Plan de Integración de Nuevos Componentes OSINT

Este plan describe cómo los componentes desarrollados (generador de dorks, plantillas JSON avanzadas) pueden integrarse con las herramientas OSINT existentes del usuario, como NUCLEI, OTE y SPIDERSUITE. Dado que no se tiene acceso directo a las implementaciones específicas del usuario, este plan se basa en principios generales de integración y asume que las herramientas existentes pueden consumir entradas de texto o JSON, o ser extendidas con scripts.

### 1. Integración del Generador de Dorks (`dork_generator.py`)

El script `dork_generator.py` produce una lista de dorks de búsqueda. Estos dorks pueden ser utilizados de varias maneras:

*   **Entrada Directa a Herramientas de Búsqueda:** Si NUCLEI, OTE o SPIDERSUITE tienen una funcionalidad para realizar búsquedas directas en motores de búsqueda (Google, Bing, etc.), los dorks generados pueden ser alimentados directamente a estas funciones.
    *   **Mecanismo:** El script `dork_generator.py` se ejecutaría primero, y su salida (la lista de dorks) se pasaría como argumento o a través de un archivo temporal a la herramienta OSINT.
    *   **Ejemplo:** `python3 dork_generator.py --template template.json > dorks.txt && OTE_tool --dorks dorks.txt`

*   **Integración con Módulos de Web Scraping:** Si las herramientas existentes incluyen módulos de web scraping, los dorks pueden ser utilizados para refinar las consultas de scraping y enfocar la recolección de datos.
    *   **Mecanismo:** Modificar el módulo de scraping de la herramienta existente para que acepte una lista de dorks como entrada y los utilice para construir sus propias consultas HTTP.

*   **Generación de Prompts para LLMs:** Los dorks generados, especialmente los más complejos, pueden ser incorporados en prompts para Modelos de Lenguaje Grandes (LLMs) si el usuario utiliza LLMs para tareas de OSINT.
    *   **Mecanismo:** El script generaría los dorks, y estos se insertarían en una plantilla de prompt para el LLM.

### 2. Integración de Plantillas JSON Avanzadas

Las plantillas JSON avanzadas (`json_template_design.md` describe su estructura) son el corazón de la automatización inteligente. Su integración dependerá de cómo las herramientas existentes manejan la configuración de las búsquedas.

*   **Adaptador de Plantillas a Formato de Herramienta:** Se necesitaría un script o módulo intermedio que lea la plantilla JSON avanzada y la traduzca al formato de entrada específico que NUCLEI, OTE o SPIDERSUITE esperan.
    *   **Mecanismo:** Un script Python (`template_adapter.py`) leería la plantilla JSON, interpretaría los `search_profile`, `target_info`, `search_parameters`, y `ai_integration`, y generaría la configuración o los comandos necesarios para la herramienta objetivo.
    *   **Ejemplo (pseudocódigo):**
        ```python
        # template_adapter.py
        import json
        from dork_generator import generate_dorks

        def adapt_template_for_nuclei(template_path):
            with open(template_path, 'r') as f:
                template = json.load(f)

            target_name = template['target_info'].get('name', '')
            # ... otras extracciones de target_info y search_parameters

            # Generar dorks si la IA está habilitada
            dorks = []
            if template['ai_integration'].get('dork_generation'):
                dorks = generate_dorks(template['target_info'], template['search_parameters']['platforms'], template['ai_integration'])

            # Construir la configuración específica para NUCLEI
            nuclei_config = {
                "target": target_name,
                "dorks": dorks,
                "modules": [] # Aquí se mapearían los search_parameters a módulos de Nuclei
            }
            return nuclei_config

        # ... funciones similares para OTE y SPIDERSUITE
        ```

*   **Extensión de Herramientas Existentes:** Si las herramientas permiten la adición de módulos o plugins personalizados, la lógica de procesamiento de las plantillas JSON podría implementarse como un nuevo módulo dentro de ellas.

### 3. Manejo de Resultados y Visualización

La estructura de datos de resultados propuesta (basada en grafo) es crucial para la visualización. Las herramientas existentes necesitarían ser adaptadas para producir o consumir esta estructura.

*   **Normalización de Salida:** Si NUCLEI, OTE o SPIDERSUITE producen resultados en formatos diferentes, se necesitaría un script post-procesamiento para convertir sus salidas a la estructura de grafo propuesta.
    *   **Mecanismo:** Un script (`result_parser.py`) leería la salida de la herramienta existente y la transformaría en el formato JSON de `entities` y `relationships`.

*   **Integración con Visualizador:** Una vez que los datos estén en el formato de grafo, pueden ser alimentados al "Visualizador Interactivo de Huella Digital" (que se desarrollaría en una fase posterior).

### 4. Consideraciones Generales para la Integración

*   **API o CLI:** La integración idealmente se realizaría a través de APIs (si las herramientas existentes las exponen) o mediante la interfaz de línea de comandos (CLI) de las herramientas.
*   **Manejo de Errores:** Implementar un robusto manejo de errores para capturar y reportar problemas durante la ejecución de las herramientas integradas.
*   **Configuración:** Permitir que la configuración de la integración (rutas a las herramientas, credenciales, etc.) sea fácilmente configurable por el usuario.
*   **Modularidad:** Mantener los nuevos componentes lo más modulares posible para facilitar futuras actualizaciones y el mantenimiento.

Este plan proporciona una hoja de ruta para la integración. La implementación real requerirá un conocimiento profundo de la arquitectura interna de NUCLEI, OTE y SPIDERSUITE del usuario.

