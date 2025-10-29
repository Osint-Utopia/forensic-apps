## Estructura de Carpetas del Proyecto 'Laboratorio Forense IA'

Esta es la estructura de carpetas propuesta para la aplicación, organizada para reflejar el flujo de trabajo criminalístico y la modularidad de sus componentes, con una fuerte integración de la Inteligencia Artificial.

```
forensic-ia-app/
├── index.html                  # Página principal de la aplicación
├── README.md                   # Descripción del proyecto y estructura
├── css/
│   └── main.css                # Estilos CSS globales
├── js/
│   └── main.js                 # Lógica JavaScript principal de la aplicación
├── assets/
│   ├── images/                 # Imágenes, iconos, logos
│   └── data/                   # Datos estáticos, JSON de referencia (ej. insectos)
├── libs/                       # Bibliotecas externas (LeafletJS, EXIFR, OpenCV.js, etc.)
├── data/                       # Datos generados por la aplicación (casos, indicios, etc.)
├── modules/
│   ├── fase_inicial/
│   │   ├── notitia_criminis/   # Módulo: Notitia Criminis y Registro Inicial
│   │   └── planificacion/      # Módulo: Planificación de Intervención
│   ├── investigacion_campo/
│   │   ├── documentacion_escena/ # Módulo: Documentación de Escena (Fotografía, Lienzo, Planimetría)
│   │   └── recoleccion_indicios/ # Módulo: Recolección y Gestión de Indicios (Checklist, Cadena de Custodia)
│   ├── analisis_laboratorio/
│   │   ├── balistica/          # Módulo: Balística Forense
│   │   ├── documentoscopia_grafoscopia/ # Módulo: Documentoscopia y Grafoscopía
│   │   ├── lofoscopia/         # Módulo: Lofoscopia
│   │   ├── identificacion_fisionomica/ # Módulo: Identificación Fisionómica y Retrato Hablado
│   │   ├── informatica_forense/ # Módulo: Informática Forense
│   │   ├── entomologia_forense/ # Módulo: Entomología Forense
│   │   ├── antropologia_forense/ # Módulo: Antropología Forense
│   │   ├── serologia_forense/  # Módulo: Serología Forense
│   │   ├── ignicologia_forense/ # Módulo: Ignicología Forense
│   │   ├── hechos_transito/    # Módulo: Investigación de Hechos de Tránsito
│   │   └── perfiles_criminales/ # Módulo: Perfiles Criminales y Grafología
│   ├── gestion_soporte/
│   │   ├── gestion_casos/      # Módulo: Gestión de Casos y Evidencia
│   │   ├── generacion_informes/ # Módulo: Generación y Gestión de Informes
│   │   ├── base_conocimientos/ # Módulo: Base de Conocimientos y Aprendizaje Continuo
│   │   └── gestion_modelos_ia/ # Módulo: Configuración y Gestión de Modelos IA
│   └── ui_ux/
│       ├── dashboard/          # Módulo: Dashboard Interactivo
│       └── asistente_virtual/  # Módulo: Asistente Virtual Forense
└── views/                      # Archivos HTML/JS/CSS específicos para cada vista/módulo
```

Cada subdirectorio dentro de `modules/` contendrá los archivos HTML, CSS y JavaScript específicos de ese módulo, así como cualquier recurso de IA o datos JSON que le sean propios. La carpeta `views/` podría contener las vistas principales que se cargan dinámicamente en `index.html`.


