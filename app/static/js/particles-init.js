// Initialize particles.js
document.addEventListener('DOMContentLoaded', function() {
  // Check if particles container exists
  if(document.getElementById('particles-js')) {
    // Load particles.js config
    particlesJS.load('particles-js', '/static/js/particles-config.json', function() {
      console.log('particles.js loaded - callback');
    });
  }
});
