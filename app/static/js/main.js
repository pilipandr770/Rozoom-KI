// Main JavaScript file for the site

// Handle flash message close buttons
document.addEventListener('DOMContentLoaded', function() {
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
