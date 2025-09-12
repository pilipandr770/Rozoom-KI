/**
 * Chat Widget Fix Script
 * This script fixes issues with the chat toggle button not responding to clicks
 */
(function() {
  console.log('Applying chat widget fix...');
  
  // Wait for DOM to be fully loaded
  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
      // Get the toggle button and window element
      const toggle = document.getElementById('chat-toggle');
      const windowEl = document.getElementById('chat-window');
      
      if (!toggle || !windowEl) {
        console.error('Chat widget elements not found!', { toggle, windowEl });
        return;
      }
      
      console.log('Found chat widget elements:', { 
        toggle: toggle, 
        window: windowEl,
        toggleDisplay: window.getComputedStyle(toggle).display,
        toggleZIndex: window.getComputedStyle(toggle).zIndex,
        togglePointerEvents: window.getComputedStyle(toggle).pointerEvents
      });
      
      // Ensure the toggle is clickable
      toggle.style.position = 'fixed';
      toggle.style.zIndex = '10000'; // Higher than anything else
      toggle.style.cursor = 'pointer';
      toggle.style.pointerEvents = 'auto';
      
      // Remove and re-add the click event listener to ensure it works
      const newToggle = toggle.cloneNode(true);
      toggle.parentNode.replaceChild(newToggle, toggle);
      
      // Add the click event listener to the new toggle
      newToggle.addEventListener('click', function(event) {
        console.log('Chat toggle clicked!');
        windowEl.classList.toggle('hidden');
        
        if (!windowEl.classList.contains('hidden')) {
          newToggle.classList.add('active');
          
          // Focus input field
          const input = document.getElementById('chat-input');
          if (input) setTimeout(() => input.focus(), 300);
          
          // Stop bounce animation
          newToggle.style.animation = 'none';
        } else {
          newToggle.classList.remove('active');
          
          // Restore bounce animation after a delay
          setTimeout(() => {
            newToggle.style.animation = '';
          }, 1000);
        }
        
        // Prevent any default behavior
        event.preventDefault();
        event.stopPropagation();
      });
      
      console.log('Chat widget fix applied successfully');
    }, 500); // Short delay to ensure DOM is ready
  });
})();
