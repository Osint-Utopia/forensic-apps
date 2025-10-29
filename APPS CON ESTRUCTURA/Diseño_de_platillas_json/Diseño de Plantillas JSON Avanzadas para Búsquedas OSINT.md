
## Diseño de Plantillas JSON Avanzadas para Búsquedas OSINT

Para la idea del "Generador de Plantillas JSON Inteligente", se propone una estructura de plantilla JSON flexible y extensible que permita definir búsquedas complejas de manera sencilla para usuarios no especialistas. Esta plantilla servirá como entrada para un script Python que interpretará los parámetros y generará las consultas adecuadas para las herramientas OSINT existentes (NUCLEI, OTE, SPIDERSUITE).

### Estructura General de la Plantilla JSON

La plantilla JSON se estructurará en torno a los siguientes componentes principales:

*   **`search_profile`**: Define el objetivo general de la búsqueda (ej. "persona", "organización", "vulnerabilidad").
*   **`target_info`**: Contiene los datos iniciales conocidos sobre el objetivo (nombre, email, usuario, etc.).
*   **`search_parameters`**: Especifica los criterios y la profundidad de la búsqueda (plataformas, tipos de datos a recolectar, etc.).
*   **`output_format`**: Define cómo se deben presentar los resultados.

```json
{
  "template_name": "nombre_descriptivo_de_la_plantilla",
  "description": "Descripción breve de lo que busca esta plantilla",
  "version": "1.0",
  "search_profile": {
    "type": "persona",
    "purpose": "investigación_antecedentes"
  },
  "target_info": {
    "name": "",
    "email": "",
    "username": "",
    "phone": "",
    "address": "",
    "social_media_handles": []
  },
  "search_parameters": {
    "platforms": {
      "social_media": {
        "enabled": true,
        "specific_platforms": ["linkedin", "twitter", "facebook", "instagram"]
      },
      "public_records": {
        "enabled": false,
        "types": ["birth_records", "marriage_records", "property_records"]
      },
      "dark_web": {
        "enabled": false
      },
      "code_repositories": {
        "enabled": true,
        "specific_platforms": ["github", "gitlab"]
      },
      "news_media": {
        "enabled": true
      }
    },
    "data_to_collect": {
      "emails": true,
      "phone_numbers": true,
      "addresses": true,
      "associated_names": true,
      "employment_history": true,
      "education_history": true,
      "online_mentions": true,
      "images": false,
      "videos": false
    },
    "depth": "medium",
    "time_frame": "all_time"
  },
  "output_format": {
    "type": "json",
    "include_raw_data": false,
    "summarize_results": true,
    "visualize_connections": true
  },
  "ai_integration": {
    "dork_generation": true,
    "sentiment_analysis": false,
    "entity_extraction": true
  }
}
```

### Descripción de los Campos Clave

*   **`template_name`**: Un identificador único y descriptivo para la plantilla.
*   **`description`**: Una breve explicación del propósito de la plantilla.
*   **`version`**: Control de versiones de la plantilla.
*   **`search_profile.type`**: El tipo de entidad que se está buscando (e.g., `persona`, `organización`, `IP_address`, `domain`).
*   **`search_profile.purpose`**: El objetivo de la búsqueda (e.g., `investigación_antecedentes`, `detección_amenazas`, `recuperación_activos`).
*   **`target_info`**: Un objeto que contendrá los datos iniciales conocidos sobre el objetivo. Los campos vacíos (`""` o `[]`) indican que no se dispone de esa información inicialmente, pero la herramienta podría intentar encontrarla.
*   **`search_parameters.platforms`**: Define las plataformas o categorías de fuentes a investigar. Cada sub-campo (`social_media`, `public_records`, etc.) tiene un `enabled` booleano y, opcionalmente, `specific_platforms` o `types` para mayor granularidad.
*   **`search_parameters.data_to_collect`**: Un conjunto de booleanos que indican qué tipos específicos de datos se desean recolectar.
*   **`search_parameters.depth`**: Nivel de profundidad de la búsqueda (e.g., `light`, `medium`, `deep`). Esto podría traducirse en el número de niveles de enlaces a seguir o la cantidad de dorks a generar.
*   **`search_parameters.time_frame`**: Marco de tiempo para la búsqueda (e.g., `all_time`, `last_year`, `last_month`).
*   **`output_format`**: Define el formato y las características del resultado final. `visualize_connections` es clave para la idea del "Visualizador Interactivo de Huella Digital".
*   **`ai_integration`**: Indica qué funcionalidades de IA se deben activar para esta búsqueda, como la generación de dorks o el análisis de sentimiento.

Esta estructura permite una gran flexibilidad y control sobre la búsqueda, al mismo tiempo que es lo suficientemente intuitiva para ser generada por un sistema inteligente a partir de una entrada de lenguaje natural de un usuario no técnico.



## Estructura de Datos para Almacenamiento y Presentación de Resultados

Para que los resultados de las búsquedas OSINT sean útiles y comprensibles para usuarios no especialistas, es fundamental definir una estructura de datos clara y consistente. Esta estructura no solo facilitará el almacenamiento, sino que también será la base para la visualización interactiva de la huella digital.

Se propone una estructura de datos basada en un grafo, donde los nodos representan entidades (personas, correos electrónicos, números de teléfono, perfiles de redes sociales, organizaciones, direcciones IP, dominios, etc.) y las aristas representan las relaciones entre estas entidades. Esto permitirá una representación visual intuitiva de la información recolectada.

