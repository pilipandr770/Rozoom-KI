/**
 * EMERGENCY FIX for chat widget send button and Enter key
 * This script forces new event handlers for the chat widget
 */
(function() {
  console.log('EMERGENCY SEND FIX: Initializing...');
  
  // Function to apply fix
  function applySendButtonFix() {
    // Try to get chat elements
    const input = document.getElementById('chat-input');
    const send = document.getElementById('chat-send');
    
    if (!input || !send) {
      console.error('EMERGENCY SEND FIX: Chat elements not found!');
      // Try again in 1 second
      setTimeout(applySendButtonFix, 1000);
      return;
    }
    
    console.log('EMERGENCY SEND FIX: Chat elements found, applying fixes...');
    
    // Define a simple send function that will work regardless of other scripts
    function emergencySend() {
      const message = input.value.trim();
      if (!message) return;
      
      console.log('EMERGENCY SEND FIX: Sending message:', message);
      
      // Show user message in chat
      const messagesEl = document.getElementById('chat-messages');
      if (messagesEl) {
        const userMsg = document.createElement('div');
        userMsg.className = 'chat-msg user';
        userMsg.textContent = message;
        messagesEl.appendChild(userMsg);
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }
      
      // Clear input
      input.value = '';
      
      // Determine user's language
      let lang = 'uk'; // default
      try {
        if (document.documentElement.lang) {
          lang = document.documentElement.lang.substring(0, 2).toLowerCase();
        } else if (navigator.language) {
          lang = navigator.language.substring(0, 2).toLowerCase();
        }
      } catch(e) {
        console.error('Error detecting language:', e);
      }
      
      // Get user_id from localStorage
      let userId = 'emergency-user';
      try {
        userId = localStorage.getItem('rozoom_user_id') || 
                 (JSON.parse(localStorage.getItem('rozoom_metadata') || '{}').user_id) || 
                 'emergency-user-' + Math.floor(Math.random() * 10000);
      } catch(e) {
        console.error('Error getting user_id:', e);
      }
      
      // Directly call API
      fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          message: message,
          metadata: {
            language: lang,
            user_id: userId,
            page: window.location.pathname
          }
        })
      })
      .then(response => {
        if (!response.ok) throw new Error('Network response was not ok');
        return response.json();
      })
      .then(data => {
        // Display bot response
        if (data.answer && messagesEl) {
          const botMsg = document.createElement('div');
          botMsg.className = 'chat-msg bot';
          botMsg.innerHTML = data.answer.replace(/\n/g, '<br>');
          messagesEl.appendChild(botMsg);
          messagesEl.scrollTop = messagesEl.scrollHeight;
        }
      })
      .catch(error => {
        console.error('Error in chat API call:', error);
        // Show error message
        if (messagesEl) {
          const errorMsg = document.createElement('div');
          errorMsg.className = 'chat-msg bot error';
          errorMsg.textContent = 'Помилка з'єднання. Будь ласка, спробуйте пізніше.';
          messagesEl.appendChild(errorMsg);
          messagesEl.scrollTop = messagesEl.scrollHeight;
        }
      });
    }
    
    // Store original functions for debugging
    window._originalHandleSendMessage = window.handleSendMessage;
    window._originalImprovedSendMessage = window.improvedSendMessage;
    
    // Force direct event listeners
    send.onclick = emergencySend;
    input.onkeypress = function(e) {
      if (e.key === 'Enter' || e.keyCode === 13) {
        e.preventDefault();
        emergencySend();
      }
    };
    
    // Make our function available globally
    window.emergencySend = emergencySend;
    
    // Override previous functions
    window.handleSendMessage = emergencySend;
    window.improvedSendMessage = emergencySend;
    
    console.log('EMERGENCY SEND FIX: Applied successfully!');
  }
  
  // Wait for DOM or apply immediately if already loaded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      setTimeout(applySendButtonFix, 1000);
    });
  } else {
    setTimeout(applySendButtonFix, 1000);
  }
})();
