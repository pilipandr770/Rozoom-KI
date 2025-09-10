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
  
  // Экспортируем интерфейс для внешнего доступа
  window.chatWidget = {
    getMetadata: () => metadata,
    setMetadata: (newMetadata) => {
      metadata = newMetadata;
      localStorage.setItem('rozoom_metadata', JSON.stringify(metadata));
    },
    restartChat: () => {
      // Clear chat history, but keep metadata like language
      conversationHistory = [];
      localStorage.removeItem('rozoom_history');
      
      // Clear the UI messages
      const messagesEl = document.getElementById('chat-messages');
      messagesEl.innerHTML = '';
      
      // Start fresh greeter
      startGreeter();
    }
  };
  
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
  function appendMessage(text, cls = 'bot', interactive = null) {
    const div = document.createElement('div');
    // Add high-contrast class to improve readability for bot messages
    div.className = cls === 'bot' ? 'chat-msg ' + cls + ' high-contrast' : 'chat-msg ' + cls;
    
    // Add agent-specific class if available in metadata
    if (cls === 'bot' && metadata.current_agent) {
      div.classList.add(metadata.current_agent);
    }
    
    // Handle markdown-like formatting
    const formattedText = text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\*(.*?)\*/g, '<em>$1</em>')
      .replace(/`(.*?)`/g, '<code>$1</code>')
      .replace(/\n/g, '<br>');
    
    div.innerHTML = formattedText;
    
    // Добавляем проверку контраста текста для сообщений бота
    if (cls === 'bot') {
      // Добавляем дополнительный класс для улучшения читаемости
      div.classList.add('high-contrast');
      
      // Добавляем индикатор текущего агента (только для первого сообщения после переключения)
      if (interactive && metadata.agent_transition) {
        const agentIndicator = document.createElement('span');
        agentIndicator.className = 'chat-agent-indicator';
        agentIndicator.textContent = metadata.current_agent || 'assistant';
        div.appendChild(agentIndicator);
      }
    }
    
    messagesEl.appendChild(div);
    messagesEl.scrollTop = messagesEl.scrollHeight;
    
    // Add interactive elements if provided
    if (interactive) {
      // Add buttons if available
      if (interactive.buttons && interactive.buttons.length) {
        const buttonContainer = document.createElement('div');
        buttonContainer.className = 'chat-options';
        
        interactive.buttons.forEach(btn => {
          const button = document.createElement('button');
          
          // Add icon if available
          if (btn.icon) {
            button.innerHTML = `<i class="fas fa-${btn.icon}"></i> `;
          }
          
          button.innerHTML += btn.label;
          
          // Add tooltip if available
          if (btn.description) {
            button.title = btn.description;
          }
          
          button.onclick = () => {
            // Add selection to chat
            appendMessage(`${btn.label}`, 'user');
            
            // Update metadata with selection and transition info
            metadata.selected_agent = btn.key;
            metadata.agent_transition = true;
            
            // Показываем индикатор переключения на нового агента
            const transferIndicator = document.createElement('div');
            transferIndicator.className = 'chat-transfer-indicator';
            transferIndicator.innerHTML = `<div class="transfer-animation"></div><span>Переключение на специалиста...</span>`;
            messagesEl.appendChild(transferIndicator);
            messagesEl.scrollTop = messagesEl.scrollHeight;
            
            // Небольшая задержка для улучшения пользовательского опыта
            setTimeout(() => {
              // Удаляем индикатор переключения
              transferIndicator.remove();
              
              // Send "silent" message to switch agent
              postChat(btn.label);
            }, 1200);
          };
          
          buttonContainer.appendChild(button);
        });
        
        messagesEl.appendChild(buttonContainer);
      }
      
      // Всегда разрешаем пользователю вводить текст, но показываем подсказку о доступных опциях
      if (interactive.requires_input !== undefined) {
        // Никогда не блокируем поле ввода полностью
        input.disabled = false;
        send.disabled = false;
        
        if (!interactive.requires_input) {
          input.placeholder = "Вы можете выбрать опцию выше или задать свой вопрос...";
        } else {
          input.placeholder = "Введите сообщение...";
        }
      }
      
      // Add restart button as a normal option
      if (interactive.show_restart) {
        if (!document.querySelector('.restart-button')) { // Добавляем только если еще нет
          const buttonContainer = document.createElement('div');
          buttonContainer.className = 'chat-options';
          
          const restartBtn = document.createElement('button');
          restartBtn.className = 'restart-button';
          restartBtn.innerHTML = '<i class="fas fa-redo"></i> Начать сначала';
          restartBtn.onclick = () => {
            // Clear chat history and metadata
            conversationHistory = [];
            metadata = {};
            localStorage.removeItem('rozoom_history');
            localStorage.removeItem('rozoom_metadata');
            
            // Clear the UI
            messagesEl.innerHTML = '';
            
            // Start fresh
            startGreeter();
          };
          
          buttonContainer.appendChild(restartBtn);
          messagesEl.appendChild(buttonContainer);
        }
      }
    }
    
    // Save to history
    conversationHistory.push({ text, type: cls, interactive });
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
      // Добавляем текущий URL страницы в метаданные
      metadata.page = window.location.pathname;
      
      // Для отладки выведем метаданные перед отправкой запроса
      console.log("Sending chat with metadata:", JSON.stringify(metadata));
      
      const resp = await fetch('/api/chat', {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message, metadata})
      });
      
      if (!resp.ok) {
        // Если произошла ошибка 400 или 302 (перенаправление из-за CSRF), 
        // перезагрузим страницу чтобы обновить CSRF токен
        if (resp.status === 400 || resp.status === 302) {
          console.log('Ошибка CSRF, пробуем заново загрузить чат...');
          // Не перезагружаем полностью, просто инициализируем чат заново через 1 секунду
          setTimeout(() => {
            // Очистим сообщения и начнем заново
            messagesEl.innerHTML = '';
            startGreeter();
          }, 1000);
          return { error: 'Проблема безопасности, перезагружаем чат...' };
        }
        throw new Error(`Server responded with ${resp.status}`);
      }
      
      const result = await resp.json();
      
      // Update conversation ID if provided
      if (result.conversation_id) {
        metadata.conversation_id = result.conversation_id;
      }
      
      return result;
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
      
      const responseText = r.answer || 'Здравствуйте! Чем я могу вам помочь?';
      
      // Check if we have interactive elements
      if (r.interactive) {
        appendMessage(responseText, 'bot', r.interactive);
      } else {
        appendMessage(responseText, 'bot');
        
        // Fallback for older API format
        if (r.options && r.options.length) {
          const opts = document.createElement('div');
          opts.className = 'chat-options';
          
          r.options.forEach(o => {
            const btn = document.createElement('button');
            btn.innerHTML = `<i class="fas fa-${o.icon || 'comment'}"></i> ${o.label}`;
            
            btn.onclick = () => {
              metadata.selected_domain = o.key;
              appendMessage(`Мне нужна помощь с ${o.label}`, 'user');
              
              const loadingIndicator = showTypingIndicator();
              
              // Short timeout to simulate agent switching
              setTimeout(() => {
                loadingIndicator.remove();
                appendMessage(`Отлично! Я специализируюсь на ${o.label}. Как я могу вам помочь?`, 'bot');
                saveSession();
              }, 800);
            };
            
            opts.appendChild(btn);
          });
          
          messagesEl.appendChild(opts);
        }
      }
    } catch (error) {
      console.error('Error starting chat:', error);
      appendMessage('Извините, возникла проблема с подключением. Пожалуйста, попробуйте позже.', 'bot');
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
        appendMessage(`Ошибка: ${r.error}`, 'bot');
      } else {
        // Сохраняем conversation_id, если он был получен от сервера
        if (r.conversation_id) {
          metadata.conversation_id = r.conversation_id;
          // Сохраняем метаданные в localStorage
          localStorage.setItem('rozoom_metadata', JSON.stringify(metadata));
        }
        
        // Check if we have interactive elements
        if (r.interactive) {
          appendMessage(r.answer, 'bot', r.interactive);
          
          // Store agent information in metadata
          if (r.agent) {
            metadata.current_agent = r.agent;
            console.log("Updated current agent to:", r.agent);
          }
          
          // Store any additional metadata
          if (r.interactive.meta) {
            console.log("Received additional metadata:", JSON.stringify(r.interactive.meta));
            Object.assign(metadata, r.interactive.meta);
          }
        } else {
          appendMessage(r.answer || JSON.stringify(r), 'bot');
        }
        
        // Сохраняем обновленные метаданные
        saveSession();
      }
    } catch (error) {
      console.error('Error sending message:', error);
      indicator.remove();
      appendMessage('Извините, что-то пошло не так. Пожалуйста, попробуйте еще раз.', 'bot');
    } finally {
      // Всегда активируем поле ввода для обеспечения возможности продолжать общение
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
