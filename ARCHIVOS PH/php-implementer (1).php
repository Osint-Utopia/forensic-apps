<?php
/**
 * Script PHP para Implementación Automática del Header Flotante
 * Tramitología ABC - Exportación de Mango
 * 
 * Este script modifica automáticamente todos los archivos HTML
 * para incluir el header flotante con las rutas correctas.
 */

class FloatingHeaderImplementer {
    
    private $projectRoot;
    private $backupDir;
    private $processedFiles = [];
    private $errors = [];
    
    // Configuración de archivos
    private $targetFiles = [
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
        'Ooprtunidad_con_preparacion.html',
        'Plan estructurado.html',
        'Potencia exportadora.html',
        'Registro formal.html',
        'main/01-Todo lo que necesitas saber .html',
        'main/02-7_pasos_para_exportar.html',
        'main/03-Que_Implica.html',
        'main/04-Es_Complicado_exportar.html',
        'main/05-Pesos_a_dolares.html',
        'main/06-Requisitos_por_pais.html',
        'main/07-Guia_de_bolsillo.html',
        'main/08-Normatividad.html',
        'main/09-upci.html'
    ];
    
    // Template del header HTML
    private $headerTemplate = '<!-- ===== HEADER FLOTANTE - TRAMITOLOGÍA ABC ===== -->
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
                <li><a href="{{ROOT_PATH}}index.html" class="mobile-nav-link">Inicio</a></li>
				<li><a href="{{ROOT_PATH}}main/Agente_Aduanal.html" class="mobile-nav-link">Agente Aduanal</a></li>
				<li><a href="{{ROOT_PATH}}main/Cadena_de_frio.html" class="mobile-nav-link">Cadena de Frio</a></li>
				<li><a href="{{ROOT_PATH}}main/Certificaciones.html" class="mobile-nav-link">Certificaciones</a></li>
				<li><a href="{{ROOT_PATH}}main/Certificados_Fito.html" class="mobile-nav-link">Certificaciones Fito</a></li>
				<li><a href="{{ROOT_PATH}}main/Cuentas_Claras.html" class="mobile-nav-link">Cuentas Claras</a></li>
				<li><a href="{{ROOT_PATH}}main/Documentos_Precisos.html" class="mobile-nav-link">Documentos Ok</a></li>
				<li><a href="{{ROOT_PATH}}main/En_caliente.html" class="mobile-nav-link">En Caliente</a></li>
				<li><a href="{{ROOT_PATH}}main/Enfoque estrategico.html" class="mobile-nav-link">Enfoque</a></li>
				<li><a href="{{ROOT_PATH}}main/Guía Estratégica.html" class="mobile-nav-link">Guia con Calma</a></li>
				<li><a href="{{ROOT_PATH}}main/No_olvidar.html" class="mobile-nav-link">No Olvidar</a></li>
				<li><a href="{{ROOT_PATH}}main/Oportunidad_con_preparacion.html" class="mobile-nav-link">Oportunidad</a></li>
				<li><a href="{{ROOT_PATH}}main/Plan estructurado.html" class="mobile-nav-link">Plan</a></li>
				<li><a href="{{ROOT_PATH}}main/Potencia exportadora.html" class="mobile-nav-link">Potencialidad</a></li>
				<li><a href="{{ROOT_PATH}}main/Registro formal.html" class="mobile-nav-link">Registro</a></li>
				<li><a href="{{ROOT_PATH}}main/01-Todo lo que necesitas saber .html" class="mobile-nav-link">Guía Completa</a></li>
				<li><a href="{{ROOT_PATH}}main/02-7_pasos_para_exportar.html" class="mobile-nav-link">7 Pasos</a></li>
				<li><a href="{{ROOT_PATH}}main/03-Que_Implica.html" class="mobile-nav-link">Que Implica</a></li>
				<li><a href="{{ROOT_PATH}}main/04-Es_Complicado_exportar.html" class="mobile-nav-link">Es complicado exportar</a></li>
				<li><a href="{{ROOT_PATH}}main/05-Pesos_a_dolares.html" class="mobile-nav-link"Pesos a dolares</a></li>
				<li><a href="{{ROOT_PATH}}main/06-Requisitos_por_pais.html" class="mobile-nav-link">Requisitos</a></li>
				<li><a href="{{ROOT_PATH}}main/07-Guia_de_bolsillo.html" class="mobile-nav-link">Guía de Bolsillo</a></li>
				<li><a href="{{ROOT_PATH}}main/08-Normatividad.html" class="mobile-nav-link">Normatividad</a></li>
				<li><a href="{{ROOT_PATH}}main/09-upci.html" class="mobile-nav-link">Upci</a></li>
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
			<a href="{{ROOT_PATH}}main/Agente_Aduanal.html" class="mobile-nav-link">Agente Aduanal</a>
			<a href="{{ROOT_PATH}}main/Cadena_de_frio.html" class="mobile-nav-link">Cadena de Frio</a>
			<a href="{{ROOT_PATH}}main/Certificaciones.html" class="mobile-nav-link">Certificaciones</a>
			<a href="{{ROOT_PATH}}main/Certificados_Fito.html" class="mobile-nav-link">Certificaciones Fito</a>
			<a href="{{ROOT_PATH}}main/Cuentas_Claras.html" class="mobile-nav-link">Cuentas Claras</a>
			<a href="{{ROOT_PATH}}main/Documentos_Precisos.html" class="mobile-nav-link">Documentos Ok</a>
			<a href="{{ROOT_PATH}}main/En_caliente.html" class="mobile-nav-link">En Caliente</a>
			<a href="{{ROOT_PATH}}main/Enfoque estrategico.html" class="mobile-nav-link">Enfoque</a>
			<a href="{{ROOT_PATH}}main/Guía Estratégica.html" class="mobile-nav-link">Guia con Calma</a>
			<a href="{{ROOT_PATH}}main/No_olvidar.html" class="mobile-nav-link">No Olvidar</a>
			<a href="{{ROOT_PATH}}main/Oportunidad_con_preparacion.html" class="mobile-nav-link">Oportunidad</a>
			<a href="{{ROOT_PATH}}main/Plan estructurado.html" class="mobile-nav-link">Plan</a>
			<a href="{{ROOT_PATH}}main/Potencia exportadora.html" class="mobile-nav-link">Potencialidad</a>
			<a href="{{ROOT_PATH}}main/Registro formal.html" class="mobile-nav-link">Registro</a>
			<a href="{{ROOT_PATH}}main/01-Todo lo que necesitas saber .html" class="mobile-nav-link">Guía Completa</a>
			<a href="{{ROOT_PATH}}main/02-7_pasos_para_exportar.html" class="mobile-nav-link">7 Pasos</a>
			<a href="{{ROOT_PATH}}main/03-Que_Implica.html" class="mobile-nav-link">Que Implica</a>
			<a href="{{ROOT_PATH}}main/04-Es_Complicado_exportar.html" class="mobile-nav-link">Es complicado exportar</a>
			<a href="{{ROOT_PATH}}main/05-Pesos_a_dolares.html" class="mobile-nav-link"Pesos a dolares</a>
			<a href="{{ROOT_PATH}}main/06-Requisitos_por_pais.html" class="mobile-nav-link">Requisitos</a>
			<a href="{{ROOT_PATH}}main/07-Guia_de_bolsillo.html" class="mobile-nav-link">Guía de Bolsillo</a>
			<a href="{{ROOT_PATH}}main/08-Normatividad.html" class="mobile-nav-link">Normatividad</a>
			<a href="{{ROOT_PATH}}main/09-upci.html" class="mobile-nav-link">Upci</a>
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
<!-- ===== FIN HEADER FLOTANTE ===== -->';
    
