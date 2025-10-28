/**
 * Generador de Dorks OSINT en JavaScript
 * Convierte la lógica de dork_generator.py para uso en el navegador
 */

class OSINTDorkGenerator {
    constructor() {
        this.platformDomains = {
            'linkedin': 'linkedin.com',
            'twitter': 'twitter.com',
            'facebook': 'facebook.com',
            'instagram': 'instagram.com',
            'github': 'github.com',
            'gitlab': 'gitlab.com'
        };
    }

    /**
     * Genera una lista de dorks de búsqueda basados en la información del objetivo
     * @param {Object} targetInfo - Información del objetivo (name, email, username, etc.)
     * @param {Object} platforms - Configuración de plataformas habilitadas
     * @param {Object} aiIntegration - Opciones de integración de IA
     * @returns {Array} Lista de dorks generados
     */
    generateDorks(targetInfo, platforms, aiIntegration) {
        const dorks = [];
        const name = targetInfo.name || '';
        const email = targetInfo.email || '';
        const username = targetInfo.username || '';

        // Dorks básicos por nombre/usuario
        if (name) {
            dorks.push(`"${name}"`);
            dorks.push(`intitle:"${name}"`);
        }
        if (username) {
            dorks.push(`"${username}"`);
            dorks.push(`inurl:"${username}"`);
        }

        // Dorks por email
        if (email) {
            dorks.push(`"${email}"`);
            dorks.push(`intext:"${email}"`);
        }

        // Dorks por plataforma
        if (platforms.social_media && platforms.social_media.enabled) {
            const socialPlatforms = platforms.social_media.specific_platforms || [];
            socialPlatforms.forEach(platform => {
                const domain = this.platformDomains[platform];
                if (domain) {
                    if (name) dorks.push(`site:${domain} "${name}"`);
                    if (username) dorks.push(`site:${domain} "${username}"`);
                    if (email) dorks.push(`site:${domain} "${email}"`);
                }
            });
        }

        if (platforms.code_repositories && platforms.code_repositories.enabled) {
            const codePlatforms = platforms.code_repositories.specific_platforms || [];
            codePlatforms.forEach(platform => {
                const domain = this.platformDomains[platform];
                if (domain) {
                    if (name) dorks.push(`site:${domain} "${name}"`);
                    if (username) dorks.push(`site:${domain} "${username}"`);
                    if (email) dorks.push(`site:${domain} "${email}"`);
                }
            });
        }

        // Dorks avanzados con IA (simulado)
        if (aiIntegration && aiIntegration.dork_generation) {
            if (name) {
                dorks.push(`"${name}" filetype:pdf resume`);
                dorks.push(`"${name}" inurl:cv OR inurl:resume`);
            }
            if (username) {
                dorks.push(`"${username}" password OR credentials`);
            }
        }

        // Eliminar duplicados
        return [...new Set(dorks)];
    }

    /**
     * Genera una plantilla JSON basada en una descripción en lenguaje natural
     * @param {string} description - Descripción en lenguaje natural
     * @returns {Object} Plantilla JSON generada
     */
    generateTemplateFromDescription(description) {
        // Análisis básico de la descripción para extraer información
        const analysis = this.analyzeDescription(description);
        
        const template = {
            template_name: `busqueda_${Date.now()}`,
            description: description,
            version: "1.0",
            search_profile: {
                type: analysis.type,
                purpose: analysis.purpose
            },
            target_info: analysis.targetInfo,
            search_parameters: {
                platforms: analysis.platforms,
                data_to_collect: analysis.dataToCollect,
                depth: "medium",
                time_frame: "all_time"
            },
            output_format: {
                type: "json",
                include_raw_data: false,
                summarize_results: true,
                visualize_connections: true
            },
            ai_integration: {
                dork_generation: true,
                sentiment_analysis: analysis.needsSentiment,
                entity_extraction: true
            }
        };

        return template;
    }

    /**
     * Analiza una descripción en lenguaje natural para extraer parámetros
     * @param {string} description - Descripción a analizar
     * @returns {Object} Parámetros extraídos
     */
    analyzeDescription(description) {
        const lowerDesc = description.toLowerCase();
        
        // Extraer nombre si está presente
        const nameMatch = description.match(/(?:buscar|encontrar|investigar).*?(?:sobre|a)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)/i);
        const name = nameMatch ? nameMatch[1] : '';

