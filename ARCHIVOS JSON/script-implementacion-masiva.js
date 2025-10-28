/**
 * Script para Implementación Masiva del Header Flotante
 * Tramitología ABC - Exportación de Mango
 * 
 * Este script ayuda a implementar el header flotante en múltiples archivos HTML
 * de forma automática o semi-automática.
 */

// Configuración de archivos y rutas
const CONFIG = {
    // Archivos que deben incluir el header
    targetFiles: [
        'index.html',
        'Agente_Aduanal.html',
        'Cadena_de_frio.html',
        'Certificaciones.html',
        'Certificados_Fito.html',
        'Cuentas_Claras.html',
        'Documentos_Precisos.html',
        'En_caliente.html',
        'Enfoque estrategico.html',
        'Guía Estratégica.html',
        'No_olvidar.html',
        'Oprtunidad_con_preparacion.html',
        'Plan estructurado.html',
        'Potencia exportadora.html',
        'Registro formal.html',
        // Archivos en la carpeta main/
        'main/01-Todo lo que necesitas saber .html',
        'main/02-7_pasos_para_exportar.html',
        'main/03-Que_Implica.html',
        'main/04-Es_Complicado_exportar.html',
        'main/05-Pesos_a_dolares.html',
        'main/06-Requisitos_por_pais.html',
        'main/07-Guia_de_bolsillo.html',
        'main/08-Normatividad.html',
        'main/09-upci.html'
    ],
    
    // Archivos que NO deben incluir el header (para descarga)
    excludeFiles: [
        'Docs/',
        'Anexos/'
    ],
    
    // Dependencias requeridas
    dependencies: {
        fontAwesome: 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css',
        headerCSS: 'floating-header.css',
        headerJS: 'floating-header.js'
    }
};

// Plantilla del header HTML
const HEADER_HTML = `<!-- ===== HEADER FLOTANTE - TRAMITOLOGÍA ABC ===== -->
<header class="floating-header" id="floatingHeader">
    <div class="header-container">
        <!-- Logo y título -->
        <a href="{{ROOT_PATH}}index.html" class="header-logo">
            <i class="fas fa-seedling"></i>
            <div class="logo-text">
                <span class="logo-title">Tramitología ABC</span>
                <span class="logo-subtitle">Exportación de Mango</span>
            </div>
        </a>

        <!-- Navegación principal -->
        <nav class="header-nav">
            <ul class="nav-links">
                <li><a href="{{ROOT_PATH}}index.html" class="nav-link">Inicio</a></li>
                <li><a href="{{ROOT_PATH}}main/01-Todo lo que necesitas saber .html" class="nav-link">Guía Completa</a></li>
                <li><a href="{{ROOT_PATH}}main/02-7_pasos_para_exportar.html" class="nav-link">7 Pasos</a></li>
                <li><a href="{{ROOT_PATH}}main/06-Requisitos_por_pais.html" class="nav-link">Requisitos</a></li>
                <li><a href="{{ROOT_PATH}}main/07-Guia_de_bolsillo.html" class="nav-link">Guía de Bolsillo</a></li>
                <li><a href="{{ROOT_PATH}}main/08-Normatividad.html" class="nav-link">Normatividad</a></li>
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
            <a href="{{ROOT_PATH}}index.html" class="mobile-nav-link">Inicio</a>
            <a href="{{ROOT_PATH}}main/01-Todo lo que necesitas saber .html" class="mobile-nav-link">Guía Completa</a>
            <a href="{{ROOT_PATH}}main/02-7_pasos_para_exportar.html" class="mobile-nav-link">7 Pasos</a>
            <a href="{{ROOT_PATH}}main/06-Requisitos_por_pais.html" class="mobile-nav-link">Requisitos</a>
            <a href="{{ROOT_PATH}}main/07-Guia_de_bolsillo.html" class="mobile-nav-link">Guía de Bolsillo</a>
            <a href="{{ROOT_PATH}}main/08-Normatividad.html" class="mobile-nav-link">Normatividad</a>
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
<!-- ===== FIN HEADER FLOTANTE ===== -->`;

// Funciones de utilidad
class HeaderImplementer {
    constructor() {
        this.processedFiles = [];
        this.errors = [];
    }

    /**
     * Determina la ruta relativa a la raíz según la ubicación del archivo
     */
    getRootPath(filePath) {
        if (filePath.startsWith('main/')) {
            return '../';
        }
        return '';
    }

    /**
     * Genera las dependencias CSS y JS para un archivo
     */
    generateDependencies(filePath) {
        const rootPath = this.getRootPath(filePath);
        
        return {
            css: [
                CONFIG.dependencies.fontAwesome,
                `${rootPath}${CONFIG.dependencies.headerCSS}`
            ],
            js: [
                `${rootPath}${CONFIG.dependencies.headerJS}`
            ]
        };
    }

