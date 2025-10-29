# Probador Iterativo de Generación de Código

Una herramienta basada en el navegador que demuestra la generación de código impulsada por IA con pruebas visuales de ejecución línea por línea.

Demostración en vivo: https://www.agentsbase.ai/iterative_code_generation.html

## Resumen

Esta herramienta demuestra un enfoque interactivo para la generación de código utilizando Modelos de Lenguaje Grandes (LLMs) a través de la API de OpenRouter. En lugar de generar código de una sola vez y esperar que funcione, esta herramienta:

- Genera soluciones de código JavaScript completas para tareas especificadas por el usuario.
- Ejecuta visualmente el código línea por línea en tiempo real.
- Identifica de forma inteligente errores reales frente a artefactos de ejecución esperados.
- Soluciona automáticamente problemas de código genuinos consultando a la IA.

## Características

- **Proceso de Generación de Dos Fases**: Primero genera soluciones completas, luego prueba incrementalmente.
- **Ejecución Visual Paso a Paso**: Observe cómo el código se ejecuta línea por línea con el resaltado de la línea actual.
- **Detección Inteligente de Errores**: Distingue entre errores esperados en la ejecución parcial y problemas reales de código.
- **Análisis y Corrección Automática de Errores**: Aprovecha la IA para solucionar los problemas identificados.
- **Velocidad de Ejecución Ajustable**: Controle la rapidez con la que el código avanza paso a paso en la ejecución.
- **Captura Completa de la Salida de la Consola**: Vea todos los registros, advertencias y errores durante la ejecución.

## Empezando

### Prerrequisitos

- Una clave API de OpenRouter (regístrese en [OpenRouter.ai](https://openrouter.ai) si no tiene una)
- Cualquier navegador web moderno

### Uso de la Herramienta

1. Clona este repositorio:

   ```bash
   git clone https://github.com/rohanarun/iterative-code-generation-tester.git
   ```

2. Abre `index.html` en tu navegador web (no se requiere servidor)

3. Introduce tu clave API de OpenRouter en el campo designado.

4. Escribe una descripción de lo que te gustaría que la IA codifique, como:
   - "Crea una función que calcule la secuencia de Fibonacci"
   - "Construye una simple lista de tareas pendientes con funcionalidad de añadir y eliminar"
   - "Escribe una implementación de búsqueda binaria"

5. Haz clic en "Generar Código Completo" para generar la solución completa.

6. Una vez que se genera el código, haz clic en "Probar Línea por Línea" para ver cómo se ejecuta incrementalmente.

7. Si se encuentran errores, la herramienta los analizará e intentará solucionarlos automáticamente.

8. Ajusta el control deslizante de velocidad de ejecución para controlar el ritmo de las pruebas línea por línea.

## Cómo Funciona

### Generación de Código

La herramienta utiliza Claude 3.7 Sonnet (a través de OpenRouter) para generar una solución JavaScript completa para la tarea especificada. Un indicador de sistema especializado guía a la IA para crear código funcional y bien formado.

### Pruebas Línea por Línea

Después de generar la solución, la herramienta:

1. Ejecuta el código línea por línea, resaltando la línea actual.
2. Captura toda la salida de la consola (registros, errores, advertencias).
3. Analiza cualquier error para determinar si son:
   - **Errores esperados**: Artefactos naturales de la ejecución parcial (como variables no definidas que se definirán más adelante)
   - **Errores reales**: Errores reales, problemas de sintaxis o problemas de lógica

### Corrección de Errores

Cuando se detectan errores reales:

1. El código completo y el contexto del error se envían de vuelta al modelo de IA.
2. Un indicador de sistema especializado en la corrección de errores guía a la IA para analizar y solucionar el problema.
3. La IA devuelve una versión corregida del código con explicaciones.
4. El código corregido reemplaza la solución original.

## Limitaciones

- Actualmente solo admite la ejecución de código JavaScript.
- Se ejecuta en el entorno JavaScript del navegador, por lo que ciertas operaciones pueden estar restringidas.
- Es posible que algún código complejo no sea adecuado para la ejecución línea por línea debido a problemas de alcance/cierre.
- Se basa en heurísticas para distinguir entre errores esperados y reales.

## Privacidad y Seguridad

- Tu clave API de OpenRouter solo se almacena en la memoria durante la sesión actual y nunca se guarda.
- Toda la ejecución del código se realiza localmente en tu navegador.
- Las llamadas a la API se realizan directamente desde tu navegador a OpenRouter.

## Contribuciones

¡Las contribuciones son bienvenidas! No dudes en enviar una solicitud de extracción (Pull Request).

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para obtener más detalles.

## Agradecimientos

- Esta herramienta utiliza la API de OpenRouter para acceder a Claude 3.7 de Anthropic
- Inspirado por el potencial de la programación asistida por IA y los flujos de trabajo de depuración

---

⭐️ Si esta herramienta te ha resultado útil, ¡considera la posibilidad de marcar el repositorio con una estrella!
