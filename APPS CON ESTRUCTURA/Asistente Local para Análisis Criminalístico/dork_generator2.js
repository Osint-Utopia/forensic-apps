/**
 * Generador de Dorks OSINT en JavaScript
 * Convierte la lógica de dork_generator.py para uso en el navegador
 * Mejoras: 
 * - Expansión de plataformas basadas en el documento proporcionado, incluyendo dominios adicionales para redes sociales y herramientas OSINT.
 * - Mejora en la generación de dorks: ahora incluye más tipos (nombre, email, username, teléfono, ubicación, leaks, etc.), formas (site:, inurl:, intitle:, filetype:, cache:, related:, etc.) y combinaciones lógicas (AND, OR, -exclusión).
 * - Lógica mejorada para extracción de parámetros: soporta más entidades como números de teléfono, direcciones, empresas, etc.
 * - Integración simulada de IA para dorks avanzados: genera variaciones contextuales y refinadas.
 * - Compatibilidad con secciones comentadas: mantiene la estructura de funciones para parsing, ejemplos, exportación, template JSON y generación de dorks.
 * - Aumento en cantidad: genera más dorks por categoría (básicos, por plataforma, por email, avanzados).
 * - Tipos de información: no solo nombre/domicilio, sino emails, perfiles sociales, historiales, metadatos, archivos asociados (PDF, DOC), imágenes, videos, etc.
 * - Lógica funcional: asegura que las funciones sean compatibles y encadenables (e.g., parse -> template -> generateDorks).
 */

class OSINTDorkGenerator {
    constructor() {
        // Expansión de platformDomains basada en el documento proporcionado
        this.platformDomains = {
            'linkedin': 'linkedin.com',
            'twitter': 'twitter.com',
            'x': 'x.com', // Alias para Twitter/X
            'facebook_recovery': 'facebook.com/login/identify?ctx=recover',
            'facebook': 'facebook.com',
            'facebook_graph': 'intelx.io/tools?tab=facebook',
            'instagram': 'instagram.com',
            'github': 'github.com',
            'gitlab': 'gitlab.com',
            'pinterest': 'pinterest.com',
            'reddit': 'reddit.com',
            'snapchat': 'snapchat.com',
            'whatsapp': 'whatsapp.com', // Dominio general, aunque no directo
            'skype': 'skype.com',
            'telegram': 'telegram.org',
            'discord': 'discord.com',
            'onlyfans': 'onlyfans.com',
            'tiktok': 'tiktok.com',
            // Herramientas OSINT adicionales como dominios para dorks relacionados
            'crowdtangle': 'apps.crowdtangle.com',
            'social_searcher': 'social-searcher.com',
            'lookup_id': 'lookup-id.com',
            'whopostedwhat': 'whopostedwhat.com',
            'sowsearch': 'sowsearch.info',
            'stalkface': 'stalkface.com',
            'searchisback': 'searchisback.com',
            'snapinsta': 'snapinsta.app',
            'pickuki': 'picuki.com',
            'imginn': 'imginn.io',
            'recruitem': 'recruitin.net',
            'rocketreach': 'rocketreach.co',
            'phantombuster': 'phantombuster.com',
            'tweetdeck': 'tweetdeck.twitter.com',
            'followerwonk': 'followerwonk.com',
            'gharchive': 'gharchive.org',
            'ghostcodes': 'ghostcodes.com',
            'snapmap': 'map.snapchat.com',
            'lyzem': 'lyzem.com',
            'tgstat': 'tgstat.com',
            'topgg': 'top.gg',
            'exolyt': 'exolyt.com'
        };
    }

