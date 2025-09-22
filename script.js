// Utilidades
const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => document.querySelectorAll(selector);

// Variables globales
let isMenuOpen = false;
let currentTab = 'database';

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
    initializeNavigation();
    initializeTabs();
    initializeAnimations();
    initializeCopyButtons();
    initializeScrollEffects();
    initializeMobileMenu();
});

// Navegación suave
function initializeNavigation() {
    const navLinks = $$('.nav-link');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            
            if (target.startsWith('#')) {
                const element = $(target);
                if (element) {
                    const offsetTop = element.offsetTop - 70; // Altura del navbar
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
            
            // Cerrar menú móvil si está abierto
            if (isMenuOpen) {
                toggleMobileMenu();
            }
        });
    });
    
    // Navegación de botones hero
    const heroButtons = $$('.hero-buttons .btn');
    heroButtons.forEach(btn => {
        btn.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href.startsWith('#')) {
                e.preventDefault();
                const element = $(href);
                if (element) {
                    const offsetTop = element.offsetTop - 70;
                    window.scrollTo({
                        top: offsetTop,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

// Sistema de tabs
function initializeTabs() {
    const tabButtons = $$('.tab-btn');
    const tabPanes = $$('.tab-pane');
    
    tabButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const targetTab = this.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });
}

function switchTab(tabId) {
    // Remover clases active de todos los botones y panes
    $$('.tab-btn').forEach(btn => btn.classList.remove('active'));
    $$('.tab-pane').forEach(pane => pane.classList.remove('active'));
    
    // Añadir clase active al botón y pane correspondiente
    $(`[data-tab="${tabId}"]`).classList.add('active');
    $(`#${tabId}`).classList.add('active');
    
    currentTab = tabId;
    
    // Animar las barras del gráfico si es la tab de visualización
    if (tabId === 'visualization') {
        setTimeout(animateChartBars, 300);
    }
}

// Animaciones
function initializeAnimations() {
    // Observador de intersección para animaciones de entrada
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Animaciones específicas
                if (entry.target.classList.contains('feature-card')) {
                    animateFeatureCard(entry.target);
                }
                
                if (entry.target.classList.contains('demo-card')) {
                    animateDemoCard(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // Observar elementos
    $$('.feature-card, .demo-card, .step').forEach(el => {
        observer.observe(el);
    });
    
    // Animaciones continuas
    startContinuousAnimations();
}

function animateFeatureCard(card) {
    const icon = card.querySelector('.feature-icon');
    if (icon) {
        icon.style.transform = 'scale(1.1) rotate(5deg)';
        setTimeout(() => {
            icon.style.transform = 'scale(1) rotate(0deg)';
        }, 300);
    }
}

function animateDemoCard(card) {
    card.style.transform = 'translateY(20px)';
    card.style.opacity = '0';
    
    setTimeout(() => {
        card.style.transition = 'all 0.6s ease';
        card.style.transform = 'translateY(0)';
        card.style.opacity = '1';
    }, 100);
}

function animateChartBars() {
    const bars = $$('.bar');
    bars.forEach((bar, index) => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, index * 200);
    });
}

function startContinuousAnimations() {
    // Animación de las notas musicales
    const notes = $$('.note');
    notes.forEach((note, index) => {
        setInterval(() => {
            note.style.transform = 'translateY(-15px) scale(1.1)';
            setTimeout(() => {
                note.style.transform = 'translateY(0) scale(1)';
            }, 300);
        }, 3000 + (index * 500));
    });
    
    // Animación de las líneas del staff
    const staffLines = $$('.staff-line');
    staffLines.forEach((line, index) => {
        setInterval(() => {
            line.style.transform = 'scaleX(1.05)';
            setTimeout(() => {
                line.style.transform = 'scaleX(1)';
            }, 200);
        }, 4000 + (index * 100));
    });
}

// Funcionalidad de copia de código
function initializeCopyButtons() {
    const copyButtons = $$('.copy-btn');
    
    copyButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const codeBlock = this.closest('.code-block');
            const code = codeBlock.querySelector('code');
            
            if (code) {
                copyToClipboard(code.textContent, this);
            }
        });
    });
}

function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        // Cambiar ícono temporalmente
        const originalIcon = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i>';
        button.style.color = '#48bb78';
        
        setTimeout(() => {
            button.innerHTML = originalIcon;
            button.style.color = '';
        }, 2000);
    }).catch(err => {
        console.error('Error al copiar al portapapeles:', err);
        
        // Fallback para navegadores más antiguos
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        
        try {
            document.execCommand('copy');
            const originalIcon = button.innerHTML;
            button.innerHTML = '<i class="fas fa-check"></i>';
            button.style.color = '#48bb78';
            
            setTimeout(() => {
                button.innerHTML = originalIcon;
                button.style.color = '';
            }, 2000);
        } catch (fallbackErr) {
            console.error('Error en el fallback de copia:', fallbackErr);
        }
        
        document.body.removeChild(textArea);
    });
}

// Efectos de scroll
function initializeScrollEffects() {
    window.addEventListener('scroll', handleScroll);
    
    // Inicializar el estado del navbar
    handleNavbarScroll();
}

function handleScroll() {
    handleNavbarScroll();
    handleScrollProgress();
    handleParallaxEffects();
}