    public function __construct($projectRoot = '.') {
        $this->projectRoot = rtrim($projectRoot, '/');
        $this->backupDir = $this->projectRoot . '/backup_' . date('Y-m-d_H-i-s');
        
        // Crear directorio de backup
        if (!is_dir($this->backupDir)) {
            mkdir($this->backupDir, 0755, true);
            mkdir($this->backupDir . '/main', 0755, true);
        }
    }
    
    /**
     * Determina la ruta relativa a la raíz según la ubicación del archivo
     */
    private function getRootPath($filePath) {
        return (strpos($filePath, 'main/') === 0) ? '../' : '';
    }
    
    /**
     * Genera las dependencias CSS y JS para un archivo
     */
    private function generateDependencies($filePath) {
        $rootPath = $this->getRootPath($filePath);
        
        return [
            'css' => [
                'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css',
                $rootPath . 'floating-header.css'
            ],
            'js' => [
                $rootPath . 'floating-header.js'
            ]
        ];
    }
    
    /**
     * Genera el HTML del header con las rutas correctas
     */
    private function generateHeaderHTML($filePath) {
        $rootPath = $this->getRootPath($filePath);
        return str_replace('{{ROOT_PATH}}', $rootPath, $this->headerTemplate);
    }
    
    /**
     * Crear backup de un archivo
     */
    private function createBackup($filePath) {
        $fullPath = $this->projectRoot . '/' . $filePath;
        $backupPath = $this->backupDir . '/' . $filePath;
        
        if (file_exists($fullPath)) {
            // Crear directorio si no existe
            $backupDir = dirname($backupPath);
            if (!is_dir($backupDir)) {
                mkdir($backupDir, 0755, true);
            }
            
            copy($fullPath, $backupPath);
            echo "✅ Backup creado: {$backupPath}\n";
            return true;
        }
        
        echo "⚠️  Archivo no encontrado para backup: {$fullPath}\n";
        return false;
    }
    
