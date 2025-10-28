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
        'Oprtunidad_con_preparacion.html',
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
            