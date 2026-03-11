// ========================================
// COMPLETE PORTFOLIO JS - OPTIMIZED
// All features in ONE file, no conflicts
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // CORE ELEMENTS
    const navbar = document.getElementById('mainNavbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse') || document.getElementById('navbarNav');
    const backToTop = document.querySelector('.footer-back-to-top') || createBackToTop();
    const form = document.querySelector('form');
    const submitBtn = form?.querySelector('button[type="submit"]');

    // PERFORMANCE: Throttled scroll handler
    let ticking = false;
    let scrollY = 0;

    const updateScroll = () => {
        scrollY = window.scrollY;
        
        // Navbar scroll effect
        navbar?.classList.toggle('scrolled', scrollY > 50);
        
        // Back to top button
        backToTop.style.display = scrollY > 300 ? 'flex' : 'none';
        
        ticking = false;
    };

    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateScroll);
            ticking = true;
        }
    }, { passive: true });

    // NAVBAR FUNCTIONALITY
    navLinks.forEach(link => {
        // Close mobile menu on click
        link.addEventListener('click', () => {
            if (window.innerWidth < 992 && navbarCollapse?.classList.contains('show')) {
                new bootstrap.Collapse(navbarCollapse, { toggle: false }).hide();
            }
        });

        // Active link highlighting
        if (link.href === window.location.href || 
            link.getAttribute('href') === window.location.pathname) {
            link.classList.add('active');
        }
    });

    // FORM HANDLING
    if (form && submitBtn) {
        form.addEventListener('submit', () => {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        });

        // Reset on validation errors
        form.addEventListener('input', () => {
            if (!submitBtn.disabled && form.querySelector('.text-danger')) {
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
            }
        });
    }

    // SINGLE UNIVERSAL ANIMATION OBSERVER
    const animObserver = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0) scale(1)';
                }, index * 150);
            }
        });
    }, { 
        threshold: 0.1, 
        rootMargin: '0px 0px -50px 0px' 
    });

    // Initialize and observe ALL cards
    document.querySelectorAll('.stat-card, .cert-card, .skill-card, .project-card, .glassmorphism, .hover-scale').forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(40px) scale(0.95)';
        el.style.transition = `all 0.8s cubic-bezier(0.4, 0, 0.2, 1) ${index * 0.1}s`;
        animObserver.observe(el);
    });

    // SKILL BARS - DEDICATED OBSERVER
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const skillBars = entry.target.querySelectorAll('.skill-bar');
                skillBars.forEach((bar, index) => {
                    const width = bar.dataset.width || bar.style.width || '80%';
                    setTimeout(() => {
                        bar.style.width = width;
                    }, index * 200);
                });
                skillObserver.unobserve(entry.target);
            }
        });
    }, { 
        threshold: 0.5, 
        rootMargin: '0px 0px -100px 0px' 
    });

    document.querySelectorAll('#skills .skill-card, .skills-section .skill-card').forEach(card => {
        skillObserver.observe(card);
    });

    // HERO PARALLAX
    const heroImg = document.querySelector('.hero-section img');
    if (heroImg) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset * 0.3;
            heroImg.style.transform = `translateY(${scrolled}px) scale(1.02)`;
        }, { passive: true });
    }

    // COUNTER ANIMATIONS
    const counters = document.querySelectorAll('.stat-card h3, .stat-number');
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.textContent.replace(/[^0-9]/g, ''));
                let current = 0;
                const increment = target / 100;
                const timer = setInterval(() => {
                    current += increment;
                    if (current >= target) {
                        el.textContent = target;
                        clearInterval(timer);
                    } else {
                        el.textContent = Math.floor(current);
                    }
                }, 20);
                counterObserver.unobserve(entry.target);
            }
        });
    });

    counters.forEach(counter => counterObserver.observe(counter));

    // SMOOTH SCROLLING
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', (e) => {
            const target = document.querySelector(anchor.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // HERO FADE-IN
    document.querySelectorAll('.animate-fade-in').forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });

    console.log('🎉 Portfolio JS loaded perfectly!');
});

// HELPER: Create back-to-top if missing
function createBackToTop() {
    const btn = document.createElement('a');
    btn.href = '#';
    btn.className = 'footer-back-to-top';
    btn.innerHTML = '<i class="fas fa-chevron-up"></i>';
    btn.title = 'Back to Top';
    document.body.appendChild(btn);
    return btn;
}
