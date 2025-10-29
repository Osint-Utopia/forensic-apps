# Instrucciones de Despliegue - Generador OSINT Integrado

## Resumen Ejecutivo

Este documento proporciona instrucciones detalladas para integrar la utilidad "Generador de Búsquedas OSINT Inteligente" en tu landing page existente de Focus24x7® y desplegarla en GitHub Pages. La utilidad permite a usuarios no especialistas generar dorks de búsqueda y plantillas JSON para investigaciones OSINT mediante descripciones en lenguaje natural.

## Archivos Necesarios

Los siguientes archivos han sido desarrollados y están listos para la integración:

### Archivos Principales
1. **`osint_section.html`** - Estructura HTML de la sección OSINT
2. **`osint_styles.css`** - Estilos CSS específicos para la utilidad
3. **`dork_generator.js`** - Lógica del generador de dorks convertida a JavaScript
4. **`osint_script.js`** - Funcionalidad de la interfaz de usuario

### Archivos de Demostración
5. **`integration_demo.html`** - Página de demostración completa (para pruebas)

## Pasos de Integración

### Paso 1: Preparación del Repositorio

1. **Accede a tu repositorio de GitHub:**
   ```
   https://github.com/ziprespaldo-hub/landing-page
   ```

2. **Crea una nueva rama para la integración:**
   ```bash
   git checkout -b feature/osint-integration
   ```

### Paso 2: Subida de Archivos

1. **Sube los archivos JavaScript a la carpeta raíz o a una subcarpeta `js/`:**
   - `dork_generator.js`
   - `osint_script.js`

2. **Sube el archivo CSS a la carpeta de estilos o raíz:**
   - `osint_styles.css`

### Paso 3: Modificación del HTML Principal

1. **Abre el archivo principal de tu landing page** (probablemente `index.html`)

2. **Añade la referencia al CSS en el `<head>`:**
   ```html
   <link rel="stylesheet" href="osint_styles.css">
   ```

3. **Localiza la sección donde quieres integrar la utilidad OSINT.** 
   Recomendación: Después de la descripción de OTE (Inteligencia OSINT) y antes de los testimonios.

4. **Inserta el contenido de `osint_section.html`** en esa ubicación.

5. **Añade las referencias a los scripts JavaScript antes del cierre del `</body>`:**
   ```html
   <script src="dork_generator.js"></script>
   <script src="osint_script.js"></script>
   </body>
   ```

### Paso 4: Ajustes de Estilo (Opcional)

Si necesitas ajustar los estilos para que coincidan mejor con tu diseño existente:

1. **Modifica las variables de color en `osint_styles.css`:**
   ```css
   /* Ajusta estos colores según tu paleta */
   :root {
     --primary-color: #2563eb;
     --secondary-color: #059669;
     --background-color: #f8fafc;
   }
   ```

2. **Ajusta las fuentes si es necesario:**
   ```css
   .osint-section {
     font-family: tu-fuente-preferida, sans-serif;
   }
   ```

### Paso 5: Pruebas Locales

1. **Abre tu archivo HTML modificado en un navegador local**
2. **Verifica que:**
   - La sección OSINT se muestra correctamente
   - Los estilos se aplican sin conflictos
   - La funcionalidad de generación de dorks funciona
   - Las pestañas de resultados funcionan
   - No hay errores en la consola del navegador

### Paso 6: Despliegue en GitHub Pages

1. **Confirma los cambios:**
   ```bash
   git add .
   git commit -m "Integrar utilidad OSINT en landing page"
   ```

2. **Sube los cambios:**
   ```bash
   git push origin feature/osint-integration
   ```

3. **Crea un Pull Request** en GitHub para revisar los cambios

4. **Una vez aprobado, fusiona con la rama principal:**
   ```bash
   git checkout main
   git merge feature/osint-integration
   git push origin main
   ```

5. **GitHub Pages se actualizará automáticamente** en unos minutos

