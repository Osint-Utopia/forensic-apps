# 🥭 Guía Completa de Implementación del Header Flotante
## Tramitología ABC - Exportación de Mango

### 📋 Resumen del Proyecto

Ya tienes todos los archivos necesarios para implementar un header flotante profesional en tu sitio web. El sistema incluye:

- ✅ **Header HTML** con navegación responsive
- ✅ **CSS completo** con efectos y animaciones
- ✅ **JavaScript funcional** con menú móvil y efectos de scroll
- ✅ **Herramientas de implementación automática**

---

## 🚀 Método 1: Implementación Automática (Recomendado)

### Paso 1: Preparar los archivos base
Asegúrate de tener estos archivos en la raíz de tu proyecto:

```
tu-proyecto/
├── floating-header.css    ← El archivo CSS que ya tienes
├── floating-header.js     ← El archivo JavaScript que ya tienes
├── implementer.php        ← El script PHP que creé
└── header-tool.html       ← La herramienta web que creé
```

### Paso 2: Validar estructura
Ejecuta en tu terminal (desde la raíz del proyecto):

```bash
php implementer.php validate
```

Esto verificará que todos los archivos necesarios estén presentes.

### Paso 3: Implementar automáticamente
```bash
php implementer.php implement
```

¡Listo! El script procesará automáticamente todos los 25 archivos HTML.

### Paso 4: Verificar resultado
- Abre cualquier archivo HTML en tu navegador
- Deberías ver el header flotante funcionando
- Prueba el menú móvil redimensionando la ventana
- Haz scroll para ver el efecto de transparencia

---

## 🛠️ Método 2: Implementación Manual

Si prefieres hacerlo manual o tienes problemas con el script PHP:

### Para archivos en la raíz (index.html, Agente_Aduanal.html, etc.)

1. **Agregar en `<head>`:**
```html
<!-- Header Flotante CSS -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
<link rel="stylesheet" href="floating-header.css">
```

2. **Agregar después de `<body>`:**
```html
<!-- ===== HEADER FLOTANTE - TRAMITOLOGÍA ABC ===== -->
<header class="floating-header" id="floatingHeader">
    <div class="header-container">
        <!-- Logo y título -->
        <a href="index.html" class="header-logo">
            <i class="fas fa-seedling"></i>
            <div class="logo-text">
                <span class="logo-title">Tramitología ABC</span>
                <span class="logo-subtitle">Exportación de Mango</span>
            </div>
        </a>

        <!-- Navegación principal -->
        <nav class="header-nav">
            <ul class="nav-links">
                <li><a href="index.html" class="nav-link">Inicio</a></li>
                <li><a href="main/01-Todo lo que necesitas saber .html" class="nav-link">Guía Completa</a></li>
                <li><a href="main/02-7_pasos_para_exportar.html" class="nav-link">7 Pasos</a></li>
                <li><a href="main/06-Requisitos_por_pais.html" class="nav-link">Requisitos</a></li>
                <li><a href="main/07-Guia_de_bolsillo.html" class="nav-link">Guía de Bolsillo</a></li>
                <li><a href="main/08-Normatividad.html" class="nav-link">Normatividad</a></li>
            </ul>
        </nav>

        <!-- Botones de acción -->
        <div class="header-actions">
            <a href="#descargas" class="action-btn download-indicator">
                <i class="fas fa-download"></i> Descargas
            </a>
            <a href="#contacto" class="action-btn primary">
                <i class="fas fa-envelope"></i> Contacto
            </a>
        </div>

        <!-- Botón menú móvil -->
        <button class="mobile-menu-toggle" onclick="FloatingHeader.toggle()">
            <i class="fas fa-bars"></i>
        </button>
    </div>

    <!-- Menú móvil -->
    <div class="mobile-menu" id="mobileMenu">
        <div class="mobile-nav-links">
            <a href="index.html" class="mobile-nav-link">Inicio</a>
            <a href="main/01-Todo lo que necesitas saber .html" class="mobile-nav-link">Guía Completa</a>
            <a href="main/02-7_pasos_para_exportar.html" class="mobile-nav-link">7 Pasos</a>
            <a href="main/06-Requisitos_por_pais.html" class="mobile-nav-link">Requisitos</a>
            <a href="main/07-Guia_de_bolsillo.html" class="mobile-nav-link">Guía de Bolsillo</a>
            <a href="main/08-Normatividad.html" class="mobile-nav-link">Normatividad</a>
        </div>
        <div class="mobile-actions">
            <a href="#descargas" class="action-btn">
                <i class="fas fa-download"></i> Descargas
            </a>
            <a href="#contacto" class="action-btn">
                <i class="fas fa-envelope"></i> Contacto
            </a>
        </div>
    </div>
</header>
<!-- ===== FIN HEADER FLOTANTE ===== -->
```