function handleNavbarScroll() {
    const navbar = $('.navbar');
    const scrolled = window.scrollY > 50;
    
    if (scrolled) {
        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
        navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
    } else {
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
        navbar.style.boxShadow = 'none';
    }
}

function handleScrollProgress() {
    const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
    const scrolled = (winScroll / height) * 100;
    
    // Crear barra de progreso si no existe
    let progressBar = $('#scroll-progress');
    if (!progressBar) {
        progressBar = document.createElement('div');
        progressBar.id = 'scroll-progress';
        progressBar.style.cssText = `
            position: fixed;
            top: 70px;
            left: 0;
            width: ${scrolled}%;
            height: 3px;
            background: linear-gradient(135deg, #667eea, #764ba2);
            z-index: 1001;
            transition: width 0.3s ease;
        `;
        document.body.appendChild(progressBar);
    } else {
        progressBar.style.width = `${scrolled}%`;
    }
}

function handleParallaxEffects() {
    const scrolled = window.scrollY;
    const heroVisual = $('.hero-visual');
    
    if (heroVisual) {
        heroVisual.style.transform = `translateY(${scrolled * 0.3}px)`;
    }
    
    // Efecto parallax en las notas musicales
    const notes = $$('.note');
    notes.forEach((note, index) => {
        const speed = 0.2 + (index * 0.1);
        note.style.transform += ` translateY(${scrolled * speed}px)`;
    });
}

// Menú móvil
function initializeMobileMenu() {
    const hamburger = $('.hamburger');
    
    if (hamburger) {
        hamburger.addEventListener('click', toggleMobileMenu);
    }
    
    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function(e) {
        const navMenu = $('.nav-menu');
        const hamburger = $('.hamburger');
        
        if (isMenuOpen && !navMenu.contains(e.target) && !hamburger.contains(e.target)) {
            toggleMobileMenu();
        }
    });
}

function toggleMobileMenu() {
    const navMenu = $('.nav-menu');
    const hamburger = $('.hamburger');
    const bars = $$('.bar');
    
    isMenuOpen = !isMenuOpen;
    
    navMenu.classList.toggle('active');
    
    // Animar hamburger
    if (isMenuOpen) {
        bars[0].style.transform = 'rotate(-45deg) translate(-5px, 6px)';
        bars[1].style.opacity = '0';
        bars[2].style.transform = 'rotate(45deg) translate(-5px, -6px)';
    } else {
        bars[0].style.transform = 'none';
        bars[1].style.opacity = '1';
        bars[2].style.transform = 'none';
    }
}

// Funciones auxiliares
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Optimizar eventos de scroll
const optimizedScrollHandler = throttle(handleScroll, 16); // ~60fps
window.addEventListener('scroll', optimizedScrollHandler);

// Efectos adicionales para mejorar la experiencia
document.addEventListener('DOMContentLoaded', function() {
    // Precargar imágenes críticas
    preloadCriticalAssets();
    
    // Inicializar lazy loading para imágenes
    initializeLazyLoading();
    
    // Detectar preferencias de movimiento reducido
    handleReducedMotion();
    
    // Mostrar página gradualmente
    showPageGradually();
});

function preloadCriticalAssets() {
    // Precargar fuentes críticas
    const fontPreload = document.createElement('link');
    fontPreload.rel = 'preload';
    fontPreload.href = 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap';
    fontPreload.as = 'style';
    document.head.appendChild(fontPreload);
}

function initializeLazyLoading() {
    const lazyElements = $$('[data-lazy]');
    
    if ('IntersectionObserver' in window) {
        const lazyObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const element = entry.target;
                    if (element.dataset.lazy) {
                        element.src = element.dataset.lazy;
                        element.classList.add('loaded');
                        lazyObserver.unobserve(element);
                    }
                }
            });
        });
        
        lazyElements.forEach(el => lazyObserver.observe(el));
    }
}

function handleReducedMotion() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    
    if (prefersReducedMotion.matches) {
        // Desactivar animaciones para usuarios que prefieren movimiento reducido
        document.documentElement.style.setProperty('--animation-duration', '0s');
        document.documentElement.style.setProperty('--transition-duration', '0s');
    }
}

function showPageGradually() {
    // Mostrar la página gradualmente después de que todo esté cargado
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    window.addEventListener('load', function() {
        setTimeout(() => {
            document.body.style.opacity = '1';
        }, 100);
    });
}

// Funciones de desarrollo y debug
function addDebugInfo() {
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        console.log('🎵 Music Analyzer - Página Web Cargada');
        console.log('🎹 Desarrollado para análisis musical avanzado');
        console.log('🎼 Soporta archivos KERN y MusicXML');
        
        // Añadir indicador visual de desarrollo
        const devIndicator = document.createElement('div');
        devIndicator.textContent = 'DEV MODE';
        devIndicator.style.cssText = `
            position: fixed;
            top: 80px;
            right: 10px;
            background: #f56565;
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 10px;
            z-index: 9999;
            font-family: monospace;
        `;
        document.body.appendChild(devIndicator);
    }
}

// Ejecutar info de debug
addDebugInfo();

// Exportar funciones para uso global si es necesario
window.MusicAnalyzer = {
    switchTab,
    toggleMobileMenu,
    copyToClipboard
};