### Estructura General del Objeto de Resultado

El resultado de una búsqueda se podría encapsular en un objeto JSON principal que contenga:

*   **`query_details`**: Detalles de la plantilla JSON utilizada para la búsqueda.
*   **`timestamp`**: Fecha y hora de la ejecución de la búsqueda.
*   **`summary`**: Un resumen generado por IA de los hallazgos clave (si `summarize_results` está habilitado).
*   **`entities`**: Un array de objetos que representan los nodos del grafo (las entidades encontradas).
*   **`relationships`**: Un array de objetos que representan las aristas del grafo (las conexiones entre entidades).
*   **`raw_data_sources`**: Un array de objetos que referencian las fuentes de donde se obtuvo la información (si `include_raw_data` está habilitado).

```json
{
  "query_details": {
    "template_name": "nombre_descriptivo_de_la_plantilla",
    "target_info": {
      "name": "Juan Pérez"
    }
  },
  "timestamp": "2025-09-04T10:30:00Z",
  "summary": "Se encontró información significativa sobre Juan Pérez en LinkedIn, Twitter y GitHub, incluyendo su empleo actual y proyectos de código abierto.",
  "entities": [
    {
      "id": "person_juan_perez",
      "type": "person",
      "value": "Juan Pérez",
      "attributes": {
        "gender": "male",
        "age_range": "30-40",
        "nationality": "unknown"
      }
    },
    {
      "id": "email_juan.perez@example.com",
      "type": "email",
      "value": "juan.perez@example.com",
      "attributes": {}
    },
    {
      "id": "linkedin_juan_perez",
      "type": "social_media_profile",
      "platform": "linkedin",
      "value": "https://linkedin.com/in/juanperez",
      "attributes": {
        "job_title": "Software Developer",
        "company": "Tech Solutions Inc."
      }
    },
    {
      "id": "github_juan_perez",
      "type": "code_repository_profile",
      "platform": "github",
      "value": "https://github.com/juanperezdev",
      "attributes": {
        "public_repos": 15,
        "followers": 120
      }
    },
    {
      "id": "company_tech_solutions_inc",
      "type": "organization",
      "value": "Tech Solutions Inc.",
      "attributes": {
        "industry": "IT",
        "location": "Mexico City"
      }
    }
  ],
  "relationships": [
    {
      "source": "person_juan_perez",
      "target": "email_juan.perez@example.com",
      "type": "has_email",
      "attributes": {}
    },
    {
      "source": "person_juan_perez",
      "target": "linkedin_juan_perez",
      "type": "has_profile",
      "attributes": {}
    },
    {
      "source": "person_juan_perez",
      "target": "github_juan_perez",
      "type": "has_profile",
      "attributes": {}
    },
    {
      "source": "linkedin_juan_perez",
      "target": "company_tech_solutions_inc",
      "type": "works_at",
      "attributes": {
        "start_date": "2022-01-15"
      }
    }
  ],
  "raw_data_sources": [
    {
      "source_name": "LinkedIn Scraper",
      "url": "https://linkedin.com/in/juanperez",
      "timestamp_collected": "2025-09-04T10:25:00Z"
    },
    {
      "source_name": "GitHub API",
      "url": "https://api.github.com/users/juanperezdev",
      "timestamp_collected": "2025-09-04T10:26:00Z"
    }
  ]
}
```

### Descripción de los Componentes de Resultado

*   **`entities`**: Cada objeto en este array representa una entidad única descubierta. Contiene:
    *   **`id`**: Un identificador único para la entidad (ej. `person_juan_perez`, `email_example`).
    *   **`type`**: El tipo de entidad (e.g., `person`, `email`, `phone_number`, `social_media_profile`, `organization`, `IP_address`, `domain`, `document`).
    *   **`value`**: El valor principal de la entidad (ej. el nombre de la persona, la dirección de correo, la URL del perfil).
    *   **`attributes`**: Un objeto para almacenar cualquier atributo adicional relevante para la entidad (ej. `job_title`, `company`, `public_repos`, `gender`, `location`).

*   **`relationships`**: Cada objeto en este array describe una conexión entre dos entidades. Contiene:
    *   **`source`**: El `id` de la entidad de origen de la relación.
    *   **`target`**: El `id` de la entidad de destino de la relación.
    *   **`type`**: El tipo de relación (e.g., `has_email`, `has_profile`, `works_at`, `owns`, `mentions`).
    *   **`attributes`**: Un objeto para almacenar atributos adicionales de la relación (ej. `start_date` para `works_at`).

*   **`raw_data_sources`**: Opcional, proporciona trazabilidad a las fuentes originales de la información. Cada objeto contiene:
    *   **`source_name`**: Nombre de la herramienta o método utilizado para la recolección.
    *   **`url`**: URL de la fuente original (si aplica).
    *   **`timestamp_collected`**: Marca de tiempo de cuándo se recolectó el dato.

Esta estructura de grafo es ideal para la visualización, ya que permite a los usuarios no técnicos comprender rápidamente las conexiones entre diferentes piezas de información y construir una imagen completa de la huella digital de la persona de interés. Además, es lo suficientemente flexible para incorporar nuevos tipos de entidades y relaciones a medida que se descubren nuevas fuentes de datos OSINT.