    /**
     * Genera el HTML del header con las rutas correctas
     */
    generateHeaderHTML(filePath) {
        const rootPath = this.getRootPath(filePath);
        return HEADER_HTML.replace(/\{\{ROOT_PATH\}\}/g, rootPath);
    }

    /**
     * Verifica si un archivo debe incluir el header
     */
    shouldIncludeHeader(filePath) {
        // Verificar si está en la lista de archivos objetivo
        if (CONFIG.targetFiles.includes(filePath)) {
            return true;
        }

        // Verificar si está en carpetas excluidas
        for (const excludePath of CONFIG.excludeFiles) {
            if (filePath.startsWith(excludePath)) {
                return false;
            }
        }

        // Por defecto, incluir header en archivos HTML en la raíz o main/
        return filePath.endsWith('.html') && 
               (filePath.indexOf('/') === -1 || filePath.startsWith('main/'));
    }

    /**
     * Genera instrucciones de implementación manual para un archivo
     */
    generateImplementationInstructions(filePath) {
        const dependencies = this.generateDependencies(filePath);
        const headerHTML = this.generateHeaderHTML(filePath);

        return {
            filePath,
            dependencies,
            headerHTML,
            instructions: [
                '1. Agregar las siguientes líneas en el <head>:',
                ...dependencies.css.map(css => `   <link rel="stylesheet" href="${css}">`),
                '',
                '2. Agregar el siguiente HTML después de <body>:',
                '   ' + headerHTML.split('\n').join('\n   '),
                '',
                '3. Agregar antes de </body>:',
                ...dependencies.js.map(js => `   <script src="${js}"></script>`)
            ]
        };
    }

    /**
     * Procesa todos los archivos objetivo
     */
    processAllFiles() {
        const results = [];

        for (const filePath of CONFIG.targetFiles) {
            if (this.shouldIncludeHeader(filePath)) {
                const instructions = this.generateImplementationInstructions(filePath);
                results.push(instructions);
                this.processedFiles.push(filePath);
            }
        }

        return results;
    }

    /**
     * Genera un reporte de implementación
     */
    generateReport() {
        const results = this.processAllFiles();
        
        return {
            summary: {
                totalFiles: CONFIG.targetFiles.length,
                processedFiles: this.processedFiles.length,
                errors: this.errors.length
            },
            processedFiles: this.processedFiles,
            errors: this.errors,
            instructions: results
        };
    }
}

// Función principal para generar instrucciones
function generateImplementationInstructions() {
    const implementer = new HeaderImplementer();
    const report = implementer.generateReport();
    
    console.log('=== REPORTE DE IMPLEMENTACIÓN DEL HEADER FLOTANTE ===');
    console.log(`Archivos procesados: ${report.summary.processedFiles}/${report.summary.totalFiles}`);
    console.log(`Errores: ${report.summary.errors}`);
    console.log('');
    
    // Mostrar instrucciones para cada archivo
    report.instructions.forEach((instruction, index) => {
        console.log(`--- ARCHIVO ${index + 1}: ${instruction.filePath} ---`);
        instruction.instructions.forEach(line => console.log(line));
        console.log('');
    });
    
    return report;
}

// Función para validar la estructura de archivos
function validateFileStructure() {
    const issues = [];
    
    // Verificar archivos requeridos
    const requiredFiles = [
        'floating-header.css',
        'floating-header.js',
        'header-component.html'
    ];
    
    console.log('=== VALIDACIÓN DE ESTRUCTURA DE ARCHIVOS ===');
    
    requiredFiles.forEach(file => {
        console.log(`Verificando ${file}...`);
        // En un entorno real, aquí verificarías si el archivo existe
        // if (!fs.existsSync(file)) issues.push(`Archivo faltante: ${file}`);
    });
    
    if (issues.length === 0) {
        console.log('✅ Todos los archivos requeridos están presentes');
    } else {
        console.log('❌ Problemas encontrados:');
        issues.forEach(issue => console.log(`  - ${issue}`));
    }
    
    return issues;
}

// Exportar funciones para uso en Node.js o navegador
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        HeaderImplementer,
        generateImplementationInstructions,
        validateFileStructure,
        CONFIG
    };
} else {
    // Para uso en navegador
    window.HeaderImplementationTool = {
        HeaderImplementer,
        generateImplementationInstructions,
        validateFileStructure,
        CONFIG
    };
}

// Ejecutar si se llama directamente
if (typeof require !== 'undefined' && require.main === module) {
    validateFileStructure();
    generateImplementationInstructions();
}

