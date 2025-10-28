/* ===== FLOATING HEADER JAVASCRIPT - TRAMITOLOGÍA ABC ===== */

// Inicialización del header flotante
document.addEventListener('DOMContentLoaded', function() {
    initFloatingHeader();
});

function initFloatingHeader() {
    // Agregar clase al body para el espaciado
    document.body.classList.add('with-floating-header');
    
    // Inicializar funcionalidades
    initScrollEffect();
    initMobileMenu();
    initActiveLinks();
    initSmoothScrolling();
}

// Efecto de scroll del header
function initScrollEffect() {
    window.addEventListener('scroll', function() {
        const header = document.getElementById('floatingHeader');
        if (header) {
            if (window.scrollY > 50) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
        }
    });
}

// Funcionalidad del menú móvil
function initMobileMenu() {
    // Cerrar menú móvil al hacer clic en un enlace
    document.querySelectorAll('.mobile-nav-link').forEach(link => {
        link.addEventListener('click', function() {
            closeMobileMenu();
        });
    });

    // Cerrar menú móvil al hacer clic fuera
    document.addEventListener('click', function(event) {
        const mobileMenu = document.getElementById('mobileMenu');
        const toggleBtn = document.querySelector('.mobile-menu-toggle');
        
        if (mobileMenu && toggleBtn) {
            if (!toggleBtn.contains(event.target) && !mobileMenu.contains(event.target)) {
                closeMobileMenu();
            }
        }
    });

    // Cerrar menú móvil al redimensionar ventana
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            closeMobileMenu();
        }
    });
}

// Función para alternar el menú móvil
function toggleMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    const toggleBtn = document.querySelector('.mobile-menu-toggle i');
    
    if (mobileMenu && toggleBtn) {
        mobileMenu.classList.toggle('active');
        
        if (mobileMenu.classList.contains('active')) {
            toggleBtn.className = 'fas fa-times';
            // Prevenir scroll del body cuando el menú está abierto
            document.body.style.overflow = 'hidden';
        } else {
            toggleBtn.className = 'fas fa-bars';
            document.body.style.overflow = '';
        }
    }
}

// Función para cerrar el menú móvil
function closeMobileMenu() {
    const mobileMenu = document.getElementById('mobileMenu');
    const toggleBtn = document.querySelector('.mobile-menu-toggle i');
    
    if (mobileMenu && toggleBtn) {
        mobileMenu.classList.remove('active');
        toggleBtn.className = 'fas fa-bars';
        document.body.style.overflow = '';
    }
}

// Resaltar enlace activo basado en la URL actual
function initActiveLinks() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-link, .mobile-nav-link');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href').split('/').pop();
        if (linkPage === currentPage) {
            link.classList.add('active');
        }
    });
}

// Scroll suave para enlaces internos
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const headerHeight = document.querySelector('.floating-header').offsetHeight;
                const targetPosition = target.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Cerrar menú móvil si está abierto
                closeMobileMenu();
            }
        });
    });
}

// Función para actualizar enlaces del header (útil para páginas dinámicas)
function updateHeaderLinks(links) {
    const navLinksContainer = document.querySelector('.nav-links');
    const mobileNavLinksContainer = document.querySelector('.mobile-nav-links');
    
    if (navLinksContainer && mobileNavLinksContainer && links) {
        // Limpiar enlaces existentes (excepto los primeros que son fijos)
        const fixedLinks = 2; // Mantener "Inicio" y "Guía Completa"
        
        // Actualizar enlaces de escritorio
        const desktopLinks = navLinksContainer.querySelectorAll('li');
        for (let i = desktopLinks.length - 1; i >= fixedLinks; i--) {
            desktopLinks[i].remove();
        }
        
        // Actualizar enlaces móviles
        const mobileLinks = mobileNavLinksContainer.querySelectorAll('a');
        for (let i = mobileLinks.length - 1; i >= fixedLinks; i--) {
            mobileLinks[i].remove();
        }
        
        // Agregar nuevos enlaces
        links.forEach(link => {
            // Enlace de escritorio
            const li = document.createElement('li');
            const a = document.createElement('a');
            a.href = link.href;
            a.className = 'nav-link';
            a.textContent = link.text;
            li.appendChild(a);
            navLinksContainer.appendChild(li);
            
            // Enlace móvil
            const mobileA = document.createElement('a');
            mobileA.href = link.href;
            mobileA.className = 'mobile-nav-link';
            mobileA.textContent = link.text;
            mobileNavLinksContainer.appendChild(mobileA);
        });
        
        // Reinicializar enlaces activos
        initActiveLinks();
    }
}

// Función para mostrar/ocultar el header
function toggleHeader(show = true) {
    const header = document.getElementById('floatingHeader');
    if (header) {
        if (show) {
            header.style.transform = 'translateY(0)';
            header.style.opacity = '1';
        } else {
            header.style.transform = 'translateY(-100%)';
            header.style.opacity = '0';
        }
    }
}

// Función para cambiar el tema del header (si se necesita)
function setHeaderTheme(theme = 'default') {
    const header = document.getElementById('floatingHeader');
    if (header) {
        // Remover clases de tema existentes
        header.classList.remove('theme-default', 'theme-dark', 'theme-light');
        
        // Agregar nueva clase de tema
        header.classList.add(`theme-${theme}`);
    }
}

// Exportar funciones para uso global
window.FloatingHeader = {
    toggle: toggleMobileMenu,
    close: closeMobileMenu,
    updateLinks: updateHeaderLinks,
    show: () => toggleHeader(true),
    hide: () => toggleHeader(false),
    setTheme: setHeaderTheme
};