    /**
     * Procesar un archivo HTML individual
     */
    private function processFile($filePath) {
        $fullPath = $this->projectRoot . '/' . $filePath;
        
        if (!file_exists($fullPath)) {
            $this->errors[] = "Archivo no encontrado: {$fullPath}";
            echo "❌ Archivo no encontrado: {$fullPath}\n";
            return false;
        }
        
        // Crear backup
        $this->createBackup($filePath);
        
        // Leer contenido actual
        $content = file_get_contents($fullPath);
        
        if ($content === false) {
            $this->errors[] = "No se pudo leer el archivo: {$fullPath}";
            return false;
        }
        
        // Verificar si ya tiene el header
        if (strpos($content, '<!-- ===== HEADER FLOTANTE') !== false) {
            echo "⚠️  El archivo ya tiene header flotante: {$filePath}\n";
            return true;
        }
        
        // Generar dependencias y header
        $dependencies = $this->generateDependencies($filePath);
        $headerHTML = $this->generateHeaderHTML($filePath);
        
        // Modificar HTML
        $modifiedContent = $this->injectHeader($content, $dependencies, $headerHTML);
        
        if ($modifiedContent === false) {
            $this->errors[] = "Error al modificar HTML: {$filePath}";
            return false;
        }
        
        // Escribir archivo modificado
        if (file_put_contents($fullPath, $modifiedContent) !== false) {
            $this->processedFiles[] = $filePath;
            echo "✅ Procesado exitosamente: {$filePath}\n";
            return true;
        } else {
            $this->errors[] = "No se pudo escribir el archivo: {$fullPath}";
            return false;
        }
    }
    
    /**
     * Inyectar header y dependencias en el HTML
     */
    private function injectHeader($content, $dependencies, $headerHTML) {
        // Patrones para encontrar elementos HTML
        $headPattern = '/<head[^>]*>/i';
        $bodyPattern = '/<body[^>]*>/i';
        $closingBodyPattern = '/<\/body>/i';
        
        // Verificar estructura HTML básica
        if (!preg_match($headPattern, $content) || !preg_match($bodyPattern, $content)) {
            echo "⚠️  Estructura HTML no válida, creando estructura básica...\n";
            return $this->createBasicHTML($dependencies, $headerHTML, $content);
        }
        
        // Generar CSS links
        $cssLinks = '';
        foreach ($dependencies['css'] as $css) {
            $cssLinks .= "    <link rel=\"stylesheet\" href=\"{$css}\">\n";
        }
        
        // Generar JS scripts
        $jsScripts = '';
        foreach ($dependencies['js'] as $js) {
            $jsScripts .= "    <script src=\"{$js}\"></script>\n";
        }
        
        // Inyectar CSS en head
        $content = preg_replace('/(<head[^>]*>)/i', "$1\n    <!-- Header Flotante CSS -->\n{$cssLinks}", $content);
        
        // Inyectar header después de body
        $content = preg_replace('/(<body[^>]*>)/i', "$1\n\n{$headerHTML}\n", $content);
        
        // Inyectar JS antes de </body>
        $content = preg_replace('/(<\/body>)/i', "\n    <!-- Header Flotante JS -->\n{$jsScripts}\n$1", $content);
        
        return $content;
    }
    
