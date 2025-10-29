# Diseño de la Interfaz de Usuario para la Utilidad OSINT

## Concepto General

La nueva sección OSINT se integrará en la landing page existente como una sección adicional que mantenga la coherencia visual y temática. El diseño seguirá los principios de simplicidad y accesibilidad para usuarios no especialistas, mientras incorpora elementos interactivos modernos.

## Ubicación y Estructura

**Ubicación:** La nueva sección se colocará después de la descripción de las herramientas existentes (XIPHOS, AKONTIA, OTE) y antes de los testimonios. Esto mantiene el flujo lógico de la página.

**Título de la Sección:** "Generador de Búsquedas OSINT Inteligente"

**Subtítulo:** "Crea plantillas de búsqueda personalizadas con IA - Solo describe lo que necesitas encontrar"

## Componentes de la Interfaz

### 1. Área de Entrada de Texto (Input Principal)

- **Elemento:** Un textarea grande y prominente con placeholder text sugerente
- **Placeholder:** "Ejemplo: 'Buscar información sobre Juan Pérez, desarrollador de software, en LinkedIn y GitHub. Necesito su historial laboral y proyectos.'"
- **Características:**
  - Bordes redondeados con sombra sutil
  - Animación de focus con cambio de color
  - Contador de caracteres
  - Icono de IA en la esquina superior derecha

### 2. Botones de Acción Principales

- **Botón "Generar Dorks":** Estilo principal (azul/verde) con icono de búsqueda
- **Botón "Generar Plantilla JSON":** Estilo secundario con icono de código
- **Efectos:** Hover states con transiciones suaves, loading spinners durante procesamiento

### 3. Área de Resultados Expandible

- **Pestañas Interactivas:**
  - "Dorks Generados" - Lista de dorks con botones de copia individual
  - "Plantilla JSON" - Código JSON formateado con syntax highlighting
  - "Vista Previa" - Resumen visual de lo que se buscará

### 4. Funcionalidades Adicionales

- **Botones de Acción Rápida:**
  - "Copiar Todos los Dorks"
  - "Descargar Plantilla JSON"
  - "Compartir Configuración"
- **Ejemplos Predefinidos:** Botones pequeños con casos de uso comunes
  - "Investigación de Candidato"
  - "Monitoreo de Marca"
  - "Análisis de Seguridad"

## Esquema Visual

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│  🤖 Generador de Búsquedas OSINT Inteligente               │
│     Crea plantillas de búsqueda personalizadas con IA      │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ Describe tu búsqueda en lenguaje natural...        │   │
│  │                                                     │   │
│  │ Ejemplo: "Buscar información sobre Juan Pérez..."  │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [🔍 Generar Dorks]  [📋 Generar Plantilla JSON]          │
│                                                             │
│  Ejemplos rápidos:                                         │
│  [👤 Candidato] [🏢 Marca] [🔒 Seguridad]                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ [Dorks] [JSON] [Vista Previa]                      │   │
│  │                                                     │   │
│  │ Resultados aparecen aquí...                        │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [📋 Copiar Todo] [💾 Descargar] [🔗 Compartir]           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Paleta de Colores y Estilo

**Colores Principales:**
- Azul primario: #2563eb (para botones principales)
- Verde secundario: #059669 (para acciones exitosas)
- Gris neutro: #6b7280 (para texto secundario)
- Blanco/Gris claro: #f9fafb (para fondos)

**Tipografía:**
- Títulos: Font-weight 600-700, tamaños 24-32px
- Texto principal: Font-weight 400, tamaño 16px
- Código: Fuente monospace (Fira Code o similar)

**Efectos Visuales:**
- Sombras sutiles: box-shadow con blur de 4-8px
- Transiciones: 0.2-0.3s ease-in-out
- Bordes redondeados: border-radius de 8-12px
- Gradientes suaves para botones principales

## Responsividad

**Desktop (>1024px):**
- Layout de dos columnas: input a la izquierda, resultados a la derecha
- Botones en línea horizontal

**Tablet (768-1024px):**
- Layout de una columna con elementos apilados
- Botones en grid de 2x2

**Mobile (<768px):**
- Layout completamente vertical
- Botones de ancho completo
- Texto más grande para legibilidad

## Interacciones y Microanimaciones

1. **Al escribir en el textarea:** Contador de caracteres se actualiza con animación
2. **Al hacer clic en "Generar":** Botón muestra spinner de carga
3. **Al mostrar resultados:** Animación de slide-down para el área de resultados
4. **Al copiar:** Feedback visual temporal ("¡Copiado!")
5. **Hover en ejemplos:** Preview tooltip con descripción del caso de uso

## Accesibilidad

- Contraste de colores WCAG AA compliant
- Navegación por teclado completa
- Labels descriptivos para screen readers
- Indicadores de estado para acciones asíncronas
- Texto alternativo para iconos

Este diseño mantiene la coherencia con la landing page existente mientras introduce la nueva funcionalidad de manera intuitiva y atractiva para usuarios no técnicos.

