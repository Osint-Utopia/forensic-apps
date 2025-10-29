# Open Agent Studio - Build Unlimited Computer Use Agents Without Running Out Of Credits (Mac/Windows/Linux)

<div align="center">

La primera aplicación de escritorio multiplataforma para la Automatización de Procesos Agenticos.
_Una alternativa de código abierto a UIPath y las herramientas RPA tradicionales, que utiliza modelos VLM ilimitados para objetivos semánticos._

[![Downloads](https://img.shields.io/badge/Downloads-Available-green)](#-installation)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-blue)](#-installation)
[![License](https://img.shields.io/badge/License-Open%20Source-orange)](#-contributing)
[![Star History](https://api.star-history.com/svg?repos=rohanarun/Open-Agent-Studio&type=Date)](https://star-history.com/#rohanarun/Open-Agent-Studio&Date)

[🚀 **Get Started**](#-installation) • [📖 **Documentation**](#-key-concepts) • [🤝 **Contributing**](#-contributing) • [💬 **Support**](#-support)

</div>

---

## 🌟 What is Open Agent Studio?

Open Agent Studio es una alternativa de código abierto a UIPath y a las herramientas RPA tradicionales, permitiendo la **Automatización de Procesos Agénticos** a través del lenguaje natural. En lugar de selectores frágiles y código complejo, describe lo que quieres en inglés sencillo y deja que la IA se encargue del resto. Utiliza modelos VLM gratuitos e ilimitados con detección de objetos de última generación de nuestro conjunto de datos sintéticos para lograr un uso informático de última generación sin créditos a través de servidores y agentes ilimitados.

### ✨ Key Features

- 🎯 **Objetivos Semánticos**: Automatización a prueba del futuro que sobrevive a los cambios en la interfaz de usuario
- 🎬 **Video a Agente**: La primera creación de agentes basada en video del mundo
- 🌐 **Multiplataforma**: Funciona en Windows y Linux
- 🔗 **API Integrada**: Cada instancia incluye una API REST
- 🧠 **Impulsado por IA**: Integración de GPT-4 para una toma de decisiones inteligente
- 🔄 **Autoreparación**: Bucles robustos de verificación y pruebas

---

## 📥 Instalación

### Windows

1. **Descargar**: [Ejecutable de Windows](https://toy.new/cheatlayer.zip)
2. **Extraer** el archivo ZIP
3. **Instalar Python 3.10** desde [Windows Store](https://www.microsoft.com/store/productId/9PJPW5LDXLZ5)
4. **Ejecutar** la aplicación (hacer clic en "Más información" → "Ejecutar de todas formas" si Windows muestra advertencias de seguridad)

### Linux

1. **Descargar**: [Ejecutable de Linux](https://toy.new/main.zip)
2. **Extraer** y ejecutar

### 📺 Video Tutoriales

- [Guía de Instalación de Windows](https://www.youtube.com/watch?v=8xhFKkD4H-0)
- [Demo de Video a Agente](https://www.youtube.com/watch?v=gsU5033ms5k)

### ✨ Herramientas construidas usando Open Agent Studio

- [Agentsbase.ai](https://Agentsbase.ai)

- [Toy.new](https://Toy.new)

---

## 🚀 Inicio Rápido

### 1. Crea Tu Primer Agente

```json
{
  "key": "tu_clave_api",
  "json_output": [
    {
      "type": "abrir pestaña",
      "target": "https://example.com"
    },
    {
      "type": "click",
      "target": "Botón de inicio de sesión",
      "browser_mode": true
    }
  ],
  "goal": "Navegar al sitio web y hacer clic en iniciar sesión"
}
```

### 2. Prueba Localmente

```bash
curl -X POST http://localhost:8080/agents \
  -H "Content-Type: application/json" \
  -d @tu_agente.json
```

---

### 🎯 Objetivos Semánticos

En lugar de selectores CSS frágiles, utiliza lenguaje natural:

```json
{
  "type": "click",
  "target": "botón azul de enviar",
  "browser_mode": true
}
```

¡Esto funciona incluso si el sitio web cambia completamente su diseño!

---

## 🛠 Tipos de Nodos de Agente

<details>
<summary><strong>🌐 Automatización del Navegador</strong></summary>

### Clic

```json
{
  "type": "click",
  "target": "Botón de enviar",
  "browser_mode": true
}
```

### Escribir Texto

```json
{
  "type": "keypress",
  "prompt": "¡Hola, Mundo!"
}
```

### Abrir Pestaña

```json
{
  "type": "open tab",
  "target": "https://example.com"
}
```

### Esperar/Retraso

```json
{
  "type": "delay",
  "time": 5
}
```

</details>

<details>
<summary><strong>🧠 IA y Procesamiento de Datos</strong></summary>

### Procesamiento con GPT-4

```json
{
  "type": "gpt4",
  "prompt": "Resume el siguiente texto:",
  "input": ["article_text"],
  "data": "summary"
}
```

### Ejecución de Python

```json
{
  "type": "python",
  "code": "import pandas as pd\nprint('¡Hola desde Python!')"
}
```

### Raspado Semántico

```json
{
  "type": "semanticScrape",
  "target": "precios de productos",
  "data": "price_data"
}
```

</details>

<details>
<summary><strong>📊 Integraciones</strong></summary>

### Hojas de Cálculo de Google

```json
{
  "type": "google_sheets_add_row",
  "URL": "sheet_url",
  "Sheet_Name": "Hoja1",
  "data": ["John", "Doe", "30"]
}
```

### Correo Electrónico

```json
{
  "type": "email",
  "to": "usuario@example.com",
  "subject": "Informe de Automatización",
  "body": "¡Tarea completada con éxito!"
}
```

### Llamadas a la API

```json
{
  "type": "api",
  "URL": "https://api.example.com/data",
  "headers": { "Content-Type": "application/json" },
  "body": { "key": "value" }
}
```

</details>

---

## 📖 Ejemplo Completo

Aquí hay un agente completo que raspa datos, los analiza y envía los resultados:

```json
{
  "key": "your_api_key",
  "json_output": [
    {
      "type": "open tab",
      "target": "https://news.ycombinator.com"
    },
    {
      "type": "semanticScrape",
      "target": "titulares principales de noticias",
      "data": "headlines"
    },
    {
      "type": "gpt4",
      "prompt": "Resume estos titulares e identifica las tendencias clave:",
      "input": ["headlines"],
      "data": "analysis"
    },
    {
      "type": "google_sheets_create",
      "URL": "sheet_url",
      "Sheet_Name": "news_analysis"
    },
    {
      "type": "google_sheets_add_row",
      "URL": "sheet_url",
      "Sheet_Name": "news_analysis",
      "data": ["{{analysis}}"]
    },
    {
      "type": "email",
      "to": "gerente@empresa.com",
      "subject": "Análisis Diario de Noticias",
      "body": "Por favor, encuentre el análisis de hoy adjunto.",
      "data": "analysis"
    }
  ],
  "goal": "Raspar noticias, analizar tendencias, guardar en hojas de cálculo y enviar los resultados por correo electrónico"
}
```

---

## 📡 Referencia de la API del Agente

### POST /agents

Crea y ejecuta un nuevo agente.

**Solicitud:**

```json
{
  "key": "your_api_key",
  "json_output": [...],
  "goal": "description"
}
```

**Respuesta:**
Devuelve los resultados de la ejecución y los datos de verificación.

---

## 🗺 Hoja de Ruta

- [x] **Nube de Agente Abierto** - Ejecución basada en la nube ¡Hecho!
- [x] **Video-a-Agente Mejorado** - Precisión de conversión mejorada ¡Hecho!
- [ ] **Evaluaciones Avanzadas** - Mejores pruebas para agentes generalizados
- [ ] **Bucle de Pruebas Mejorado** - Automatización de auto-reparación
- [x] **Backend Completamente de Código Abierto** - ¡Despliegue local completo Hecho!

---

## 🤝 Contribuciones

¡Agradecemos las contribuciones! Aquí te mostramos cómo puedes ayudar:

### 🚀 Empieza

1. Envía un correo electrónico a [rohan@cheatlayer.com](mailto:rohan@cheatlayer.com) para obtener acceso de colaborador
2. Únete a nuestras discusiones comunitarias
3. Consulta los problemas abiertos y las solicitudes de funciones

### 🎯 Áreas en las que Necesitamos Ayuda

- **Evaluaciones** para agentes generalizados
- **Mejoras en el bucle de pruebas**
- **Mejora de Video-a-agente**
- **Documentación y tutoriales**
- **Informes y correcciones de errores**

### 📋 Configuración del Desarrollo

```bash
# Clona el repositorio
git clone https://github.com/rohanarun/Open-Agent-Studio.git

# Correo electrónico: rohan@cheatlayer.com
```

---

## 💬 Soporte

- **📧 Correo Electrónico**: [rohan@cheatlayer.com](mailto:rohan@cheatlayer.com)
- **📚 Documentación**: [docs.cheatlayer.com](https://docs.cheatlayer.com)
- **🐛 Problemas**: [GitHub Issues](https://github.com/rohanarun/Open-Agent-Studio/issues)
- **💡 Solicitudes de Funciones**: [GitHub Discussions](https://github.com/rohanarun/Open-Agent-Studio/discussions)

---

## 🏆 Nuestra Historia

Fundada durante la pandemia para ayudar a las personas a reconstruir sus negocios con IA, fuimos la primera startup aprobada por OpenAI para vender GPT-3 para la automatización en agosto de 2021. Inventamos los "Objetivos Semánticos" y logramos una precisión del 97% con nuestro modelo multimodal Atlas-2.

**Nuestra Visión**: En un futuro donde la IA pueda generar versiones personalizadas, seguras y gratuitas de software empresarial costoso, estamos construyendo herramientas que nivelen el campo de juego para todos.

---

<div align="center">

**Hecho con ❤️ por el Equipo de Cheat Layer**

[Empieza Ahora](#-installation) • [Destaca en GitHub](https://github.com/rohanarun/Open-Agent-Studio) • [Únete a la Comunidad](mailto:rohan@cheatlayer.com)

</div>