    /**
     * Crear HTML básico si no tiene estructura válida
     */
    private function createBasicHTML($dependencies, $headerHTML, $originalContent) {
        // Generar CSS links
        $cssLinks = '';
        foreach ($dependencies['css'] as $css) {
            $cssLinks .= "    <link rel=\"stylesheet\" href=\"{$css}\">\n";
        }
        
        // Generar JS scripts
        $jsScripts = '';
        foreach ($dependencies['js'] as $js) {
            $jsScripts .= "    <script src=\"{$js}\"></script>\n";
        }
        
        // Extraer título si existe
        $title = 'Tramitología ABC - Exportación de Mango';
        if (preg_match('/<title[^>]*>(.*?)<\/title>/i', $originalContent, $matches)) {
            $title = $matches[1];
        }
        
        // Extraer contenido del body si existe
        $bodyContent = $originalContent;
        if (preg_match('/<body[^>]*>(.*?)<\/body>/is', $originalContent, $matches)) {
            $bodyContent = $matches[1];
        } elseif (preg_match('/<body[^>]*>(.*)/is', $originalContent, $matches)) {
            $bodyContent = $matches[1];
        }
        
        return "<!DOCTYPE html>
<html lang=\"es\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{$title}</title>
    
    <!-- Header Flotante CSS -->
{$cssLinks}
</head>
<body>

{$headerHTML}

    <!-- Contenido original -->
{$bodyContent}

    <!-- Header Flotante JS -->
{$jsScripts}
</body>
</html>";
    }
    
    /**
     * Procesar todos los archivos
     */
    public function processAllFiles() {
        echo "🚀 Iniciando implementación masiva del header flotante...\n";
        echo "📁 Directorio del proyecto: {$this->projectRoot}\n";
        echo "💾 Backups en: {$this->backupDir}\n\n";
        
        $totalFiles = count($this->targetFiles);
        $processedCount = 0;
        
        foreach ($this->targetFiles as $index => $filePath) {
            $fileNumber = $index + 1;
            echo "📄 [{$fileNumber}/{$totalFiles}] Procesando: {$filePath}\n";
            
            if ($this->processFile($filePath)) {
                $processedCount++;
            }
            
            echo "\n";
        }
        
        // Generar reporte
        $this->generateReport($totalFiles, $processedCount);
    }
    
    /**
     * Procesar un archivo específico
     */
    public function processSingleFile($filePath) {
        echo "🚀 Procesando archivo individual: {$filePath}\n";
        return $this->processFile($filePath);
    }
    
    /**
     * Generar reporte final
     */
    private function generateReport($totalFiles, $processedCount) {
        echo "=" . str_repeat("=", 50) . "\n";
        echo "📊 REPORTE DE IMPLEMENTACIÓN\n";
        echo "=" . str_repeat("=", 50) . "\n";
        echo "📁 Archivos totales: {$totalFiles}\n";
        echo "✅ Archivos procesados: {$processedCount}\n";
        echo "❌ Errores: " . count($this->errors) . "\n";
        echo "💾 Backups en: {$this->backupDir}\n\n";
        
        if (!empty($this->processedFiles)) {
            echo "✅ ARCHIVOS PROCESADOS EXITOSAMENTE:\n";
            foreach ($this->processedFiles as $file) {
                echo "   - {$file}\n";
            }
            echo "\n";
        }
        
        if (!empty($this->errors)) {
            echo "❌ ERRORES ENCONTRADOS:\n";
            foreach ($this->errors as $error) {
                echo "   - {$error}\n";
            }
            echo "\n";
        }
        
        if ($processedCount === $totalFiles) {
            echo "🎉 ¡IMPLEMENTACIÓN COMPLETADA EXITOSAMENTE!\n";
            echo "   Todos los archivos han sido procesados.\n";
        } elseif ($processedCount > 0) {
            echo "⚠️  IMPLEMENTACIÓN PARCIAL COMPLETADA\n";
            echo "   Algunos archivos fueron procesados con éxito.\n";
        } else {
            echo "❌ LA IMPLEMENTACIÓN FALLÓ\n";
            echo "   No se pudo procesar ningún archivo.\n";
        }
        
        echo "\n📋 PRÓXIMOS PASOS:\n";
        echo "1. Verifica que floating-header.css esté en la raíz del proyecto\n";
        echo "2. Verifica que floating-header.js esté en la raíz del proyecto\n";
        echo "3. Prueba la navegación en diferentes archivos\n";
        echo "4. Si algo sale mal, restaura desde: {$this->backupDir}\n";
    }
    
