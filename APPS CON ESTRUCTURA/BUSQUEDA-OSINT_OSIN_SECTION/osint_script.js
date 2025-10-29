/**
 * Script principal para la funcionalidad OSINT
 */

class OSINTInterface {
    constructor() {
        this.generator = new OSINTDorkGenerator();
        this.currentTemplate = null;
        this.currentDorks = [];
        this.init();
    }

    init() {
        this.bindEvents();
        this.setupCharacterCounter();
        this.loadExamples();
    }

    bindEvents() {
        // Botones principales
        document.getElementById('generate-dorks-btn').addEventListener('click', () => this.generateDorks());
        document.getElementById('generate-template-btn').addEventListener('click', () => this.generateTemplate());

        // Ejemplos rápidos
        document.querySelectorAll('.example-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.loadExample(e.target.dataset.example));
        });

        // Pestañas
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Botones de acción en resultados
        document.getElementById('copy-all-dorks').addEventListener('click', () => this.copyAllDorks());
        document.getElementById('download-json').addEventListener('click', () => this.downloadJSON());

        // Cerrar notificación
        document.getElementById('notification-close').addEventListener('click', () => this.hideNotification());

        // Textarea events
        const textarea = document.getElementById('osint-description');
        textarea.addEventListener('input', () => this.updateCharacterCounter());
        textarea.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
                this.generateDorks();
            }
        });
    }

    setupCharacterCounter() {
        this.updateCharacterCounter();
    }

    updateCharacterCounter() {
        const textarea = document.getElementById('osint-description');
        const counter = document.getElementById('char-count');
        const length = textarea.value.length;
        counter.textContent = length;
        
        // Cambiar color si se acerca al límite
        if (length > 450) {
            counter.style.color = '#dc2626';
        } else if (length > 400) {
            counter.style.color = '#f59e0b';
        } else {
            counter.style.color = '#64748b';
        }
    }

    loadExamples() {
        const examples = this.generator.getExamples();
        // Los ejemplos ya están definidos en el HTML, solo necesitamos manejar los clicks
    }

    loadExample(type) {
        const examples = this.generator.getExamples();
        const example = examples.find(ex => ex.title.toLowerCase().includes(type));
        
        if (example) {
            document.getElementById('osint-description').value = example.description;
            this.updateCharacterCounter();
            
            // Animación sutil para indicar que se cargó el ejemplo
            const textarea = document.getElementById('osint-description');
            textarea.style.background = '#dbeafe';
            setTimeout(() => {
                textarea.style.background = '';
            }, 1000);
        }
    }

    async generateDorks() {
        const description = document.getElementById('osint-description').value.trim();
        
        if (!description) {
            this.showNotification('Por favor, describe tu búsqueda primero.', 'warning');
            return;
        }

        this.showLoading();

        try {
            // Simular un pequeño delay para mostrar el loading
            await new Promise(resolve => setTimeout(resolve, 1000));

            // Generar plantilla desde la descripción
            const template = this.generator.generateTemplateFromDescription(description);
            this.currentTemplate = template;

            // Generar dorks
            const dorks = this.generator.generateDorks(
                template.target_info,
                template.search_parameters.platforms,
                template.ai_integration
            );
            this.currentDorks = dorks;

            // Mostrar resultados
            this.displayDorks(dorks);
            this.displayJSON(template);
            this.displayPreview(template, dorks);
            this.showResults();
            this.switchTab('dorks');

            this.showNotification(`Se generaron ${dorks.length} dorks de búsqueda.`, 'success');

        } catch (error) {
            console.error('Error generando dorks:', error);
            this.showNotification('Error al generar los dorks. Inténtalo de nuevo.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async generateTemplate() {
        const description = document.getElementById('osint-description').value.trim();
        
        if (!description) {
            this.showNotification('Por favor, describe tu búsqueda primero.', 'warning');
            return;
        }

        this.showLoading();

        try {
            await new Promise(resolve => setTimeout(resolve, 800));

            const template = this.generator.generateTemplateFromDescription(description);
            this.currentTemplate = template;

            this.displayJSON(template);
            this.displayPreview(template, []);
            this.showResults();
            this.switchTab('json');

            this.showNotification('Plantilla JSON generada exitosamente.', 'success');

        } catch (error) {
            console.error('Error generando plantilla:', error);
            this.showNotification('Error al generar la plantilla. Inténtalo de nuevo.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    displayDorks(dorks) {
        const container = document.getElementById('dorks-list');
        container.innerHTML = '';

        if (dorks.length === 0) {
            container.innerHTML = '<p class="text-gray-500">No se generaron dorks para esta búsqueda.</p>';
            return;
        }

        dorks.forEach((dork, index) => {
            const dorkElement = document.createElement('div');
            dorkElement.className = 'dork-item';
            dorkElement.innerHTML = `
                <span class="dork-text">${this.escapeHtml(dork)}</span>
                <button class="copy-dork-btn" onclick="osintInterface.copyDork('${this.escapeHtml(dork)}', this)">
                    Copiar
                </button>
            `;
            container.appendChild(dorkElement);
        });
    }

    displayJSON(template) {
        const container = document.getElementById('json-content');
        container.textContent = JSON.stringify(template, null, 2);
    }

    displayPreview(template, dorks) {
        const container = document.getElementById('preview-content');
        const targetInfo = template.target_info;
        const platforms = template.search_parameters.platforms;
        
        let previewHTML = '';

        // Información del objetivo
        if (targetInfo.name || targetInfo.email || targetInfo.username) {
            previewHTML += `
                <div class="preview-item">
                    <h4>🎯 Objetivo de la Búsqueda</h4>
                    <p>
                        ${targetInfo.name ? `Nombre: ${targetInfo.name}<br>` : ''}
                        ${targetInfo.email ? `Email: ${targetInfo.email}<br>` : ''}
                        ${targetInfo.username ? `Usuario: ${targetInfo.username}` : ''}
                    </p>
                </div>
            `;
        }

        // Plataformas habilitadas
        const enabledPlatforms = [];
        if (platforms.social_media && platforms.social_media.enabled) {
            enabledPlatforms.push(`Redes Sociales (${platforms.social_media.specific_platforms.join(', ')})`);
        }
        if (platforms.code_repositories && platforms.code_repositories.enabled) {
            enabledPlatforms.push(`Repositorios de Código (${platforms.code_repositories.specific_platforms.join(', ')})`);
        }
        if (platforms.news_media && platforms.news_media.enabled) {
            enabledPlatforms.push('Medios de Comunicación');
        }

        if (enabledPlatforms.length > 0) {
            previewHTML += `
                <div class="preview-item">
                    <h4>🌐 Plataformas a Buscar</h4>
                    <p>${enabledPlatforms.join('<br>')}</p>
                </div>
            `;
        }

        // Tipos de datos a recolectar
        const dataTypes = [];
        const dataToCollect = template.search_parameters.data_to_collect;
        Object.keys(dataToCollect).forEach(key => {
            if (dataToCollect[key]) {
                const labels = {
                    emails: 'Correos electrónicos',
                    phone_numbers: 'Números de teléfono',
                    addresses: 'Direcciones',
                    associated_names: 'Nombres asociados',
                    employment_history: 'Historial laboral',
                    education_history: 'Historial educativo',
                    online_mentions: 'Menciones en línea',
                    images: 'Imágenes',
                    videos: 'Videos'
                };
                dataTypes.push(labels[key] || key);
            }
        });

        if (dataTypes.length > 0) {
            previewHTML += `
                <div class="preview-item">
                    <h4>📊 Datos a Recolectar</h4>
                    <p>${dataTypes.join(', ')}</p>
                </div>
            `;
        }

        // Estadísticas de dorks
        if (dorks.length > 0) {
            previewHTML += `
                <div class="preview-item">
                    <h4>🔍 Dorks Generados</h4>
                    <p>Se generaron ${dorks.length} consultas de búsqueda optimizadas para encontrar la información especificada.</p>
                </div>
            `;
        }

        container.innerHTML = previewHTML;
    }

    showResults() {
        const resultsSection = document.getElementById('results-section');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    switchTab(tabName) {
        // Actualizar botones de pestañas
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Actualizar contenido de pestañas
        document.querySelectorAll('.tab-pane').forEach(pane => {
            pane.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    copyDork(dork, button) {
        navigator.clipboard.writeText(dork).then(() => {
            const originalText = button.textContent;
            button.textContent = '¡Copiado!';
            button.classList.add('copied');
            
            setTimeout(() => {
                button.textContent = originalText;
                button.classList.remove('copied');
            }, 2000);
        }).catch(err => {
            console.error('Error copiando dork:', err);
            this.showNotification('Error al copiar. Inténtalo de nuevo.', 'error');
        });
    }

    copyAllDorks() {
        if (this.currentDorks.length === 0) {
            this.showNotification('No hay dorks para copiar.', 'warning');
            return;
        }

        const allDorks = this.currentDorks.join('\n');
        navigator.clipboard.writeText(allDorks).then(() => {
            this.showNotification(`Se copiaron ${this.currentDorks.length} dorks al portapapeles.`, 'success');
        }).catch(err => {
            console.error('Error copiando dorks:', err);
            this.showNotification('Error al copiar. Inténtalo de nuevo.', 'error');
        });
    }

    downloadJSON() {
        if (!this.currentTemplate) {
            this.showNotification('No hay plantilla para descargar.', 'warning');
            return;
        }

        const jsonString = JSON.stringify(this.currentTemplate, null, 2);
        const blob = new Blob([jsonString], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `${this.currentTemplate.template_name}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);

        this.showNotification('Plantilla JSON descargada exitosamente.', 'success');
    }

    showLoading() {
        document.getElementById('loading-overlay').style.display = 'flex';
        document.getElementById('generate-dorks-btn').disabled = true;
        document.getElementById('generate-template-btn').disabled = true;
    }

    hideLoading() {
        document.getElementById('loading-overlay').style.display = 'none';
        document.getElementById('generate-dorks-btn').disabled = false;
        document.getElementById('generate-template-btn').disabled = false;
    }

    showNotification(message, type = 'success') {
        const notification = document.getElementById('notification');
        const text = document.getElementById('notification-text');
        
        text.textContent = message;
        
        // Cambiar color según el tipo
        const content = notification.querySelector('.notification-content');
        content.className = 'notification-content';
        
        switch (type) {
            case 'success':
                content.style.background = '#059669';
                break;
            case 'warning':
                content.style.background = '#f59e0b';
                break;
            case 'error':
                content.style.background = '#dc2626';
                break;
        }
        
        notification.style.display = 'block';
        
        // Auto-hide después de 5 segundos
        setTimeout(() => {
            this.hideNotification();
        }, 5000);
    }

    hideNotification() {
        document.getElementById('notification').style.display = 'none';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// Inicializar cuando el DOM esté listo
let osintInterface;

document.addEventListener('DOMContentLoaded', function() {
    osintInterface = new OSINTInterface();
});

// Función global para copiar dorks (llamada desde el HTML)
function copyDork(dork, button) {
    if (osintInterface) {
        osintInterface.copyDork(dork, button);
    }
}

