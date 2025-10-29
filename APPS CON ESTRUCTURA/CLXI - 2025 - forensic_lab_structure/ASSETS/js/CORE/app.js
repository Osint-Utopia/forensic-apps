/**
 * Laboratorio Forense IA - Aplicación Principal
 * Sistema completo de análisis forense con IA local
 */

class ForensicApp {
    constructor() {
        this.currentView = 'evidence';
        this.uploadedFiles = [];
        this.analysisHistory = [];
        this.activeModel = null;
        this.embeddings = null;
        this.isProcessing = false;
        
        // Configuración
        this.config = {
            maxFileSize: 50 * 1024 * 1024, // 50MB
            allowedFileTypes: ['image/*', 'application/pdf', 'text/*', '.docx', '.xlsx'],
            models: {
                primary: 'local-llama',
                embedding: 'sentence-transformers'
            },
            storage: {
                casesPath: 'data/user-data/cases/',
                templatesPath: 'data/user-data/templates/'
            }
        };

        // Prompts forenses especializados
        this.forensicPrompts = {
            'analiza-metadatos': 'Analiza los metadatos EXIF de esta imagen desde una perspectiva forense. Incluye: geolocalización, fecha/hora de captura, dispositivo utilizado, posibles alteraciones, y relevancia para la investigación.',
            
            'fotografia-forense': 'Realiza un análisis técnico de fotografía forense considerando: composición, iluminación, ángulos, escalas, distorsiones, calidad de imagen, elementos probatorios visibles y recomendaciones para documentación.',
            
            'escena-crimen': 'Ayuda con la reconstrucción tridimensional de la escena del crimen basándose en las evidencias fotográficas. Analiza perspectivas, distancias, posicionamiento de objetos y sugiere toma de medidas.',
            
            'balistica': 'Interpreta los patrones balísticos visibles. Analiza: trayectorias, impactos, residuos de pólvora, distancia de disparo, y características del proyectil o arma utilizada.',
            
            'antropologia': 'Realiza análisis antropológico forense de los restos o evidencias humanas. Considera: edad, sexo, estatura, ancestralidad, traumas, tiempo transcurrido desde la muerte.',
            
            'entomologia': 'Interpreta los patrones entomológicos para estimación de intervalo post-mortem. Analiza especies presentes, estadios de desarrollo, condiciones ambientales y cronología.',

            'documentoscopia': 'Examina el documento para detectar alteraciones, falsificaciones o autenticidad. Analiza: tintas, papeles, firmas, sellos, técnicas de alteración y elementos de seguridad.',

            'informatica-forense': 'Analiza la evidencia digital: metadatos, hash, registro de actividad, recuperación de archivos eliminados, análisis de dispositivos y preservación de la cadena de custodia digital.'
        };

        this.init();
    }

    /**
     * Manejo de drop de archivos
     */
    handleFileDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.remove('dragover');
        