3. **Agregar antes de `</body>`:**
```html
<!-- Header Flotante JS -->
<script src="floating-header.js"></script>
```

### Para archivos en main/ (01-Todo lo que necesitas saber .html, etc.)

**¡IMPORTANTE!** Para archivos en la carpeta `main/`, las rutas son diferentes:

1. **CSS y JS:**
```html
<link rel="stylesheet" href="../floating-header.css">
<script src="../floating-header.js"></script>
```

2. **Enlaces en el HTML del header:**
Cambiar todas las rutas para que apunten hacia arriba:
```html
<a href="../index.html" class="header-logo">
<a href="../index.html" class="nav-link">Inicio</a>
<a href="../main/01-Todo lo que necesitas saber .html" class="nav-link">Guía Completa</a>
<!-- etc. -->
```

---

## 🔧 Comandos Útiles del Script PHP

### Validar antes de implementar:
```bash
php implementer.php validate
```

### Implementar todos los archivos:
```bash
php implementer.php implement
```

### Implementar un archivo específico:
```bash
php implementer.php single . index.html
php implementer.php single . "main/01-Todo lo que necesitas saber .html"
```

### Restaurar desde backup (si algo sale mal):
```bash
php implementer.php restore
```

---

## 🎨 Personalización

### Cambiar colores:
Edita las variables CSS en `floating-header.css`:
```css
:root {
    --mango-orange: #FF8C42;    ← Color principal
    --mango-yellow: #FFD23F;    ← Color secundario
    --leaf-green: #2ECC71;      ← Color de acento
}
```

### Modificar navegación:
Edita directamente el HTML del header en cada archivo o actualiza la plantilla en el script.

### Agregar nuevos enlaces:
Usa la función JavaScript:
```javascript
FloatingHeader.updateLinks([
    {href: 'nuevo-archivo.html', text: 'Nuevo Enlace'}
]);
```

---

## 🚨 Solución de Problemas

### El header no aparece:
1. Verifica que `floating-header.css` esté en la ubicación correcta
2. Abre las herramientas de desarrollador (F12) y busca errores en la consola
3. Asegúrate de que Font Awesome se esté cargando

### El menú móvil no funciona:
1. Verifica que `floating-header.js` se esté cargando
2. Revisa la consola por errores de JavaScript
3. Asegúrate de que el script se ejecute después del DOM

### Las rutas no funcionan:
1. Para archivos en `main/`: usar `../` antes de cada ruta
2. Para archivos en raíz: usar rutas directas
3. Verifica que los nombres de archivo coincidan exactamente

### Restaurar si algo sale mal:
El script automáticamente crea backups. Si necesitas restaurar:
```bash
php implementer.php restore
```

---

## ✅ Checklist Final

- [ ] `floating-header.css` en la raíz del proyecto
- [ ] `floating-header.js` en la raíz del proyecto
- [ ] Font Awesome CDN incluido en todos los archivos
- [ ] Header HTML insertado en todos los archivos
- [ ] Rutas correctas según ubicación de archivos
- [ ] Funcionalidad del menú móvil probada
- [ ] Efecto de scroll del header probado
- [ ] Navegación entre páginas funcional

---

## 🎉 ¡Listo para usar!

Una vez completada la implementación, tendrás:

- ✅ Header flotante profesional y responsive
- ✅ Menú de navegación con efectos suaves
- ✅ Menú móvil completamente funcional
- ✅ Efectos de scroll y transparencia
- ✅ Diseño consistente con tu tema de mango
- ✅ Fácil navegación entre todas las páginas

**¡Tu sitio web de exportación de mango está listo para impresionar a tus visitantes!** 🥭✨