    /** 2
     * Analiza una descripción en lenguaje natural para extraer parámetros
     * @param {string} description - Descripción a analizar
     * @returns {Object} Parámetros extraídos
     */
    parseDescription(description) {
        const params = {
            name: null,
            email: null,
            username: null,
            phone: null,
            location: null,
            company: null,
            searchType: 'general', // general, profile, leak, media, etc.
            purpose: 'osint', // osint, research, etc.
            platforms: [], // Lista de plataformas especificadas
            dataToCollect: ['profiles', 'posts', 'emails'], // Expandido: profiles, posts, emails, phones, locations, media, files, metadata
            sentimentAnalysis: false
        };

        // Extraer nombre si está presente (mejorado con regex para nombres completos)
        const nameMatch = description.match(/(?:name|nombre|persona):\s*([\w\s]+)/i);
        if (nameMatch) params.name = nameMatch[1].trim();

        // Extraer email si está presente
        const emailMatch = description.match(/(?:email|correo):\s*([\w\.-]+@[\w\.-]+)/i);
        if (emailMatch) params.email = emailMatch[1].trim();

        // Extraer username si está presente
        const usernameMatch = description.match(/(?:username|usuario):\s*(@?[\w\.-]+)/i);
        if (usernameMatch) params.username = usernameMatch[1].trim().replace('@', '');

        // Extraer teléfono (nuevo)
        const phoneMatch = description.match(/(?:phone|teléfono|numero):\s*(\+?\d[\d\s\-]+)/i);
        if (phoneMatch) params.phone = phoneMatch[1].trim();

        // Extraer ubicación (nuevo)
        const locationMatch = description.match(/(?:location|ubicación|ciudad):\s*([\w\s,]+)/i);
        if (locationMatch) params.location = locationMatch[1].trim();

        // Extraer empresa (nuevo)
        const companyMatch = description.match(/(?:company|empresa):\s*([\w\s]+)/i);
        if (companyMatch) params.company = companyMatch[1].trim();

        // Determinar tipo de búsqueda (expandido)
        if (description.includes('perfil') || description.includes('profile')) params.searchType = 'profile';
        else if (description.includes('leak') || description.includes('fuga')) params.searchType = 'leak';
        else if (description.includes('media') || description.includes('imagenes') || description.includes('videos')) params.searchType = 'media';
        else if (description.includes('files') || description.includes('archivos')) params.searchType = 'files';

        // Determinar propósito
        if (description.includes('investigación') || description.includes('research')) params.purpose = 'research';

        // Determinar plataformas (expandido para detectar más)
        Object.keys(this.platformDomains).forEach(platform => {
            if (description.toLowerCase().includes(platform)) params.platforms.push(platform);
        });

        // Si no se especificaron plataformas, habilitar las más comunes
        if (params.platforms.length === 0) {
            params.platforms = ['facebook', 'twitter', 'linkedin', 'instagram', 'github', 'reddit'];
        }

        // Determinar datos a recolectar (expandido)
        if (description.includes('emails')) params.dataToCollect.push('emails');
        if (description.includes('phones')) params.dataToCollect.push('phones');
        if (description.includes('locations')) params.dataToCollect.push('locations');
        if (description.includes('media')) params.dataToCollect.push('media');
        if (description.includes('files')) params.dataToCollect.push('files');
        if (description.includes('metadata')) params.dataToCollect.push('metadata');

        // Determinar si necesita análisis de sentimiento
        if (description.includes('sentimiento') || description.includes('sentiment')) params.sentimentAnalysis = true;

        return params;
    }

    /** 3
     * Genera ejemplos predefinidos para casos de uso comunes
     * @returns {Array} Lista de ejemplos
     */
    generateExamples() {
        return [
            { description: 'Buscar perfil de John Doe en Facebook y Twitter', expected: this.parseDescription('Buscar perfil de John Doe en Facebook y Twitter') },
            { description: 'Encontrar emails de example@domain.com en leaks', expected: { searchType: 'leak', dataToCollect: ['emails'] } },
            { description: 'OSINT sobre username: @user123 en Instagram con ubicación: New York', expected: { username: 'user123', platforms: ['instagram'], location: 'New York' } },
            // Nuevos ejemplos expandidos
            { description: 'Buscar teléfono +123456789 en Reddit y Telegram', expected: { phone: '+123456789', platforms: ['reddit', 'telegram'] } },
            { description: 'Analizar media de empresa Acme Corp en LinkedIn y Github', expected: { company: 'Acme Corp', platforms: ['linkedin', 'github'], searchType: 'media' } },
            { description: 'Dorks para archivos PDF relacionados con John Doe', expected: { name: 'John Doe', searchType: 'files', dataToCollect: ['files'] } }
        ];
    }

    /**
     * Genera una plantilla JSON basada en una descripción en lenguaje natural
     * @param {string} description - Descripción en lenguaje natural
     * @returns {Object} Plantilla JSON generada
     */
    generateJSONTemplate(description) {
        const params = this.parseDescription(description);
        return {
            target: {
                name: params.name,
                email: params.email,
                username: params.username,
                phone: params.phone,
                location: params.location,
                company: params.company
            },
            config: {
                searchType: params.searchType,
                purpose: params.purpose,
                platforms: params.platforms,
                dataToCollect: params.dataToCollect,
                sentimentAnalysis: params.sentimentAnalysis
            }
        };
    }

