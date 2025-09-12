/**
 * Ultimate Direct Fix for Chat Widget
 * This script completely bypasses the original chat implementation
 * and provides a simple, reliable solution for sending messages.
 */
document.addEventListener('DOMContentLoaded', function() {
  console.log('Ultimate Chat Fix: Initializing...');
  
  // Function to apply once DOM is loaded
  function applyDirectFix() {
    // Get required elements
    const input = document.getElementById('chat-input');
    const send = document.getElementById('chat-send');
    const messages = document.getElementById('chat-messages');
    const toggle = document.getElementById('chat-toggle');
    const closeBtn = document.getElementById('chat-close');
    const chatWindow = document.getElementById('chat-window');
    
    if (!input || !send || !messages) {
      console.error('Ultimate Chat Fix: Required elements not found!');
      // Retry after a delay
      setTimeout(applyDirectFix, 500);
      return;
    }
    
    console.log('Ultimate Chat Fix: Elements found, applying direct solution...');
    
    // Store conversation ID in localStorage
    let conversationId = localStorage.getItem('chat_conversation_id');
    if (!conversationId) {
      conversationId = generateUUID();
      localStorage.setItem('chat_conversation_id', conversationId);
    }
    
    // User ID generation/retrieval
    let userId = localStorage.getItem('rozoom_user_id');
    if (!userId) {
      userId = generateUUID();
      localStorage.setItem('rozoom_user_id', userId);
    }
    
    // Simple UUID generator
    function generateUUID() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }
    
    // Detect language
    function detectLanguage() {
      // First try the page language
      const htmlLang = document.documentElement.lang;
      if (htmlLang) {
        if (htmlLang.includes('uk')) return 'uk';
        if (htmlLang.includes('ru')) return 'ru';
        if (htmlLang.includes('de')) return 'de';
        if (htmlLang.includes('en')) return 'en';
      }
      
      // Fallback to browser language
      const lang = (navigator.language || navigator.userLanguage || 'uk').toLowerCase();
      if (lang.includes('uk') || lang === 'ua') return 'uk';
      if (lang.includes('ru')) return 'ru';
      if (lang.includes('de')) return 'de';
      if (lang.includes('en')) return 'en';
      
      // Default to Ukrainian
      return 'uk';
    }
    
    // The core send message function
    function sendMessage() {
      const text = input.value.trim();
      if (!text) return;
      
      console.log('Ultimate Chat Fix: Sending message:', text);
      
      // Display user message
      const userDiv = document.createElement('div');
      userDiv.className = 'chat-msg user';
      userDiv.textContent = text;
      messages.appendChild(userDiv);
      messages.scrollTop = messages.scrollHeight;
      
      // Clear input
      input.value = '';
      
      // Show thinking animation
      const loadingDiv = document.createElement('div');
      loadingDiv.className = 'chat-msg bot thinking';
      for (let i = 0; i < 3; i++) {
        const dot = document.createElement('div');
        dot.className = 'thinking-dot';
        loadingDiv.appendChild(dot);
      }
      messages.appendChild(loadingDiv);
      messages.scrollTop = messages.scrollHeight;
      
      // Get CSRF token if available
      let csrfToken = null;
      const tokenMeta = document.querySelector('meta[name="csrf-token"]');
      if (tokenMeta) {
        csrfToken = tokenMeta.getAttribute('content');
      }
      
      // Build request headers
      const headers = {
        'Content-Type': 'application/json'
      };
      
      // Add CSRF token if available
      if (csrfToken) {
        headers['X-CSRFToken'] = csrfToken;
      }
      
      // Prepare metadata
      const metadata = {
        language: detectLanguage(),
        page: window.location.pathname,
        user_id: userId,
        conversation_id: conversationId
      };
      
      // Send to API
      fetch('/api/chat', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({
          message: text,
          metadata: metadata
        })
      })
      .then(response => {
        // Remove loading indicator
        loadingDiv.remove();
        
        if (!response.ok) {
          throw new Error(`API response error: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        console.log('Ultimate Chat Fix: Got response:', data);
        
        if (data.answer) {
          // Display bot message
          const botDiv = document.createElement('div');
          botDiv.className = 'chat-msg bot';
          botDiv.innerHTML = data.answer.replace(/\n/g, '<br>');
          messages.appendChild(botDiv);
          messages.scrollTop = messages.scrollHeight;
        } else {
          throw new Error('No answer in response');
        }
      })
      .catch(error => {
        console.error('Ultimate Chat Fix: Error:', error);
        
        // Show error message
        const errorDiv = document.createElement('div');
        errorDiv.className = 'chat-msg bot error';
        
        // Select error message based on language
        const lang = detectLanguage();
        const errorMessages = {
          'uk': 'Помилка при надсиланні повідомлення. Спробуйте ще раз.',
          'ru': 'Ошибка при отправке сообщения. Попробуйте еще раз.',
          'de': 'Fehler beim Senden der Nachricht. Bitte versuchen Sie es erneut.',
          'en': 'Error sending message. Please try again.'
        };
        
        errorDiv.textContent = errorMessages[lang] || errorMessages['uk'];
        messages.appendChild(errorDiv);
        messages.scrollTop = messages.scrollHeight;
      });
    }
    
    // Apply event handlers
    
    // 1. Send button
    send.onclick = function(e) {
      e.preventDefault();
      e.stopPropagation();
      sendMessage();
      return false;
    };
    
    // 2. Enter key in input
    input.onkeypress = function(e) {
      if (e.key === 'Enter' || e.keyCode === 13) {
        e.preventDefault();
        e.stopPropagation();
        sendMessage();
        return false;
      }
    };
    
    // 3. Toggle button (open/close chat)
    if (toggle && chatWindow) {
      toggle.onclick = function() {
        const isHidden = chatWindow.classList.contains('hidden');
        if (isHidden) {
          chatWindow.classList.remove('hidden');
          toggle.classList.add('active');
        } else {
          chatWindow.classList.add('hidden');
          toggle.classList.remove('active');
        }
      };
    }
    
    // 4. Close button
    if (closeBtn && chatWindow) {
      closeBtn.onclick = function() {
        chatWindow.classList.add('hidden');
        if (toggle) toggle.classList.remove('active');
      };
    }
    
    console.log('Ultimate Chat Fix: Successfully applied all fixes');
  }
  
  // Apply the fix immediately, then again after a short delay to ensure it works
  applyDirectFix();
  setTimeout(applyDirectFix, 1000);
});