    /**
     * Validar estructura del proyecto
     */
    public function validateProject() {
        echo "🔍 Validando estructura del proyecto...\n\n";
        
        $requiredFiles = [
            'floating-header.css' => 'Archivo CSS del header flotante',
            'floating-header.js' => 'Archivo JavaScript del header flotante'
        ];
        
        $allValid = true;
        
        foreach ($requiredFiles as $file => $description) {
            $fullPath = $this->projectRoot . '/' . $file;
            if (file_exists($fullPath)) {
                echo "✅ {$description}: {$file}\n";
            } else {
                echo "❌ {$description}: {$file} (NO ENCONTRADO)\n";
                $allValid = false;
            }
        }
        
        echo "\n📁 Verificando archivos HTML objetivo:\n";
        $htmlCount = 0;
        $missingCount = 0;
        
        foreach ($this->targetFiles as $file) {
            $fullPath = $this->projectRoot . '/' . $file;
            if (file_exists($fullPath)) {
                echo "✅ {$file}\n";
                $htmlCount++;
            } else {
                echo "❌ {$file} (NO ENCONTRADO)\n";
                $missingCount++;
            }
        }
        
        echo "\n📊 RESUMEN DE VALIDACIÓN:\n";
        echo "✅ Archivos HTML encontrados: {$htmlCount}\n";
        echo "❌ Archivos HTML faltantes: {$missingCount}\n";
        
        if ($allValid && $missingCount === 0) {
            echo "🎉 ¡Proyecto listo para implementación!\n";
        } elseif ($allValid) {
            echo "⚠️  Faltan algunos archivos HTML, pero se puede proceder\n";
        } else {
            echo "❌ Faltan archivos requeridos. Revisa la configuración.\n";
        }
        
        return $allValid;
    }
    
    /**
     * Restaurar desde backup
     */
    public function restoreFromBackup($backupPath = null) {
        if ($backupPath === null) {
            // Buscar el backup más reciente
            $backups = glob($this->projectRoot . '/backup_*');
            if (empty($backups)) {
                echo "❌ No se encontraron backups\n";
                return false;
            }
            $backupPath = max($backups); // Más reciente
        }
        
        if (!is_dir($backupPath)) {
            echo "❌ Directorio de backup no existe: {$backupPath}\n";
            return false;
        }
        
        echo "🔄 Restaurando desde backup: {$backupPath}\n";
        
        foreach ($this->targetFiles as $filePath) {
            $backupFile = $backupPath . '/' . $filePath;
            $projectFile = $this->projectRoot . '/' . $filePath;
            
            if (file_exists($backupFile)) {
                if (copy($backupFile, $projectFile)) {
                    echo "✅ Restaurado: {$filePath}\n";
                } else {
                    echo "❌ Error restaurando: {$filePath}\n";
                }
            }
        }
        
        echo "🎉 Restauración completada\n";
        return true;
    }
}

// Función principal para uso directo
function main() {
    // Verificar argumentos de línea de comandos
    global $argv;
    $action = $argv[1] ?? 'help';
    $projectPath = $argv[2] ?? '.';
    
    $implementer = new FloatingHeaderImplementer($projectPath);
    
    switch ($action) {
        case 'validate':
            $implementer->validateProject();
            break;
            
        case 'implement':
            $implementer->processAllFiles();
            break;
            
        case 'single':
            $file = $argv[3] ?? '';
            if (empty($file)) {
                echo "❌ Especifica el archivo a procesar\n";
                echo "Uso: php implementer.php single [ruta_proyecto] [archivo]\n";
                break;
            }
            $implementer->processSingleFile($file);
            break;
            
        case 'restore':
            $backupPath = $argv[3] ?? null;
            $implementer->restoreFromBackup($backupPath);
            break;
            
        case 'help':
        default:
            echo "🥭 Script de Implementación del Header Flotante\n";
            echo "Tramitología ABC - Exportación de Mango\n\n";
            echo "Uso:\n";
            echo "  php implementer.php validate [ruta_proyecto]  - Validar estructura\n";
            echo "  php implementer.php implement [ruta_proyecto] - Implementar en todos\n";
            echo "  php implementer.php single [ruta_proyecto] [archivo] - Procesar uno\n";
            echo "  php implementer.php restore [ruta_proyecto] [backup] - Restaurar\n";
            echo "  php implementer.php help - Mostrar esta ayuda\n\n";
            echo "Ejemplos:\n";
            echo "  php implementer.php validate\n";
            echo "  php implementer.php implement .\n";
            echo "  php implementer.php single . index.html\n";
            break;
    }
}

// Ejecutar si se llama directamente
if (php_sapi_name() === 'cli' && basename(__FILE__) === basename($_SERVER['SCRIPT_NAME'])) {
    main();
}

?>
            