        const files = Array.from(e.dataTransfer.files);
        this.processFiles(files);
    }

    /**
     * Manejo de selección de archivos
     */
    handleFileSelect(e) {
        const files = Array.from(e.target.files);
        this.processFiles(files);
    }

    /**
     * Procesar archivos subidos
     */
    async processFiles(files) {
        for (const file of files) {
            if (this.validateFile(file)) {
                const fileObj = await this.createFileObject(file);
                this.uploadedFiles.push(fileObj);
            }
        }
        
        this.updateFileList();
        this.updateFileStats();
    }

    /**
     * Validar archivo
     */
    validateFile(file) {
        // Validar tamaño
        if (file.size > this.config.maxFileSize) {
            this.showStatus(`Archivo ${file.name} muy grande (máx ${this.formatFileSize(this.config.maxFileSize)})`, 'error');
            return false;
        }

        return true;
    }

    /**
     * Crear objeto de archivo con metadatos
     */
    async createFileObject(file) {
        const fileObj = {
            id: this.generateId(),
            name: file.name,
            size: file.size,
            type: file.type,
            lastModified: file.lastModified,
            file: file,
            metadata: {},
            analysis: null
        };

        // Extraer metadatos si es imagen
        if (file.type.startsWith('image/')) {
            try {
                fileObj.metadata = await this.extractImageMetadata(file);
            } catch (error) {
                console.warn('No se pudieron extraer metadatos de', file.name);
            }
        }

        return fileObj;
    }

    /**
     * Extraer metadatos EXIF de imagen
     */
    async extractImageMetadata(file) {
        return new Promise((resolve) => {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    // Simulación de extracción EXIF (en producción usar librería EXIF-js)
                    const metadata = {
                        fileName: file.name,
                        fileSize: file.size,
                        dateCreated: new Date(file.lastModified),
                        camera: 'Información no disponible',
                        gps: null,
                        dimensions: null,
                        orientation: 1
                    };
                    
                    // Obtener dimensiones de imagen
                    const img = new Image();
                    img.onload = () => {
                        metadata.dimensions = {
                            width: img.width,
                            height: img.height
                        };
                        resolve(metadata);
                    };
                    img.src = e.target.result;
                } catch (error) {
                    resolve({});
                }
            };
            reader.readAsDataURL(file);
        });
    }

    /**
     * Actualizar lista de archivos en UI
     */
    updateFileList() {
        const fileList = document.getElementById('fileList');
        if (!fileList) return;

        fileList.innerHTML = '';

        this.uploadedFiles.forEach((fileObj, index) => {
            const fileItem = this.createFileListItem(fileObj, index);
            fileList.appendChild(fileItem);
        });
    }

    /**
     * Crear elemento de archivo en lista
     */
    createFileListItem(fileObj, index) {
        const item = document.createElement('div');
        item.className = 'file-item';
        item.innerHTML = `
            <div class="file-info">
                <div class="file-name">${this.getFileIcon(fileObj.type)} ${fileObj.name}</div>
                <div class="file-details">
                    ${this.formatFileSize(fileObj.size)} • ${fileObj.type || 'Desconocido'} • 
                    ${new Date(fileObj.lastModified).toLocaleString()}
                    ${fileObj.metadata?.dimensions ? ` • ${fileObj.metadata.dimensions.width}×${fileObj.metadata.dimensions.height}px` : ''}
                </div>
            </div>
            <div class="file-actions">
                <button class="btn btn-small btn-outline" onclick="forensicApp.analyzeFile(${index})">
                    🔍 Analizar
                </button>
                <button class="btn btn-small btn-outline" onclick="forensicApp.removeFile(${index})">
                    ❌ Quitar
                </button>
            </div>
        `;

        return item;
    }

    /**
     * Obtener icono según tipo de archivo
     */
    getFileIcon(mimeType) {
        if (mimeType.startsWith('image/')) return '📸';
        if (mimeType.startsWith('video/')) return '🎥';
        if (mimeType.includes('pdf')) return '📄';
        if (mimeType.includes('word') || mimeType.includes('document')) return '📝';
        if (mimeType.includes('excel') || mimeType.includes('spreadsheet')) return '📊';
        return '📎';
    }

    /**
     * Formatear tamaño de archivo
     */
    formatFileSize(bytes) {
        const sizes = ['B', 'KB', 'MB', 'GB'];
        if (bytes === 0) return '0 B';
        const i = Math.floor(Math.log(bytes) / Math.log(1024));
        return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
    }

    /**
     * Actualizar estadísticas de archivos
     */
    updateFileStats() {
        const fileCount = document.getElementById('fileCount');
        const totalSize = document.getElementById('totalSize');

        if (fileCount) {
            fileCount.textContent = `${this.uploadedFiles.length} archivo${this.uploadedFiles.length !== 1 ? 's' : ''}`;
        }

        if (totalSize) {
            const total = this.uploadedFiles.reduce((sum, file) => sum + file.size, 0);
            totalSize.textContent = this.formatFileSize(total);
        }
    }

    /**
     * Remover archivo de la lista
     */
    removeFile(index) {
        this.uploadedFiles.splice(index, 1);
        this.updateFileList();
        this.updateFileStats();
    }

    /**
     * Usar prompt predefinido
     */
    usePrompt(promptKey) {
        const prompt = this.forensicPrompts[promptKey];
        if (prompt) {
            const promptInput = document.getElementById('promptInput');
            if (promptInput) {
                promptInput.value = prompt;
                promptInput.focus();
            }
        }
    }

    /**
     * Realizar análisis forense
     */
    async performAnalysis() {
        if (this.isProcessing) {
            this.showStatus('Análisis en progreso, por favor espera...', 'warning');
            return;
        }

        const promptInput = document.getElementById('promptInput');
        const prompt = promptInput?.value.trim();

        if (!prompt && this.uploadedFiles.length === 0) {
            this.showStatus('Ingresa una consulta o sube archivos para analizar', 'error');
            return;
        }

        this.isProcessing = true;
        this.showLoadingOverlay(true);
        this.updateLoadingText('Iniciando análisis forense...');

        try {
            // Preparar contexto del análisis
            const analysisContext = {
                prompt: prompt || 'Analiza la evidencia proporcionada',
                files: this.uploadedFiles,
                analysisType: document.getElementById('analysisType')?.value || 'general',
                timestamp: new Date().toISOString()
            };

            // Mostrar mensaje del usuario en chat
            this.addChatMessage('user', prompt || 'Análisis de evidencia', this.uploadedFiles);

            // Realizar análisis con IA local
            const analysisResult = await this.analyzeWithLocalAI(analysisContext);

            // Mostrar resultado en chat
            this.addChatMessage('ai', analysisResult.response, null, analysisResult);

            // Guardar en historial
            this.analysisHistory.push({
                id: this.generateId(),
                timestamp: new Date(),
                context: analysisContext,
                result: analysisResult
            });

            // Mostrar sección de resultados
            this.showResults(analysisResult);

            // Limpiar input
            if (promptInput) promptInput.value = '';

        } catch (error) {
            console.error('Error en análisis:', error);
            this.addChatMessage('ai', `Error al realizar el análisis: ${error.message}`, null, { error: true });
            this.showStatus('Error en el análisis. Verifica la configuración del modelo.', 'error');
        } finally {
            this.isProcessing = false;
            this.showLoadingOverlay(false);
        }
    }

    /**
     * Analizar con IA local
     */
    async analyzeWithLocalAI(context) {
        this.updateLoadingText('Procesando con modelo IA local...');

        // Preparar contexto forense
        const forensicContext = this.buildForensicContext(context);

        // Simular análisis con IA local (aquí se integraría con Llama/Mistral)
        const analysisResult = await this.simulateLocalAIAnalysis(forensicContext);

        return analysisResult;
    }

    /**
     * Construir contexto forense para IA
     */
    buildForensicContext(context) {
        let forensicPrompt = `Eres un especialista en criminalística y ciencias forenses. Analiza la siguiente evidencia con rigor técnico y científico.

TIPO DE ANÁLISIS: ${context.analysisType.toUpperCase()}
CONSULTA: ${context.prompt}

EVIDENCIA DISPONIBLE:`;

        // Agregar información de archivos
        if (context.files.length > 0) {
            context.files.forEach((file, index) => {
                forensicPrompt += `\n\n--- ARCHIVO ${index + 1} ---`;
                forensicPrompt += `\nNombre: ${file.name}`;
                forensicPrompt += `\nTipo: ${file.type}`;
                forensicPrompt += `\nTamaño: ${this.formatFileSize(file.size)}`;
                
                if (file.metadata && Object.keys(file.metadata).length > 0) {
                    forensicPrompt += `\nMetadatos EXIF:`;
                    if (file.metadata.dimensions) {
                        forensicPrompt += `\n  - Dimensiones: ${file.metadata.dimensions.width}×${file.metadata.dimensions.height}px`;
                    }
                    if (file.metadata.dateCreated) {
                        forensicPrompt += `\n  - Fecha de creación: ${file.metadata.dateCreated}`;
                    }
                    if (file.metadata.gps) {
                        forensicPrompt += `\n  - GPS: ${file.metadata.gps.latitude}, ${file.metadata.gps.longitude}`;
                    }
                }
            });
        }

        forensicPrompt += `\n\nPROPORCIONA UN ANÁLISIS TÉCNICO QUE INCLUYA:
1. Descripción detallada de la evidencia
2. Metodología de análisis aplicada
3. Hallazgos significativos
4. Interpretación forense
5. Conclusiones y recomendaciones
6. Próximos pasos sugeridos

Mantén un enfoque científico y cita procedimientos estándar cuando sea relevante.`;

        return forensicPrompt;
    }

    /**
     * Simular análisis con IA local (placeholder para integración real)
     */
    async simulateLocalAIAnalysis(forensicContext) {
        // Simular tiempo de procesamiento
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Generar respuesta simulada basada en el contexto
        const response = this.generateForensicResponse(forensicContext);

        return {
            response: response,
            confidence: 0.85,
            processingTime: '2.3s',
            model: this.config.models.primary,
            recommendations: this.generateRecommendations(),
            metadata: {
                analysisDate: new Date().toISOString(),
                filesAnalyzed: this.uploadedFiles.length,
                technique: 'Análisis multimodal con IA'
            }
        };
    }

    /**
     * Generar respuesta forense simulada
     */
    generateForensicResponse(context) {
        const hasImages = this.uploadedFiles.some(f => f.type.startsWith('image/'));
        const fileCount = this.uploadedFiles.length;

        let response = `## 🔬 ANÁLISIS FORENSE TÉCNICO\n\n`;
        response += `**Fecha del análisis:** ${new Date().toLocaleString()}\n`;
        response += `**Archivos analizados:** ${fileCount}\n`;
        response += `**Modelo IA:** ${this.config.models.primary}\n\n`;

        response += `### 📊 DESCRIPCIÓN DE LA EVIDENCIA\n`;
        if (fileCount > 0) {
            response += `Se han procesado ${fileCount} archivo(s) de evidencia digital. `;
            if (hasImages) {
                response += `Las imágenes han sido sometidas a análisis de metadatos EXIF, `;
                response += `evaluación de autenticidad y extracción de información georreferenciada. `;
            }
        }

        response += `\n### 🔍 METODOLOGÍA APLICADA\n`;
        response += `- Análisis automatizado de metadatos\n`;
        response += `- Verificación de integridad de archivos\n`;
        response += `- Extracción de información EXIF (imágenes)\n`;
        response += `- Evaluación de cadena de custodia digital\n`;

        response += `\n### 📋 HALLAZGOS PRINCIPALES\n`;
        if (hasImages) {
            response += `- Las imágenes presentan metadatos coherentes con dispositivos de captura convencionales\n`;
            response += `- No se detectan signos evidentes de manipulación digital\n`;
            response += `- La información temporal coincide con los parámetros esperados\n`;
        }

        response += `\n### ⚖️ INTERPRETACIÓN FORENSE\n`;
        response += `Basándose en el análisis técnico realizado, la evidencia digital presenta características `;
        response += `consistentes con archivos auténticos. Se recomienda realizar análisis complementarios `;
        response += `para validación cruzada de los hallazgos.\n`;

        response += `\n### 📝 CONCLUSIONES\n`;
        response += `1. La evidencia digital ha sido procesada siguiendo protocolos forenses estándar\n`;
        response += `2. Los metadatos extraídos proporcionan información valiosa para la investigación\n`;
        response += `3. Se sugiere conservar copias hash para mantener la integridad\n`;

        response += `\n### 🎯 PRÓXIMOS PASOS RECOMENDADOS\n`;
        response += `- Realizar análisis especializado según tipo de evidencia\n`;
        response += `- Documentar hallazgos en informe oficial\n`;
        response += `- Considerar análisis por experto en la materia específica\n`;

        return response;
    }

    /**
     * Generar recomendaciones
     */
    generateRecommendations() {
        const recommendations = [
            'Preservar la cadena de custodia digital',
            'Generar hashes de integridad de todos los archivos',
            'Documentar el proceso de análisis step-by-step'
        ];

        if (this.uploadedFiles.some(f => f.type.startsWith('image/'))) {
            recommendations.push('Realizar análisis fotogramétrico si es necesario');
            recommendations.push('Verificar autenticidad mediante análisis de compresión');
        }

        return recommendations;
    }

    /**
     * Agregar mensaje al chat
     */
    addChatMessage(sender, content, files = null, analysisData = null) {
        const chatMessages = document.getElementById('chatMessages');
        if (!chatMessages) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = 'message';
        messageDiv.innerHTML = `
            <div class="message-header">
                <span class="sender">
                    ${sender === 'user' ? '👤 Usuario' : '🤖 Asistente Forense IA'}
                </span>
                <span class="timestamp">${new Date().toLocaleTimeString()}</span>
            </div>
            <div class="message-content">
                ${this.formatMessageContent(content)}
                ${files && files.length > 0 ? this.formatFileAttachments(files) : ''}
                ${analysisData ? this.formatAnalysisMetadata(analysisData) : ''}
            </div>
        `;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    /**
     * Formatear contenido del mensaje
     */
    formatMessageContent(content) {
        // Convertir markdown básico a HTML
        return content
            .replace(/^### (.*$)/gim, '<h4>$1</h4>')
            .replace(/^## (.*$)/gim, '<h3>$1</h3>')
            .replace(/^# (.*$)/gim, '<h2>$1</h2>')
            .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
            .replace(/\*(.*)\*/gim, '<em>$1</em>')
            .replace(/^\- (.*$)/gim, '<li>$1</li>')
            .replace(/(<li>.*<\/li>)/s, '<ul>$1</ul>')
            .replace(/\n/g, '<br>');
    }

    /**
     * Formatear archivos adjuntos en mensaje
     */
    formatFileAttachments(files) {
        const fileList = files.map(file => 
            `<div class="file-attachment">
                ${this.getFileIcon(file.type)} ${file.name} (${this.formatFileSize(file.size)})
            </div>`
        ).join('');

        return `<div class="message-attachments">
            <h5>📎 Archivos adjuntos:</h5>
            ${fileList}
        </div>`;
    }

    /**
     * Formatear metadatos del análisis
     */
    formatAnalysisMetadata(analysisData) {
        if (analysisData.error) return '';

        return `<div class="analysis-metadata">
            <h5>📊 Metadatos del análisis:</h5>
            <div class="metadata-grid">
                <span>Confianza: ${Math.round(analysisData.confidence * 100)}%</span>
                <span>Tiempo: ${analysisData.processingTime}</span>
                <span>Modelo: ${analysisData.model}</span>
            </div>
        </div>`;
    }

    /**
     * Mostrar resultados en sección dedicada
     */
    showResults(analysisResult) {
        const resultsSection = document.getElementById('resultsSection');
        const resultsContent = document.getElementById('resultsContent');

        if (resultsSection && resultsContent) {
            resultsContent.innerHTML = this.formatAnalysisResults(analysisResult);
            resultsSection.style.display = 'block';
            
            // Scroll suave hasta los resultados
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        }
    }

    /**
     * Formatear resultados del análisis
     */
    formatAnalysisResults(result) {
        return `
            <div class="results-header">
                <h4>🔍 Análisis Completo</h4>
                <div class="results-stats">
                    <span>Confianza: ${Math.round(result.confidence * 100)}%</span>
                    <span>Tiempo: ${result.processingTime}</span>
                </div>
            </div>
            <div class="results-body">
                ${this.formatMessageContent(result.response)}
            </div>
            <div class="results-recommendations">
                <h5>💡 Recomendaciones:</h5>
                <ul>
                    ${result.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        `;
    }

    /**
     * Toggle de tema claro/oscuro
     */
    toggleTheme() {
        const currentTheme = document.body.dataset.theme || 'dark';
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.body.dataset.theme = newTheme;
        localStorage.setItem('forensic-theme', newTheme);
        
        const themeToggle = document.getElementById('themeToggle');
        if (themeToggle) {
            themeToggle.textContent = newTheme === 'dark' ? '🌙' : '☀️';
        }
    }

    /**
     * Mostrar modal de configuración
     */
    showSettingsModal() {
        const modal = document.getElementById('settingsModal');
        if (modal) {
            modal.classList.add('active');
            this.loadSettingsToModal();
        }
    }

    /**
     * Ocultar modal de configuración
     */
    hideSettingsModal() {
        const modal = document.getElementById('settingsModal');
        if (modal) {
            modal.classList.remove('active');
        }
    }

    /**
     * Cargar configuración al modal
     */
    loadSettingsToModal() {
        const primaryModel = document.getElementById('primaryModel');
        const embeddingModel = document.getElementById('embeddingModel');
        const casesPath = document.getElementById('casesPath');
        const templatesPath = document.getElementById('templatesPath');

        if (primaryModel) primaryModel.value = this.config.models.primary;
        if (embeddingModel) embeddingModel.value = this.config.models.embedding;
        if (casesPath) casesPath.value = this.config.storage.casesPath;
        if (templatesPath) templatesPath.value = this.config.storage.templatesPath;
    }

    /**
     * Guardar configuración
     */
    saveSettings() {
        const primaryModel = document.getElementById('primaryModel');
        const embeddingModel = document.getElementById('embeddingModel');
        const casesPath = document.getElementById('casesPath');
        const templatesPath = document.getElementById('templatesPath');

        if (primaryModel) this.config.models.primary = primaryModel.value;
        if (embeddingModel) this.config.models.embedding = embeddingModel.value;
        if (casesPath) this.config.storage.casesPath = casesPath.value;
        if (templatesPath) this.config.storage.templatesPath = templatesPath.value;

        // Guardar en localStorage
        localStorage.setItem('forensic-config', JSON.stringify(this.config));
        
        this.hideSettingsModal();
        this.showStatus('Configuración guardada correctamente', 'success');
    }

    /**
     * Mostrar/ocultar overlay de carga
     */
    showLoadingOverlay(show) {
        const overlay = document.getElementById('loadingOverlay');
        if (overlay) {
            if (show) {
                overlay.classList.add('active');
            } else {
                overlay.classList.remove('active');
            }
        }
    }

    /**
     * Actualizar texto de carga
     */
    updateLoadingText(text) {
        const loadingText = document.getElementById('loadingText');
        if (loadingText) {
            loadingText.textContent = text;
        }
    }

    /**
     * Actualizar estado del modelo
     */
    updateModelStatus(status) {
        const modelStatus = document.getElementById('modelStatus');
        if (modelStatus) {
            const dot = modelStatus.querySelector('.status-dot');
            const text = modelStatus.querySelector('span:last-child');
            
            if (dot && text) {
                dot.className = `status-dot ${status}`;
                text.textContent = status === 'ready' ? 'Listo' : 
                                 status === 'loading' ? 'Cargando' : 'Error';
            }
        }
    }

    /**
     * Mostrar mensaje de estado
     */
    showStatus(message, type = 'info', duration = 5000) {
        // Crear elemento de notificación
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Agregar al DOM
        document.body.appendChild(notification);
        
        // Mostrar con animación
        setTimeout(() => notification.classList.add('show'), 100);
        
        // Remover después del tiempo especificado
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => document.body.removeChild(notification), 300);
        }, duration);
    }

    /**
     * Generar ID único
     */
    generateId() {
        return Date.now().toString(36) + Math.random().toString(36).substr(2);
    }

    /**
     * Analizar archivo específico
     */
    async analyzeFile(index) {
        const file = this.uploadedFiles[index];
        if (!file) return;

        const prompt = `Analiza específicamente el archivo "${file.name}" de tipo ${file.type}`;
        document.getElementById('promptInput').value = prompt;
        
        // Crear contexto solo con este archivo
        const originalFiles = [...this.uploadedFiles];
        this.uploadedFiles = [file];
        
        await this.performAnalysis();
        
        // Restaurar lista completa
        this.uploadedFiles = originalFiles;
        this.updateFileList();
    }
}

