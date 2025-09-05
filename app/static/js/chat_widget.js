/**
 * Enhanced Rozoom Chat Widget
 * Features:
 * - Animated loading indicators
 * - Session persistence
 * - UI enhancements
 * - Input handling & validation
 * - Keyboard support (Enter to send)
 * - Fixed positioning during scroll
 * - Responsive design
 */
(() => {
  // DOM Elements
  const toggle = document.getElementById('chat-toggle');
  const closeBtn = document.getElementById('chat-close');
  const windowEl = document.getElementById('chat-window');
  const messagesEl = document.getElementById('chat-messages');
  const input = document.getElementById('chat-input');
  const send = document.getElementById('chat-send');
  const chatWidget = document.getElementById('chat-widget');

  // State management
  let metadata = {};
  let conversationHistory = [];
  
  // Ensure the chat widget is always in the bottom right corner
  function ensureFixedPosition() {
    // Refresh the position to ensure it's always in the bottom right
    toggle.style.position = 'fixed';
    toggle.style.right = window.innerWidth <= 480 ? '15px' : '30px';
    toggle.style.bottom = window.innerWidth <= 480 ? '15px' : '30px';
    toggle.style.zIndex = '9999';
  }
  
  // Run on load and resize
  ensureFixedPosition();
  window.addEventListener('resize', ensureFixedPosition);
  window.addEventListener('scroll', ensureFixedPosition);
  
  // Check for saved session
  try {
    const savedMetadata = localStorage.getItem('rozoom_metadata');
    const savedHistory = localStorage.getItem('rozoom_history');
    
    if (savedMetadata) {
      metadata = JSON.parse(savedMetadata);
    }
    
    if (savedHistory) {
      conversationHistory = JSON.parse(savedHistory);
    }
  } catch (e) {
    console.error('Error loading saved chat session:', e);
  }

  /**
   * Creates and appends a message to the chat window
   */
  function appendMessage(text, cls = 'bot') {
    const div = document.createElement('div');
    div.className = 'chat-msg ' + cls;
    
    // Handle markdown-like formatting
    const formattedText = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br>');
    
    div.innerHTML = formattedText;
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    
    // Save to history
    conversationHistory.push({ text, type: cls });
    saveSession();
    
    return div;
  }

  /**
   * Shows the typing indicator when waiting for bot response
   */
  function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'chat-msg bot thinking';
    
    for (let i = 0; i < 3; i++) {
      const dot = document.createElement('div');
      dot.className = 'thinking-dot';
      indicator.appendChild(dot);
    }
    
    messagesEl.appendChild(indicator);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    return indicator;
  }

  /**
   * Sends message to backend API
   */
  async function postChat(message) {
    try {
      const resp = await fetch('/api/chat', {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message, metadata})
      });
      
      if (!resp.ok) {
        throw new Error(`Server responded with ${resp.status}`);
      }
      
      return resp.json();
    } catch (error) {
      console.error('Chat API error:', error);
      return { error: error.message || 'Failed to connect to chat service' };
    }
  }

  /**
   * Initialize chat with greeting message
   */
  async function startGreeter() {
    const indicator = showTypingIndicator();
    
    try {
      const r = await postChat('hello');
      // Remove typing indicator
      indicator.remove();
      
      const responseText = r.message || r.answer || 'Hello! How can I assist you today?';
      appendMessage(responseText, 'bot');
      
      // Show options if available
      if (r.options && r.options.length) {
        const opts = document.createElement('div');
        opts.className = 'chat-options';
        
        r.options.forEach(o => {
          const btn = document.createElement('button');
          btn.innerHTML = `<i class="fas fa-${o.icon || 'comment'}"></i> ${o.label}`;
          
          btn.onclick = () => {
            metadata.selected_domain = o.key;
            appendMessage(`I'd like to discuss ${o.label}`, 'user');
            
            const loadingIndicator = showTypingIndicator();
            
            // Short timeout to simulate agent switching
            setTimeout(() => {
              loadingIndicator.remove();
              appendMessage(`Great! I'm now in ${o.label} mode and ready to assist you. How can I help?`, 'bot');
              saveSession();
            }, 800);
          };
          
          opts.appendChild(btn);
        });
        
        messagesEl.appendChild(opts);
      }
    } catch (error) {
      console.error('Error starting chat:', error);
      appendMessage('Sorry, I had trouble connecting. Please try again later.', 'bot');
    }
  }

  /**
   * Saves chat state to localStorage
   */
  function saveSession() {
    try {
      if (conversationHistory.length) {
        localStorage.setItem('rozoom_history', JSON.stringify(conversationHistory.slice(-20)));
        localStorage.setItem('rozoom_metadata', JSON.stringify(metadata));
      }
    } catch (e) {
      console.warn('Could not save chat session:', e);
    }
  }

  /**
   * Restores previous chat session
   */
  function restoreChatSession() {
    // Clear the current messages display
    messagesEl.innerHTML = '';
    
    // Only restore if we have history
    if (conversationHistory.length > 0) {
      conversationHistory.forEach(msg => {
        appendMessage(msg.text, msg.type);
      });
      return true;
    }
    
    return false;
  }

  /**
   * Handle sending user message
   */
  async function handleSendMessage() {
    const txt = input.value.trim();
    
    if (!txt) return;
    
    // Clear input and disable while processing
    input.value = '';
    input.disabled = true;
    send.disabled = true;
    
    // Show user message
    appendMessage(txt, 'user');
    
    // Show typing indicator
    const indicator = showTypingIndicator();
    
    try {
      // Send to API
      const r = await postChat(txt);
      
      // Remove indicator
      indicator.remove();
      
      // Show response
      if (r.error) {
        appendMessage(`Error: ${r.error}`, 'bot');
      } else {
        appendMessage(r.answer || JSON.stringify(r), 'bot');
      }
    } catch (error) {
      console.error('Error sending message:', error);
      indicator.remove();
      appendMessage('Sorry, something went wrong. Please try again.', 'bot');
    } finally {
      // Re-enable input
      input.disabled = false;
      send.disabled = false;
      input.focus();
    }
  }

  // Event Listeners
  toggle.addEventListener('click', () => {
    windowEl.classList.toggle('hidden');
    
    if (!windowEl.classList.contains('hidden')) {
      // Add active class to toggle button when chat is open
      toggle.classList.add('active');
      
      // Initialize chat if it's empty
      if (messagesEl.children.length === 0) {
        const hasRestoredSession = restoreChatSession();
        
        if (!hasRestoredSession) {
          startGreeter();
        }
      }
      
      // Focus input field
      setTimeout(() => input.focus(), 300);
      
      // Stop bounce animation
      toggle.style.animation = 'none';
    } else {
      toggle.classList.remove('active');
      
      // Restore bounce animation after a delay
      setTimeout(() => {
        toggle.style.animation = '';
      }, 1000);
    }
  });
  
  // Close button
  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      windowEl.classList.add('hidden');
      toggle.classList.remove('active');
      
      // Restore bounce animation after a delay
      setTimeout(() => {
        toggle.style.animation = '';
      }, 1000);
    });
  }

  // Send button
  send.addEventListener('click', handleSendMessage);
  
  // Enter key to send
  input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleSendMessage();
    }
  });
  
  // Handle scroll events to keep chat in place
  window.addEventListener('scroll', () => {
    if (window.innerWidth <= 480) {
      const scrollY = window.scrollY;
      const windowHeight = window.innerHeight;
      const docHeight = document.documentElement.scrollHeight;
      
      // Adjust position when near bottom of page
      if (docHeight - (scrollY + windowHeight) < 100) {
        chatWidget.style.bottom = '80px';
      } else {
        chatWidget.style.bottom = '15px';
      }
    }
  });
  
  // Store user session on unload
  window.addEventListener('beforeunload', saveSession);
})();
