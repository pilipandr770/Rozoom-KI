/**
 * Animation effects for Rozoom-KI website
 */

document.addEventListener('DOMContentLoaded', function() {
  
  // Initialize particle animations if present
  if (document.querySelector('.particle-container')) {
    initParticles();
  }

  // Add floating animation to selected elements
  document.querySelectorAll('.should-float').forEach(el => {
    el.classList.add('floating');
  });

  // Lazy load videos when they come into view
  const videos = document.querySelectorAll('video[data-src]');
  
  if (videos.length > 0) {
    const videoObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const video = entry.target;
          video.src = video.dataset.src;
          video.load();
          observer.unobserve(video);
        }
      });
    });
    
    videos.forEach(video => {
      videoObserver.observe(video);
    });
  }
  
  // Parallax effect for elements with data-parallax attribute
  window.addEventListener('scroll', function() {
    const parallaxElems = document.querySelectorAll('[data-parallax]');
    
    if (parallaxElems.length > 0) {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      parallaxElems.forEach(elem => {
        const speed = elem.dataset.parallax || 0.5;
        elem.style.transform = `translateY(${scrollTop * speed * -1}px)`;
      });
    }
  });
});

/**
 * Initialize particle animation in specified container
 */
function initParticles() {
  const particleContainer = document.querySelector('.particle-container');
  if (!particleContainer) return;
  
  // Create particles
  for (let i = 0; i < 50; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    
    // Random position
    const x = Math.random() * 100;
    const y = Math.random() * 100;
    
    // Random size
    const size = Math.random() * 5 + 1;
    
    // Random opacity
    const opacity = Math.random() * 0.5 + 0.1;
    
    // Random animation duration
    const duration = Math.random() * 20 + 10;
    
    // Set styles
    particle.style.cssText = `
      position: absolute;
      top: ${y}%;
      left: ${x}%;
      width: ${size}px;
      height: ${size}px;
      background: rgba(255, 255, 255, ${opacity});
      border-radius: 50%;
      animation: float ${duration}s linear infinite;
      z-index: 1;
    `;
    
    particleContainer.appendChild(particle);
  }
}

/**
 * Initialize typed text animation
 * @param {string} elementId - ID of element to animate typing in
 * @param {Array} textArray - Array of strings to type
 */
function initTypedText(elementId, textArray) {
  const element = document.getElementById(elementId);
  if (!element || !textArray || !textArray.length) return;
  
  let textIndex = 0;
  let charIndex = 0;
  let isDeleting = false;
  let typingDelay = 100;
  let deletingDelay = 50;
  let newTextDelay = 2000;
  
  function type() {
    const currentText = textArray[textIndex];
    
    if (isDeleting) {
      // Removing characters
      element.textContent = currentText.substring(0, charIndex - 1);
      charIndex--;
      typingDelay = deletingDelay;
    } else {
      // Adding characters
      element.textContent = currentText.substring(0, charIndex + 1);
      charIndex++;
      typingDelay = 100;
    }
    
    // Handle end of typing or deleting
    if (!isDeleting && charIndex === currentText.length) {
      // Finished typing
      typingDelay = newTextDelay;
      isDeleting = true;
    } else if (isDeleting && charIndex === 0) {
      // Finished deleting
      isDeleting = false;
      textIndex = (textIndex + 1) % textArray.length;
    }
    
    setTimeout(type, typingDelay);
  }
  
  // Start the typing animation
  setTimeout(type, newTextDelay);
}