        // Extraer email si está presente
        const emailMatch = description.match(/([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/);
        const email = emailMatch ? emailMatch[1] : '';

        // Extraer username si está presente
        const usernameMatch = description.match(/usuario[:\s]+([a-zA-Z0-9_-]+)/i);
        const username = usernameMatch ? usernameMatch[1] : '';

        // Determinar tipo de búsqueda
        let type = 'persona';
        if (lowerDesc.includes('empresa') || lowerDesc.includes('organización') || lowerDesc.includes('compañía')) {
            type = 'organización';
        }

        // Determinar propósito
        let purpose = 'investigación_antecedentes';
        if (lowerDesc.includes('candidato') || lowerDesc.includes('empleado')) {
            purpose = 'investigación_antecedentes';
        } else if (lowerDesc.includes('marca') || lowerDesc.includes('reputación')) {
            purpose = 'monitoreo_reputación';
        } else if (lowerDesc.includes('seguridad') || lowerDesc.includes('amenaza')) {
            purpose = 'análisis_seguridad';
        }

        // Determinar plataformas
        const platforms = {
            social_media: {
                enabled: false,
                specific_platforms: []
            },
            code_repositories: {
                enabled: false,
                specific_platforms: []
            },
            news_media: {
                enabled: false
            }
        };

        if (lowerDesc.includes('linkedin')) {
            platforms.social_media.enabled = true;
            platforms.social_media.specific_platforms.push('linkedin');
        }
        if (lowerDesc.includes('twitter')) {
            platforms.social_media.enabled = true;
            platforms.social_media.specific_platforms.push('twitter');
        }
        if (lowerDesc.includes('facebook')) {
            platforms.social_media.enabled = true;
            platforms.social_media.specific_platforms.push('facebook');
        }
        if (lowerDesc.includes('github')) {
            platforms.code_repositories.enabled = true;
            platforms.code_repositories.specific_platforms.push('github');
        }
        if (lowerDesc.includes('noticias') || lowerDesc.includes('prensa')) {
            platforms.news_media.enabled = true;
        }

        // Si no se especificaron plataformas, habilitar las más comunes
        if (!platforms.social_media.enabled && !platforms.code_repositories.enabled && !platforms.news_media.enabled) {
            platforms.social_media.enabled = true;
            platforms.social_media.specific_platforms = ['linkedin', 'twitter'];
            platforms.news_media.enabled = true;
        }

        // Determinar datos a recolectar
        const dataToCollect = {
            emails: true,
            phone_numbers: lowerDesc.includes('teléfono') || lowerDesc.includes('contacto'),
            addresses: lowerDesc.includes('dirección') || lowerDesc.includes('ubicación'),
            associated_names: true,
            employment_history: lowerDesc.includes('trabajo') || lowerDesc.includes('empleo') || lowerDesc.includes('laboral'),
            education_history: lowerDesc.includes('educación') || lowerDesc.includes('estudios'),
            online_mentions: true,
            images: lowerDesc.includes('foto') || lowerDesc.includes('imagen'),
            videos: lowerDesc.includes('video')
        };

        // Determinar si necesita análisis de sentimiento
        const needsSentiment = lowerDesc.includes('reputación') || lowerDesc.includes('opinión') || lowerDesc.includes('sentimiento');

        return {
            type,
            purpose,
            targetInfo: {
                name,
                email,
                username,
                phone: '',
                address: '',
                social_media_handles: []
            },
            platforms,
            dataToCollect,
            needsSentiment
        };
    }

    /**
     * Genera ejemplos predefinidos para casos de uso comunes
     * @returns {Array} Lista de ejemplos
     */
    getExamples() {
        return [
            {
                title: "Investigación de Candidato",
                description: "Buscar información sobre Juan Pérez, desarrollador de software, en LinkedIn y GitHub. Necesito su historial laboral y proyectos.",
                icon: "👤"
            },
            {
                title: "Monitoreo de Marca",
                description: "Monitorear mi marca TechCorp en Twitter, Facebook y noticias. Necesito alertas sobre menciones y análisis de sentimiento.",
                icon: "🏢"
            },
            {
                title: "Análisis de Seguridad",
                description: "Investigar el correo sospechoso hacker@example.com y el usuario malicious_user en foros de seguridad y bases de datos de filtraciones.",
                icon: "🔒"
            }
        ];
    }
}

// Exportar para uso en el navegador
if (typeof window !== 'undefined') {
    window.OSINTDorkGenerator = OSINTDorkGenerator;
}

// Exportar para Node.js (si se usa en testing)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OSINTDorkGenerator;
}