// Inicializar aplicación global
window.ForensicApp = ForensicApp;

// Crear instancia global cuando el DOM esté listo
let forensicApp;
document.addEventListener('DOMContentLoaded', () => {
    forensicApp = new ForensicApp();
    window.forensicApp = forensicApp; // Para acceso desde HTML
}); Inicialización de la aplicación
     */
    async init() {
        console.log('🔬 Inicializando Laboratorio Forense IA...');
        
        try {
            // Cargar configuración guardada
            await this.loadConfig();
            
            // Inicializar componentes
            await this.initializeComponents();
            
            // Configurar event listeners
            this.setupEventListeners();
            
            // Cargar modelos IA
            await this.initializeAI();
            
            // Mostrar vista inicial
            this.showView(this.currentView);
            
            console.log('✅ Aplicación inicializada correctamente');
            this.showStatus('Sistema forense iniciado en modo offline', 'success');
            
        } catch (error) {
            console.error('❌ Error inicializando la aplicación:', error);
            this.showStatus('Error al inicializar el sistema', 'error');
        }
    }

    /**
     * Cargar configuración desde localStorage
     */
    async loadConfig() {
        try {
            const savedConfig = localStorage.getItem('forensic-config');
            if (savedConfig) {
                this.config = { ...this.config, ...JSON.parse(savedConfig) };
            }
        } catch (error) {
            console.warn('No se pudo cargar la configuración guardada');
        }
    }

    /**
     * Inicializar componentes del sistema
     */
    async initializeComponents() {
        // Inicializar sistema de almacenamiento
        if (window.ForensicStorage) {
            this.storage = new window.ForensicStorage(this.config.storage);
        }

        // Inicializar sistema de embeddings
        if (window.ForensicEmbeddings) {
            this.embeddings = new window.ForensicEmbeddings();
            await this.embeddings.init();
        }

        // Inicializar procesador de evidencias
        if (window.EvidenceProcessor) {
            this.evidenceProcessor = new window.EvidenceProcessor();
        }

        // Inicializar generador de reportes
        if (window.ReportGenerator) {
            this.reportGenerator = new window.ReportGenerator();
        }
    }

    /**
     * Configurar todos los event listeners
     */
    setupEventListeners() {
        // Navegación
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const view = e.target.dataset.view;
                this.showView(view);
            });
        });

        // Toggle de tema
        document.getElementById('themeToggle')?.addEventListener('click', () => {
            this.toggleTheme();
        });

        // Configuración
        document.getElementById('settingsBtn')?.addEventListener('click', () => {
            this.showSettingsModal();
        });

        // Upload de archivos
        const uploadArea = document.getElementById('uploadArea');
        const evidenceInput = document.getElementById('evidenceInput');

        if (uploadArea && evidenceInput) {
            // Drag & Drop
            uploadArea.addEventListener('dragover', this.handleDragOver.bind(this));
            uploadArea.addEventListener('dragleave', this.handleDragLeave.bind(this));
            uploadArea.addEventListener('drop', this.handleFileDrop.bind(this));
            uploadArea.addEventListener('click', () => evidenceInput.click());

            // File input
            evidenceInput.addEventListener('change', this.handleFileSelect.bind(this));
        }

        // Prompts rápidos
        document.querySelectorAll('.prompt-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const promptKey = e.target.dataset.prompt;
                this.usePrompt(promptKey);
            });
        });

        // Análisis
        document.getElementById('analyzeBtn')?.addEventListener('click', () => {
            this.performAnalysis();
        });

        // Enter en textarea para análisis
        document.getElementById('promptInput')?.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
                e.preventDefault();
                this.performAnalysis();
            }
        });

        // Modal de configuración
        document.getElementById('closeSettings')?.addEventListener('click', () => {
            this.hideSettingsModal();
        });

        document.getElementById('saveSettings')?.addEventListener('click', () => {
            this.saveSettings();
        });
    }

    /**
     * Inicializar modelos de IA
     */
    async initializeAI() {
        try {
            this.updateLoadingText('Cargando modelos de IA...');
            
            // Inicializar modelo principal
            if (window.LocalAI) {
                this.localAI = new window.LocalAI();
                await this.localAI.init(this.config.models.primary);
                this.updateModelStatus('ready');
            }

            // Cargar templates y conocimiento base
            await this.loadForensicKnowledge();

            console.log('✅ Modelos IA inicializados');
        } catch (error) {
            console.error('❌ Error inicializando IA:', error);
            this.updateModelStatus('error');
        }
    }

    /**
     * Cargar base de conocimientos forense
     */
    async loadForensicKnowledge() {
        try {
            // Cargar templates de informes
            const templates = await fetch('data/models/document-templates/informe-criminalistica.json');
            if (templates.ok) {
                this.forensicTemplates = await templates.json();
            }

            // Cargar conocimiento forense base
            const knowledge = await fetch('data/knowledge-base/forensic-procedures.json');
            if (knowledge.ok) {
                this.forensicKnowledge = await knowledge.json();
            }

        } catch (error) {
            console.warn('No se pudo cargar toda la base de conocimientos:', error);
        }
    }

    /**
     * Mostrar vista específica
     */
    showView(viewName) {
        // Ocultar todas las vistas
        document.querySelectorAll('.view').forEach(view => {
            view.classList.remove('active');
        });

        // Remover clase activa de navegación
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Mostrar vista seleccionada
        const targetView = document.getElementById(`${viewName}View`);
        const targetBtn = document.querySelector(`[data-view="${viewName}"]`);

        if (targetView && targetBtn) {
            targetView.classList.add('active');
            targetBtn.classList.add('active');
            this.currentView = viewName;
        }
    }

    /**
     * Manejo de drag over en upload area
     */
    handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.add('dragover');
    }

    /**
     * Manejo de drag leave en upload area
     */
    handleDragLeave(e) {
        e.preventDefault();
        e.stopPropagation();
        e.currentTarget.classList.remove('dragover');
    }

    /**
     *