    /**
     * Genera una lista de dorks de búsqueda basados en la información del objetivo
     * @param {Object} targetInfo - Información del objetivo (name, email, username, etc.)
     * @param {Object} platforms - Configuración de plataformas habilitadas (e.g., {facebook: true, twitter: true})
     * @param {Object} aiIntegration - Opciones de integración de IA (e.g., {enabled: true})
     * @returns {Array} Lista de dorks generados
     */
    generateDorks(targetInfo, platforms = {}, aiIntegration = { enabled: false }) {
        let dorks = [];

        // Habilitar todas las plataformas si no se especifican
        if (Object.keys(platforms).length === 0) {
            platforms = Object.fromEntries(Object.keys(this.platformDomains).map(p => [p, true]));
        }

        // Dorks básicos por nombre/usuario (expandido con más formas)
        if (targetInfo.name || targetInfo.username) {
            const query = targetInfo.name || `@${targetInfo.username}`;
            dorks.push(`"${query}"`); // Búsqueda exacta
            dorks.push(`intext:"${query}"`); // En texto
            dorks.push(`intitle:"${query}"`); // En título
            dorks.push(`inurl:"${query}"`); // En URL
            dorks.push(`cache:"${query}"`); // Cache de Google
            dorks.push(`related:${query}`); // Sitios relacionados
            if (targetInfo.location) dorks.push(`"${query}" "${targetInfo.location}"`); // Con ubicación
            if (targetInfo.company) dorks.push(`"${query}" site:${this.platformDomains.linkedin} "${targetInfo.company}"`); // En LinkedIn con empresa
        }

        // Dorks por email (expandido)
        if (targetInfo.email) {
            dorks.push(`"${targetInfo.email}"`); // Búsqueda exacta
            dorks.push(`site:pastebin.com "${targetInfo.email}"`); // En pastes
            dorks.push(`filetype:txt "${targetInfo.email}"`); // En archivos TXT
            dorks.push(`inurl:leak "${targetInfo.email}"`); // En leaks
            dorks.push(`"${targetInfo.email}" -site:example.com`); // Excluyendo sitios
            if (targetInfo.phone) dorks.push(`"${targetInfo.email}" "${targetInfo.phone}"`); // Combinado con teléfono
        }

        // Dorks por teléfono (nuevo)
        if (targetInfo.phone) {
            dorks.push(`"${targetInfo.phone}"`); // Exacto
            dorks.push(`site:facebook.com "${targetInfo.phone}"`); // En Facebook
            dorks.push(`intext:"${targetInfo.phone}" filetype:pdf`); // En PDFs
            dorks.push(`"${targetInfo.phone}" location:"${targetInfo.location || ''}"`); // Con ubicación
        }

        // Dorks por plataforma (expandido: más combinaciones y tipos)
        Object.keys(platforms).forEach(platform => {
            if (platforms[platform] && this.platformDomains[platform]) {
                const domain = this.platformDomains[platform];
                if (targetInfo.name) dorks.push(`site:${domain} "${targetInfo.name}"`); // Nombre en sitio
                if (targetInfo.username) dorks.push(`site:${domain} inurl:${targetInfo.username}`); // Username en URL
                if (targetInfo.email) dorks.push(`site:${domain} "${targetInfo.email}"`); // Email en sitio
                dorks.push(`site:${domain} filetype:jpg | filetype:png`); // Imágenes en sitio (media)
                dorks.push(`site:${domain} filetype:pdf | filetype:doc`); // Archivos en sitio
                dorks.push(`site:${domain} intext:metadata`); // Metadatos
                if (targetInfo.searchType === 'leak') dorks.push(`site:${domain} inurl:leak`); // Leaks en sitio
            }
        });

        // Dorks avanzados con IA (simulado: genera variaciones refinadas)
        if (aiIntegration.enabled) {
            // Simulación: agregar variaciones lógicas y contextuales
            if (targetInfo.name) {
                dorks.push(`("${targetInfo.name}" OR "${targetInfo.name.split(' ')[0]}") AND (profile OR perfil)`); // OR para variaciones de nombre
                dorks.push(`-site:irrelevant.com "${targetInfo.name}"`); // Exclusión de sitios irrelevantes
            }
            if (targetInfo.location) dorks.push(`geocode:${targetInfo.location} "${targetInfo.name || targetInfo.username}"`); // Búsqueda geolocalizada (simulada)
            dorks.push(`inurl:api "${targetInfo.email || targetInfo.username}"`); // En endpoints API potenciales
            dorks.push(`filetype:json | filetype:xml "${targetInfo.name}"`); // En archivos de datos
        }

        // Filtrar duplicados y retornar
        return [...new Set(dorks)]; // Eliminar duplicados para eficiencia
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