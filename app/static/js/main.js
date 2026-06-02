// Main JavaScript file for the site

// Handle flash message close buttons
document.addEventListener('DOMContentLoaded', function() {
  const ACTIVE_EXPERIMENT = 'home_cta_order_v1';

  function trackExperiment(eventName, payload) {
    if (typeof window.fbq === 'function') {
      window.fbq('trackCustom', eventName, payload);
    }
  }

  function initHomeCtaExperiment() {
    const heroCta = document.querySelector('.video-hero .hero-cta');
    if (!heroCta) {
      return;
    }

    const primaryOffer = heroCta.querySelector('[data-exp-role="primary-offer"]');
    const consultationOffer = heroCta.querySelector('[data-exp-role="consultation-offer"]');

    if (!primaryOffer || !consultationOffer) {
      return;
    }

    const storageKey = 'exp_' + ACTIVE_EXPERIMENT;
    let variant = window.localStorage.getItem(storageKey);

    if (variant !== 'A' && variant !== 'B') {
      variant = Math.random() < 0.5 ? 'A' : 'B';
      window.localStorage.setItem(storageKey, variant);
    }

    if (variant === 'B') {
      heroCta.insertBefore(consultationOffer, primaryOffer);
    }

    trackExperiment('Experiment_Exposure', {
      experiment_id: ACTIVE_EXPERIMENT,
      variant: variant,
      page: window.location.pathname
    });

    heroCta.querySelectorAll('[data-cta-track]').forEach(function(cta) {
      cta.addEventListener('click', function() {
        trackExperiment('Experiment_Conversion', {
          experiment_id: ACTIVE_EXPERIMENT,
          variant: variant,
          cta_id: cta.getAttribute('data-cta-id') || 'unknown',
          page: window.location.pathname
        });
      });
    });
  }

  initHomeCtaExperiment();

  function trackCta(payload) {
    if (typeof window.fbq === 'function') {
      window.fbq('trackCustom', 'CTA_Click', payload);
    }
  }

  document.addEventListener('click', function(event) {
    const ctaElement = event.target.closest('[data-cta-track]');
    if (!ctaElement) {
      return;
    }

    const payload = {
      cta_id: ctaElement.getAttribute('data-cta-id') || 'unknown',
      cta_location: ctaElement.getAttribute('data-cta-location') || window.location.pathname,
      cta_text: (ctaElement.getAttribute('data-cta-text') || ctaElement.textContent || '').trim().slice(0, 120),
      destination: ctaElement.getAttribute('href') || ''
    };

    trackCta(payload);
  });

  document.querySelectorAll('form[data-cta-form]').forEach(function(form) {
    form.addEventListener('submit', function() {
      const payload = {
        cta_id: form.getAttribute('data-cta-id') || 'form-submit',
        cta_location: form.getAttribute('data-cta-location') || window.location.pathname,
        cta_text: form.getAttribute('data-cta-text') || 'form_submit',
        destination: form.getAttribute('action') || window.location.pathname
      };

      trackCta(payload);
    });
  });

  const nav = document.querySelector('.nav');
  const navToggle = document.getElementById('nav-toggle');

  if (nav && navToggle) {
    const closeNav = () => {
      nav.classList.remove('is-open');
      navToggle.setAttribute('aria-expanded', 'false');
    };

    navToggle.addEventListener('click', function() {
      const isOpen = nav.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });

    nav.querySelectorAll('.nav-panel a').forEach(function(link) {
      link.addEventListener('click', function() {
        if (window.innerWidth <= 980) {
          closeNav();
        }
      });
    });

    document.addEventListener('click', function(event) {
      if (!nav.contains(event.target)) {
        closeNav();
      }
    });

    document.addEventListener('keydown', function(event) {
      if (event.key === 'Escape') {
        closeNav();
      }
    });

    window.addEventListener('resize', function() {
      if (window.innerWidth > 980) {
        closeNav();
      }
    });
  }

  const flashMessages = document.querySelectorAll('.flash-message');
  
  flashMessages.forEach(message => {
    const closeButton = message.querySelector('.flash-close');
    
    if (closeButton) {
      closeButton.addEventListener('click', function() {
        message.style.opacity = '0';
        message.style.transform = 'translateY(-10px)';
        message.style.transition = 'opacity 0.3s, transform 0.3s';
        
        setTimeout(() => {
          message.remove();
        }, 300);
      });
    }
    
    // Auto-hide success messages after 5 seconds
    if (message.classList.contains('flash-success')) {
      setTimeout(() => {
        if (message.parentNode) {
          message.style.opacity = '0';
          message.style.transform = 'translateY(-10px)';
          message.style.transition = 'opacity 0.3s, transform 0.3s';
          
          setTimeout(() => {
            if (message.parentNode) {
              message.remove();
            }
          }, 300);
        }
      }, 5000);
    }
  });
  
  // Form validation for contact form
  const contactForm = document.querySelector('.contact-form');
  
  if (contactForm) {
    contactForm.addEventListener('submit', function(event) {
      const nameInput = document.getElementById('name');
      const emailInput = document.getElementById('email');
      const messageInput = document.getElementById('message');
      const privacyCheckbox = document.querySelector('input[name="privacy_consent"]');
      
      let isValid = true;
      
      // Simple validation
      if (!nameInput.value.trim()) {
        highlightError(nameInput);
        isValid = false;
      } else {
        removeError(nameInput);
      }
      
      if (!emailInput.value.trim() || !emailInput.value.includes('@') || !emailInput.value.includes('.')) {
        highlightError(emailInput);
        isValid = false;
      } else {
        removeError(emailInput);
      }
      
      if (!messageInput.value.trim()) {
        highlightError(messageInput);
        isValid = false;
      } else {
        removeError(messageInput);
      }
      
      if (privacyCheckbox && !privacyCheckbox.checked) {
        privacyCheckbox.parentElement.classList.add('checkbox-error');
        isValid = false;
      } else if (privacyCheckbox) {
        privacyCheckbox.parentElement.classList.remove('checkbox-error');
      }
      
      if (!isValid) {
        event.preventDefault();
      }
    });
  }
  
  function highlightError(element) {
    element.classList.add('input-error');
    element.addEventListener('input', function onInput() {
      element.classList.remove('input-error');
      element.removeEventListener('input', onInput);
    });
  }
  
  function removeError(element) {
    element.classList.remove('input-error');
  }
});