## Estructura de Integración Recomendada

### Ubicación en la Landing Page

```html
<!-- Secciones existentes -->
<section><!-- XIPHOS --></section>
<section><!-- AKONTIA --></section>
<section><!-- OTE --></section>

<!-- NUEVA SECCIÓN OSINT -->
<section id="osint-generator" class="osint-section">
  <!-- Contenido de osint_section.html aquí -->
</section>

<!-- Secciones existentes -->
<section><!-- Testimonios --></section>
<section><!-- CTA Final --></section>
```

### Consideraciones de Diseño

La nueva sección está diseñada para integrarse armoniosamente con tu landing page existente:

- **Colores:** Utiliza una paleta compatible con tu diseño actual
- **Tipografía:** Hereda las fuentes de tu página principal
- **Espaciado:** Mantiene consistencia con las secciones existentes
- **Responsividad:** Se adapta a dispositivos móviles y tablets

## Funcionalidades Incluidas

### Para Usuarios No Especialistas

1. **Entrada en Lenguaje Natural:**
   - Los usuarios describen lo que buscan en español simple
   - Ejemplo: "Buscar información sobre Juan Pérez en LinkedIn y GitHub"

2. **Ejemplos Rápidos:**
   - Botones predefinidos para casos comunes
   - Investigación de candidatos, monitoreo de marca, análisis de seguridad

3. **Resultados Múltiples:**
   - **Dorks de búsqueda:** Consultas optimizadas para motores de búsqueda
   - **Plantilla JSON:** Configuración estructurada para herramientas OSINT
   - **Vista previa:** Resumen comprensible de la búsqueda

4. **Funcionalidades de Copia/Descarga:**
   - Copiar dorks individuales o todos a la vez
   - Descargar plantilla JSON para uso posterior

### Integración con tus Herramientas Existentes

La utilidad genera plantillas JSON compatibles con la estructura diseñada para integrarse con NUCLEI, OTE y SPIDERSUITE. Los usuarios pueden:

1. **Generar plantillas** usando la interfaz web
2. **Descargar el JSON** generado
3. **Usar el JSON** como entrada para tus herramientas existentes

## Mantenimiento y Actualizaciones

### Archivos a Monitorear

- **`osint_styles.css`** - Para ajustes visuales
- **`dork_generator.js`** - Para mejoras en la generación de dorks
- **`osint_script.js`** - Para nuevas funcionalidades de interfaz

### Posibles Mejoras Futuras

1. **Integración con Backend:**
   - Conectar con APIs reales de tus herramientas OSINT
   - Procesamiento más avanzado con IA en el servidor

2. **Visualizador de Resultados:**
   - Implementar el "Visualizador Interactivo de Huella Digital"
   - Mostrar conexiones entre entidades encontradas

3. **Más Tipos de Búsqueda:**
   - Soporte para organizaciones, dominios, IPs
   - Plantillas especializadas por industria

## Soporte y Resolución de Problemas

### Problemas Comunes

1. **Los estilos no se aplican:**
   - Verifica que `osint_styles.css` esté correctamente enlazado
   - Revisa la consola del navegador por errores de carga

2. **JavaScript no funciona:**
   - Asegúrate de que ambos archivos JS estén cargados
   - Verifica que no haya conflictos con otros scripts

3. **La sección no se muestra:**
   - Confirma que el HTML se insertó correctamente
   - Revisa que no haya errores de sintaxis HTML

### Contacto para Soporte

Si encuentras problemas durante la integración, los archivos incluyen comentarios detallados y la estructura está diseñada para ser fácil de modificar y mantener.

## Conclusión

Esta integración añade valor significativo a tu landing page al proporcionar una herramienta práctica que demuestra la facilidad de uso de tus soluciones OSINT. Los usuarios pueden experimentar directamente cómo la tecnología simplifica tareas complejas, reforzando tu propuesta de valor de "Ciberseguridad Nivel Experto. Simplificada para Ti."

