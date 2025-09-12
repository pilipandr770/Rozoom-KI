/**
 * Chat Send Fix Script
 * This script fixes issues with sending messages in the chat widget
 */
(function() {
  console.log('Applying chat send fix...');
  
  // Wait for DOM to be fully loaded
  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
      // Get the chat elements
      const input = document.getElementById('chat-input');
      const send = document.getElementById('chat-send');
      const messagesEl = document.getElementById('chat-messages');
      
      if (!input || !send || !messagesEl) {
        console.error('Chat widget elements not found!', { input, send, messagesEl });
        return;
      }
      
      console.log('Found chat widget elements for send fix');
      
      // Create a new improved send function
      async function improvedSendMessage() {
        const txt = input.value.trim();
        
        if (!txt) return;
        
        console.log('Send button clicked! Text:', txt);
        
        // Clear input and disable while processing
        input.value = '';
        input.disabled = true;
        send.disabled = true;
        
        // Show user message
        if (typeof appendMessage === 'function') {
          appendMessage(txt, 'user');
        } else {
          // Fallback if appendMessage is not available
          const userDiv = document.createElement('div');
          userDiv.className = 'chat-msg user';
          userDiv.textContent = txt;
          messagesEl.appendChild(userDiv);
          messagesEl.scrollTop = messagesEl.scrollHeight;
        }
        
        try {
          // Show typing indicator
          const indicator = document.createElement('div');
          indicator.className = 'chat-msg bot thinking';
          
          for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'thinking-dot';
            indicator.appendChild(dot);
          }
          
          messagesEl.appendChild(indicator);
          messagesEl.scrollTop = messagesEl.scrollHeight;
          
          // Get metadata from window.chatWidget if available
          let metadata = {};
          if (window.chatWidget && window.chatWidget.getMetadata) {
            metadata = window.chatWidget.getMetadata();
          }
          
          // Improved language detection
          function detectLanguage() {
            // Спочатку перевіряємо мову сторінки через тег html
            const htmlLang = document.documentElement.lang;
            if (htmlLang) {
              const pageLang = htmlLang.toLowerCase();
              if (pageLang.includes('uk')) return 'uk';
              if (pageLang.includes('ru')) return 'ru';
              if (pageLang.includes('de')) return 'de';
              if (pageLang.includes('en')) return 'en';
            }
            
            // Перевіряємо активну кнопку мови
            const activeBtn = document.querySelector('.lang-button.active');
            if (activeBtn) {
              const btnLang = activeBtn.getAttribute('data-lang');
              if (btnLang) return btnLang.toLowerCase();
            }
            
            // Fallback на мову браузера
            const lang = (navigator.language || navigator.userLanguage || 'uk').toLowerCase();
            if (lang.includes('uk') || lang === 'ua') return 'uk';
            if (lang.includes('ru')) return 'ru';
            if (lang.includes('de')) return 'de';
            if (lang.includes('en')) return 'en';
            
            // Дефолт - українська
            return 'uk';
          }
          
          // Ensure we have the basic metadata
          metadata = {
            ...metadata,
            language: detectLanguage(),
            page: window.location.pathname,
            user_id: metadata.user_id || localStorage.getItem('rozoom_user_id') || 'anonymous-user'
          };
          
          console.log('Sending chat with metadata:', metadata);
          
          // Send to API
          const resp = await fetch('/api/chat', {
            method: 'POST', 
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
              message: txt, 
              metadata: metadata
            })
          });
          
          // Remove typing indicator
          if (indicator) indicator.remove();
          
          if (!resp.ok) {
            throw new Error(`Server responded with ${resp.status}`);
          }
          
          const result = await resp.json();
          
          if (result.answer) {
            // Create bot message element
            const botDiv = document.createElement('div');
            botDiv.className = 'chat-msg bot high-contrast';
            
            // Format the answer with basic markdown support
            const formattedText = result.answer
              .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
              .replace(/\*(.*?)\*/g, '<em>$1</em>')
              .replace(/`(.*?)`/g, '<code>$1</code>')
              .replace(/\n/g, '<br>');
            
            botDiv.innerHTML = formattedText;
            messagesEl.appendChild(botDiv);
            messagesEl.scrollTop = messagesEl.scrollHeight;
          } else {
            throw new Error('No answer in response');
          }
          
        } catch (error) {
          console.error('Error sending message:', error);
          
          // Create error message
          const errorDiv = document.createElement('div');
          errorDiv.className = 'chat-msg bot error';
          errorDiv.textContent = 'Вибачте, сталася помилка. Спробуйте ще раз.';
          messagesEl.appendChild(errorDiv);
          messagesEl.scrollTop = messagesEl.scrollHeight;
        } finally {
          // Always re-enable the input field
          input.disabled = false;
          send.disabled = false;
          input.focus();
        }
      }
      
      // Use direct event assignment instead of addEventListener
      send.onclick = function(event) {
        console.log('Send button clicked (direct)!');
        event.preventDefault();
        improvedSendMessage();
      };
      
      // Fix Enter key press with direct assignment
      input.onkeypress = function(event) {
        console.log('Key pressed in input (direct):', event.key);
        if (event.key === 'Enter') {
          console.log('Enter key pressed (direct)!');
          event.preventDefault();
          improvedSendMessage();
        }
      };
      
      // Also add keydown handler for better cross-browser support
      input.onkeydown = function(event) {
        if (event.key === 'Enter') {
          console.log('Enter keydown detected (direct)!');
          event.preventDefault();
          improvedSendMessage();
        }
      };
      
      // Make functions available globally
      window.improvedSendMessage = improvedSendMessage;
      
      console.log('Chat send fix applied successfully');
    }, 500); // Short delay to ensure DOM is ready
  });
})();
