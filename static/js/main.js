// COMPLETE main.js - Glassmorphism Portfolio (Django/Bootstrap 5)
// All CSS interactions preserved + optimized (debounced, single observers)

document.addEventListener('DOMContentLoaded', function() {
  console.log('Shivam Portfolio - Glassmorphism JS Loaded');

  // GLOBAL SCROLL LISTENER (debounced)
  let ticking = false;
  let lastScrollY = window.scrollY;
  function updateScroll() {
    const navbar = document.getElementById('mainNavbar');
    if (window.scrollY > 50) {
      navbar?.classList.add('scrolled');
    } else {
      navbar?.classList.remove('scrolled');
    }
    // Hide/show direction
    if (window.scrollY > lastScrollY + 100) {
      navbar.style.transform = 'translateY(-100%)';
    } else {
      navbar.style.transform = 'translateY(0)';
    }
    lastScrollY = window.scrollY;
    ticking = false;
  }
  window.addEventListener('scroll', () => {
    if (!ticking) {
      requestAnimationFrame(updateScroll);
      ticking = true;
    }
  });

  // ALERT AUTO-DISMISS
  document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }, 5000);
  });

  // SMOOTH SCROLLING + ACTIVE NAV
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      target?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Mobile close
      const navbarNav = document.getElementById('navbarNav');
      const navbarToggler = document.querySelector('.navbar-toggler');
      navbarNav?.classList.remove('show');
      navbarToggler?.setAttribute('aria-expanded', 'false');
    });
  });

  // MOBILE NAVBAR
  const navbarToggler = document.querySelector('.navbar-toggler');
  const navbarNav = document.getElementById('navbarNav');
  navbarToggler?.addEventListener('click', function() {
    const isExpanded = navbarNav.classList.contains('show');
    this.setAttribute('aria-expanded', !isExpanded);
  });
  // Outside close
  document.addEventListener('click', e => {
    if (!navbarToggler?.contains(e.target) && !navbarNav?.contains(e.target)) {
      navbarNav?.classList.remove('show');
      navbarToggler?.setAttribute('aria-expanded', 'false');
    }
  });

  // BUTTON LOADING (Resume/Downloads)
  document.querySelectorAll('.btn-primary[href*="resume"], .btn-primary[href*="download"]').forEach(btn => {
    btn.addEventListener('click', function() {
      this.classList.add('loading');
      if (!this.querySelector('.btn-spinner')) {
        const spinner = document.createElement('div');
        spinner.className = 'btn-spinner';
        spinner.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>';
        this.prepend(spinner);
        const text = document.createElement('span');
        text.className = 'btn-text';
        text.textContent = this.textContent.trim();
        this.appendChild(text);
      }
    });
  });

  // ANIMATION ON SCROLL (IntersectionObserver)
  const observerOptions = { threshold: 0.1, rootMargin: '0px 0px -50px 0px' };
  const revealObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('animate-fade-in');
        revealObserver.unobserve(entry.target);
      }
    });
  }, observerOptions);
  document.querySelectorAll('.glassmorphism, .stat-card, .skill-card, .project-card, .cert-card, [class*="animate-"]').forEach(el => revealObserver.observe(el));

  // BACK TO TOP
  const backToTop = document.querySelector('.footer-back-to-top');
  if (backToTop) {
    window.addEventListener('scroll', () => {
      backToTop.style.display = window.scrollY > 500 ? 'flex' : 'none';
    });
    backToTop.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  // SKILL BAR ANIMATIONS
  const skillBars = document.querySelectorAll('.skill-bar');
  const skillObserver = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const bar = entry.target;
        const width = bar.dataset.width || '80%';
        bar.style.width = width;
        skillObserver.unobserve(bar);
      }
    });
  }, { threshold: 0.5 });
  skillBars.forEach(bar => skillObserver.observe(bar));

  // COUNTER ANIMATIONS
  function animateCounters() {
    document.querySelectorAll('.counter[data-target]').forEach(counter => {
      const target = parseInt(counter.dataset.target);
      const num = parseInt(counter.textContent) || 0;
      if (Math.abs(counter.getBoundingClientRect().top - window.innerHeight) < 100) {
        let current = num;
        const increment = target / 200;
        function update() {
          if (current < target) {
            current += increment;
            counter.textContent = Math.floor(current).toLocaleString();
            requestAnimationFrame(update);
          } else {
            counter.textContent = target.toLocaleString();
          }
        }
        update();
      }
    });
  }
  window.addEventListener('scroll', animateCounters);

  // NAV LINK SHINE
  document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('mouseenter', () => link.style.setProperty('--shine-progress', '100%'));
    link.addEventListener('mouseleave', () => link.style.setProperty('--shine-progress', '0%'));
  });

  // PLATFORM LINKS + FOOTER
  document.querySelectorAll('.platform-link').forEach(link => {
    const icon = link.querySelector('i');
    link.addEventListener('mouseenter', () => {
      icon.style.animation = 'iconPulse 0.6s ease-in-out';
    });
    link.addEventListener('mouseleave', () => {
      icon.style.animation = '';
    });
  });
  const heart = document.querySelector('footer .fa-heart');
  if (heart) heart.style.animation = 'heartbeat 1.5s ease-in-out infinite';

  // CONTACT FORM (if present)
  const contactForm = document.getElementById('contactForm');
  if (contactForm) {
    const submitBtn = document.querySelector('.submit-btn');
    const inputs = contactForm.querySelectorAll('.form-input');
    inputs.forEach(input => {
      input.addEventListener('input', () => {
        input.classList.toggle('valid', input.value.length > 0);
      });
    });
    contactForm.addEventListener('submit', e => {
      e.preventDefault();
      submitBtn.classList.add('loading');
      submitBtn.disabled = true;
      // Simulate (replace with fetch/Django)
      setTimeout(() => {
        submitBtn.classList.remove('loading');
        submitBtn.disabled = false;
        // Reset
        contactForm.reset();
        inputs.forEach(i => i.classList.remove('valid'));
      }, 2000);
    });
  }

  // PROJECT CARDS 3D TILT (if present)
  document.querySelectorAll('.project-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const tiltX = (y / rect.height - 0.5) * 15;
      const tiltY = (x / rect.width - 0.5) * 15;
      card.style.transform = `rotateX(${tiltX}deg) rotateY(${tiltY}deg) scale(1.05)`;
      card.style.setProperty('--shine-x', (x / rect.width));
      card.style.setProperty('--glare-intensity', Math.min(x / rect.width * 2, 1));
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'rotateX(0deg) rotateY(0deg) scale(1)';
      card.style.setProperty('--shine-x', '0.5');
      card.style.setProperty('--glare-intensity', '0');
    });
  });

  // NOTIFICATION SYSTEM
  function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i> ${message}`;
    document.body.appendChild(notification);
    setTimeout(() => {
      notification.style.transform = 'translateY(0) scale(1)';
      notification.style.opacity = '1';
    }, 100);
    setTimeout(() => {
      notification.style.transform = 'translateY(-20px) scale(0.9)';
      notification.style.opacity = '0';
      setTimeout(() => notification.remove(), 300);
    }, 3000);
  }
});
// SKILL BAR ANIMATIONS (Fixed for Django proficiency)
const skillBars = document.querySelectorAll('.skill-bar');
const skillObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const bar = entry.target;
      let width = bar.dataset.width; // Gets "90" from Django
      
      // FIX: Add % if missing (Django sends raw numbers)
      if (width && !width.includes('%')) {
        width += '%';
      }
      
      // Fallbacks
      if (!width || width === '0%') {
        width = '80%';
      }
      
      bar.style.width = width;
      skillObserver.unobserve(bar);
    }
  });
}, { threshold: 0.5 });

skillBars.forEach(bar => skillObserver.observe(bar));

document.addEventListener("DOMContentLoaded", () => {
  const bars = document.querySelectorAll(".skill-bar");

  bars.forEach(bar => {
    const width = bar.getAttribute("data-width");
    setTimeout(() => {
      bar.style.width = width + "%";
    }, 300);
  });
});