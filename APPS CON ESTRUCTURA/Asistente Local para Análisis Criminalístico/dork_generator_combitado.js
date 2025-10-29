/** 1
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
            'gitlab': 'gitlab.com',
            'AddMeS': 'addmes.io/', 'WhatsApp Fake Chat': 'www.fakewhats.com/generator',
			'Analizador de Perfiles': 'inflact.com/tools/profile-analyzer/',
			'AnalyzeID': 'analyzeid.com/', 'sowsearch': 'www.sowsearch.info/',
			'Aplicaciones de Facebook': 'khalil-shreateh.com/khalil.shtml/social_applications/facebook-applications/',
			'BirdHunt': 'birdhunt.huntintel.io/',
			'Búsqueda de Recuperación de Facebook': 'www.facebook.com/login/identify?ctx=recover',
			'ChatBottle: Telegram': 'chatbottle.co/bots/telegram',
			'Commit-stream': 'github.com/x1sec/commit-stream',
			'CrossLinked': 'github.com/m8sec/CrossLinked',
			'Deleted Tweet Finder': 'cache.digitaldigging.org/',
			'Digital Privacy': 'github.com/ffffffff0x/Digital-Privacy',
			'Disboard': 'disboard.org/',
			'Discord.name': 'discord.name/',
			'DiscordOSINT': 'github.com/husseinmuhaisen/DiscordOSINT?tab=readme-ov-file#-discord-search-syntax-',
			'DownAlbum': 'chrome.google.com/webstore/detail/downalbum/cgjnhhjpfcdhbhlcmmjppicjmgfkppok',
			'Download Twitter Data': 'www.twtdata.com/',
			'DumpItBlue+': 'chrome.google.com/webstore/detail/dumpitblue%2B/igmgknoioooacbcpcfgjigbaajpelbfe/',
			'Encontrar ID de Usuario de Instagram': 'www.codeofaninja.com/tools/find-instagram-user-id/',
			'Exportar Comentarios': 'exportcomments.com/',
			'Exportgram': 'exportgram.net/',
			'Facebook Graph Searcher': 'intelx.io/tools?tab=facebook',
			'Facebook People Search': 'www.facebook.com/directory/people/',
			'FacebookMatrix': 'plessas.net/facebookmatrix',
			'Fansearch': 'www.fansearch.com/',
			'Fansmetrics': 'fansmetrics.com/',
			'Find Github User ID': 'caius.github.io/github_id',
			'Findr.fans': 'findr.fans/',
			'Foller': 'foller.me/',
			'FollowerWonk': 'followerwonk.com/bio',
			'Free People Search Tool': 'freepeoplesearchtool.com/#gsc.tab=0',
			'Fulldp': 'fulldp.co/onlyfans-full-size-profile-picture/',
			'Gebruikersnamen: Snapchat': 'gebruikersnamen.nl/snapchat',
			'GitGot': 'github.com/BishopFox/GitGot',
			'Github Dorks': 'github.com/techgaun/github-dorks',
			'Github Trending RSS': 'mshibanami.github.io/GitHubTrendingRSS',
			'Github Username Search Engine': 'githubnotes-47071.firebaseapp.com/#/?_k=n0bgxn',
			'Hubite': 'hubite.com/en/onlyfans-search/',
			'InSpy': 'github.com/jobroche/InSpy',
			'InstaFreeView': 'instafreeview.com/',
			'Instahunt': 'instahunt.huntintel.io/',
			'Instaloader': 'github.com/instaloader/instaloader',
			'Integraciones IFTTT de Instagram': 'ifttt.com/instagram',
			'IntelligenceX Linkedin': 'intelx.io/tools?tab=linkedin',
			'La búsqueda ha vuelto': 'searchisback.com/',
			'LinkedIn Boolean Search': 'linkedprospect.com/linkedin-boolean-search-tool/#tool',
			'LinkedInt': 'github.com/vysecurity/LinkedInt',
			'Linkedin Search Tool': 'inteltechniques.com/tools/Linkedin.html',
			'Lookupguru': 'lookup.guru/',
			'Mavekite': 'mavekite.com/',
			'Mostly Harmless': 'kerrick.github.io/Mostly-Harmless/#features',
			'Network Tool': 'osome.iu.edu/tools/networks/',
			'OSINT Combine: Analizador de Publicaciones de Reddit': 'www.osintcombine.com/reddit-post-analyser',
			'OSINT Combine: Snapchat MultiViewer': 'www.osintcombine.com/snapchat-multi-viewer',
			'OnlyFinder': 'onlyfinder.com/',
			'OnlySearch': 'onlysearch.co/',
			'Osintgram': 'github.com/Datalux/Osintgram',
			'Phantom Buster': 'phantombuster.com/phantombuster?category=reddit',
			'Pickuki': 'www.picuki.com/', 'IMGinn.io': 'imginn.io/',
			'Pinterest Guest': 'addons.mozilla.org/en-US/firefox/addon/pinterest-guest',
			'Pinterest Photo Downloader': 'www.expertsphp.com/pinterest-photo-downloader.html',
			'Programmable Search Engine': 'cse.google.com/cse?cx=daaf18e804f81bed0',
			'Quién publicó qué': 'whopostedwhat.com/', 'StalkFace': 'stalkface.com/en/',
			'Readr for Reddit': 'chrome.google.com/webstore/detail/readr-forreddit/molhdaofohigaepljchpmfablknhabmo',
			'RecruitEm': 'recruitin.net/',
			'Reddit Enhancement Suite (Complemento de Firefox)': 'addons.mozilla.org/enGB/firefox/addon/reddit-enhancement-suite',
			'Reddit Enhancement Suite (Extensión de Chrome)': 'chrome.google.com/webstore/detail/redditenhancementsuite/kbmfpngjjgdllneeigpgjifpgocmfgmb',
			'Reddit Hacks': 'github.com/EdOverflow/hacks',
			'Reddit Search (cemulate)': 'cemulate.github.io/reddit-search',
			'Reddit Search (realsrikar)': 'realsrikar.github.io/reddit-search',
			'Reddit Search (viralharia)': 'viralharia.github.io/finddit',
			'Reddit User Analyser': 'atomiks.github.io/reddit-user-analyser',
			'Reverse Email Lookup': 'www.reversecontact.com/',
			'RocketReach': 'rocketreach.co/person',
			'Similarfans': 'similarfans.com/',
			'SimpleScraper OSINT': 'airtable.com/appyDhNeSetZU0rIw/shrceHfvukijgln9q/tblxgilU0SzfXNEwS/viwde4ACDDOpeJ8aO?blocks=bipxY3tKD5Lx0wmEU',
			'Snap Political Ads Library': 'www.snap.com/en-GB/political-ads',
			'SnapIntel': 'github.com/Kr0wZ/SnapIntel',
			'Snapchat-mapscraper': 'github.com/nemec/snapchat-map-scraper',
			'Social Bearing': 'socialbearing.com/',
			'Social Searcher': 'www.social-searcher.com/', 'Lookup-id.com': 'lookup-id.com/',
			'SocialAnalyzer - Análisis y Sentimiento Social': 'chromewebstore.google.com/detail/socialanalyzer-social-sen/efeikkcpimdfpdlmlbjdecnmkknjcfcp',
			'SocialData API': 'socialdata.tools/',
			'SolG': 'github.com/yezz123/SoIG',
			'SourcingLab: Pinterest': 'sourcinglab.io/search/pinterest',
			'Suggest me a subreddit': 'nikas.praninskas.com/suggest-subreddit',
			'SóTugas': 'sotugas.com/',
			'Telegram Channels Search': 'xtea.io/ts_en.html',
			'Telegram Channels': 'tlgrm.eu/channels',
			'Telegram Scraper': 'github.com/th3unkn0n/TeleGram-Scraper',
			'Telegram-osint-lib': 'github.com/Postuf/telegram-osint-lib',
			'The Favourite OnlyFans search': 'onlyfansfinder.co/',
			'TikTok Video Downloader': 'ssstik.io/en-1',
			'TikTok hashtag analysis toolset': 'github.com/bellingcat/tiktok-hashtag-analysis',
			'Tinfoleak': 'tinfoleak.com/',
			'Top.gg': 'top.gg/',
			'TweetDeck': 'tweetdeck.twitter.com/',
			'Twitonomy': 'www.twitonomy.com/',
			'Twitter Advanced Search': 'twitter.com/search-advanced',
			'Twitter Video Downloader': 'twittervideodownloader.com/',
			'Twitter search tool': 'www.aware-online.com/en/osint-tools/twitter-search-tool/',
			'Universal Reddit Scraper (URS)': 'github.com/JosephLai241/URS',
			'Unofficial Discord Lookup': 'discord.id/',
			'Verificador de enlaces de CrowdTangle': 'apps.crowdtangle.com/chrome-extension',
			'Vizit': 'redditstuff.github.io/sna/vizit',
			'Wayback Tweets': 'waybacktweets.streamlit.app/',
			'Whatsapp Monitor': 'github.com/ErikTschierschke/WhatsappMonitor',
			'Who posted this': 'whopostedwhat.com/', 'Facebook Search': 'www.sowsearch.info/',
			'_IntelligenceX: Telegram': 'intelx.io/tools?tab=telegram',
			'exolyt': 'exolyt.com/',
			'git-hound': 'github.com/tillson/git-hound',
			'gitGraber': 'github.com/hisxo/gitGraber',
			'informer': 'github.com/paulpierre/informer',
			'instalooter': 'pypi.org/project/instalooter/',
			'instanavigation': 'instanavigation.com/',
			'memory.lol': 'memory.lol/app/',
			'smat': 'www.smat-app.com/timeline',
			'socid_extractor': 'github.com/soxoj/socid_extractor',
			'telegram-history-dump': 'github.com/tvdstaaij/telegram-history-dump',
			'toutatis': 'pypi.org/project/toutatis/',
			'tweeterid': 'tweeterid.com/',
			'whatsfoto': 'github.com/zoutepopcorn/whatsfoto',
            'AddMeS': 'addmes.io',
            'AddMeSnaps': 'www.addmesnaps.com',
            'Analizador de Perfiles': 'inflact.com',
            'AnalyzeID': 'analyzeid.com',
            'Aplicaciones de Facebook': 'khalil-shreateh.com',
            'Awesome Lists': 'awesomelists.top',
            'BirdHunt': 'birdhunt.huntintel.io',
            'Búsqueda de Recuperación de Facebook': 'www.facebook.com',
            'ChatBottle: Telegram': 'chatbottle.co',
            'ChatToday': 'chattoday.com',
            'CoderStats': 'coderstats.net',
            'Commit-stream': 'github.com',
            'CrossLinked': 'github.com',
            'Deleted Tweet Finder': 'cache.digitaldigging.org',
            'Digital Privacy': 'github.com',
            'Disboard': 'disboard.org',
            'Discord.name': 'discord.name',
            'DiscordOSINT': 'github.com',
            'DownAlbum': 'chrome.google.com',
            'Download Twitter Data': 'www.twtdata.com',
            'DumpItBlue+': 'chrome.google.com',
            'Encontrar ID de Usuario de Instagram': 'www.codeofaninja.com',
            'Exportar Comentarios': 'exportcomments.com',
            'Exportgram': 'exportgram.net',
            'F5BOT': 'f5bot.com',
            'Facebook Graph Searcher': 'intelx.io',
            'Facebook People Search': 'www.facebook.com',
            'Facebook Search': 'www.sowsearch.info',
            'FacebookMatrix': 'plessas.net',
            'Fansearch': 'www.fansearch.com',
            'Fansmetrics': 'fansmetrics.com',
            'Find Github User ID': 'caius.github.io',
            'Findr.fans': 'findr.fans',
            'Foller': 'foller.me',
            'FollowerWonk': 'followerwonk.com',
            'Free People Search Tool': 'freepeoplesearchtool.com',
            'Fulldp': 'fulldp.co',
            'GH Archive': 'www.gharchive.org',
            'Gebruikersnamen: Snapchat': 'gebruikersnamen.nl',
            'GhostCodes': 'www.ghostcodes.com',
            'Git-Awards': 'git-awards.com',
            'GitGot': 'github.com',
            'GitHut': 'githut.info',
            'Github Dorks': 'github.com',
            'Github Stars': 'githubstars.com',
            'Github Trending RSS': 'mshibanami.github.io',
            'Github Username Search Engine': 'githubnotes-47071.firebaseapp.com',
            'Hubite': 'hubite.com',
            'IMGinn.io': 'imginn.io',
            'InSpy': 'github.com',
            'InstaFreeView': 'instafreeview.com',
            'Instahunt': 'instahunt.huntintel.io',
            'Instaloader': 'github.com',
            'Integraciones IFTTT de Instagram': 'ifttt.com',
            'IntelligenceX Linkedin': 'intelx.io',
            'Karma Decay': 'karmadecay.com',
            'La búsqueda ha vuelto': 'searchisback.com',
            'LinkedIn Boolean Search': 'linkedprospect.com',
            'LinkedInt': 'github.com',
            'Linkedin Search Tool': 'inteltechniques.com',
            'Lookup-id.com': 'lookup-id.com',
            'Lookupguru': 'lookup.guru',
            'Lyzem.com': 'lyzem.com',
            'Mavekite': 'mavekite.com',
            'Mostly Harmless': 'kerrick.github.io',
            'Network Tool': 'osome.iu.edu',
            'OSINT Combine: Analizador de Publicaciones de Reddit': 'www.osintcombine.com',
            'OSINT Combine: Snapchat MultiViewer': 'www.osintcombine.com',
            'OnlyFinder': 'onlyfinder.com',
            'OnlySearch': 'onlysearch.co',
            'Osintgram': 'github.com',
            'Phantom Buster': 'phantombuster.com',
            'Pickuki': 'www.picuki.com',
            'Pingroupie': 'pingroupie.com',
            'Pinterest Guest': 'addons.mozilla.org',
            'Pinterest Photo Downloader': 'www.expertsphp.com',
            'Programmable Search Engine': 'cse.google.com',
            'Quién publicó qué': 'whopostedwhat.com',
            'ReSavr': 'www.resavr.com',
            'Readr for Reddit': 'chrome.google.com',
            'RecruitEm': 'recruitin.net',
            'Reddit Archive': 'www.redditarchive.com',
            'Reddit Comment Search': 'redditcommentsearch.com',
            'Reddit Enhancement Suite (Complemento de Firefox)': 'addons.mozilla.org',
            'Reddit Enhancement Suite (Extensión de Chrome)': 'chrome.google.com',
            'Reddit Hacks': 'github.com',
            'Reddit List': 'redditlist.com',
            'Reddit Search (cemulate)': 'cemulate.github.io',
            'Reddit Search (react-reddit-search-app)': 'react-reddit-search-app.web.app',
            'Reddit Search (realsrikar)': 'realsrikar.github.io',
            'Reddit Search (reddit-search)': 'reddit-search.surge.sh',
            'Reddit Search (redditsearch.io)': 'www.redditsearch.io',
            'Reddit Search (viralharia)': 'viralharia.github.io',
            'Reddit Shell': 'redditshell.com',
            'Reddit Stream': 'reddit-stream.com',
            'Reddit User Analyser': 'atomiks.github.io',
            'Redditery': 'www.redditery.com',
            'Redective': 'redective.com',
            'Reditr': 'reditr.com',
            'Reeddit': 'reedditapp.com',
            'Reverse Email Lookup': 'www.reversecontact.com',
            'RocketReach': 'rocketreach.co',
            'Similarfans': 'similarfans.com',
            'SimpleScraper OSINT': 'airtable.com',
            'Skypli': 'www.skypli.com',
            'Snap Map': 'map.snapchat.com',
            'Snap Political Ads Library': 'www.snap.com',
            'SnapInsta': 'snapinsta.app',
            'SnapIntel': 'github.com',
            'Snapchat-mapscraper': 'github.com',
            'Social Bearing': 'socialbearing.com',
            'Social Finder': 'socialfinder.app',
            'Social Searcher': 'www.social-searcher.com',
            'SocialAnalyzer - Análisis y Sentimiento Social': 'chromewebstore.google.com',
            'SocialData API': 'socialdata.tools',
            'SolG': 'github.com',
            'SourcingLab: Pinterest': 'sourcinglab.io',
            'StalkFace': 'stalkface.com',
            'Subreddits': 'subreddits.org',
            'Suggest me a subreddit': 'nikas.praninskas.com',
            'SóTugas': 'sotugas.com',
            'Tailwind': 'www.tailwindapp.com',
            'Telegram Channels Search': 'xtea.io',
            'Telegram Channels': 'tlgrm.eu',
            'Telegram Directory': 'tdirectory.me',
            'Telegram Group': 'www.telegram-group.com',
            'Telegram Scraper': 'github.com',
            'Telegram-osint-lib': 'github.com',
            'Tgram.io': 'tgram.io',
            'Tgstat RU': 'tgstat.ru',
            'Tgstat.com': 'tgstat.com',
            'The Favourite OnlyFans search': 'onlyfansfinder.co',
            'TikTok Video Downloader': 'ssstik.io',
            'TikTok hashtag analysis toolset': 'github.com',
            'Tinfoleak': 'tinfoleak.com',
            'Top.gg': 'top.gg',
            'TweetDeck': 'tweetdeck.twitter.com',
            'Twitonomy': 'www.twitonomy.com',
            'Twitter Advanced Search': 'twitter.com',
            'Twitter Video Downloader': 'twittervideodownloader.com',
            'Twitter search tool': 'www.aware-online.com',
            'Universal Reddit Scraper (URS)': 'github.com',
            'Unofficial Discord Lookup': 'discord.id',
            'Verificador de enlaces de CrowdTangle': 'apps.crowdtangle.com',
            'Vizit': 'redditstuff.github.io',
            'Wayback Tweets': 'waybacktweets.streamlit.app',
            'WhatsApp Fake Chat': 'www.fakewhats.com',
            'Whatsapp Monitor': 'github.com',
            'Who posted this': 'whopostedwhat.com',
            'Wisdom of Reddit': 'wisdomofreddit.com',
            '_IntelligenceX: Telegram': 'intelx.io',
            'addmeContacts': 'add-me-contacts.com',
            'checkwa': 'checkwa.online',
            'exolyt': 'exolyt.com',
            'git-hound': 'github.com',
            'gitGraber': 'github.com',
            'informer': 'github.com',
            'instalooter': 'pypi.org',
            'instanavigation': 'instanavigation.com',
            'memory.lol': 'memory.lol',
            'rdddeck': 'rdddeck.com',
            'redditvids': 'redditvids.com',
            'reddtip': 'www.redditp.com',
            'smat': 'www.smat-app.com',
            'socid_extractor': 'github.com',
            'sowsearch': 'www.sowsearch.info',
            'telegram-history-dump': 'github.com',
            'toutatis': 'pypi.org',
            'tweeterid': 'tweeterid.com',
            'uforio': 'uforio.com',
            'whatsfoto': 'github.com',
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
