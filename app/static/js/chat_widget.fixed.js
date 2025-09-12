/**
 * Enhanced Rozoom Chat Widget
 * Features:
 * - Animated loading indicators
 * - Session persistence with stable user_id
 * - UI enhancements
 * - Input handling & validation
 * - Keyboard support (Enter to send)
 * - Fixed positioning during scroll
 * - Responsive design
 * - Direct OpenAI API integration
 */
(() => {
  // Проверка существования элементов
  if (!document.getElementById('chat-widget')) {
    console.error('Элемент #chat-widget не найден! Виджет чата не может быть инициализирован.');
    return; // Прекращаем выполнение скрипта
  }

  // DOM Elements
  const toggle = document.getElementById('chat-toggle');
  const closeBtn = document.getElementById('chat-close');
  const windowEl = document.getElementById('chat-window');
  const messagesEl = document.getElementById('chat-messages');
  const input = document.getElementById('chat-input');
  const send = document.getElementById('chat-send');
  const chatWidget = document.getElementById('chat-widget');
  
  // Проверка всех необходимых элементов
  if (!toggle || !closeBtn || !windowEl || !messagesEl || !input || !send) {
    console.error('Не все необходимые элементы чата найдены! Виджет может работать некорректно.');
    console.log({toggle, closeBtn, windowEl, messagesEl, input, send});
  }

  // === Стабільний user_id у localStorage ===
  function getStableUserId() {
    const KEY = 'rozoom_user_id';
    let uid = localStorage.getItem(KEY);
    if (!uid) {
      uid = crypto.randomUUID ? crypto.randomUUID() : 
            ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
              (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
            );
      localStorage.setItem(KEY, uid);
    }
    return uid;
  }

  // === Мова користувача з браузера ===
  function detectLanguage() {
    const lang = (navigator.language || navigator.userLanguage || 'uk').toLowerCase();
    if (lang.includes('uk')) return 'uk';
    if (lang.includes('ru')) return 'ru';
    if (lang.includes('de')) return 'de';
    return 'en';
  }

  // State management with enhanced metadata
  let metadata = JSON.parse(localStorage.getItem('rozoom_metadata') || '{}');
  metadata.language = metadata.language || detectLanguage();
  metadata.user_id = metadata.user_id || getStableUserId();
  metadata.suppress_greeting = false;
  
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
    },
    // New method for switching between assistants
    switchAssistant: (agentKey) => {
      if (agentKey && ['greeter', 'spec', 'pm'].includes(agentKey)) {
        metadata.selected_agent = agentKey;
        metadata.suppress_greeting = true; // щоб асистент не вітався, а продовжив по суті
        localStorage.setItem('rozoom_metadata', JSON.stringify(metadata));
        // Пошлемо "тихий" запит без тексту — асистент підхопить контекст і продовжить
        postChat('');
      } else {
        console.error('Invalid assistant key:', agentKey);
      }
    }
  };
  
  // For backwards compatibility
  window.chatWidgetSwitch = function(agentKey) {
    window.chatWidget.switchAssistant(agentKey);
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
          
          // Fix issues with missing or undefined labels for Ukrainian language
          const isUkrainian = metadata.language === "uk";
          
          // Handle migration from text to label property
          if (!btn.label && btn.text) {
            btn.label = btn.text;
          }
          
          // Handle undefined labels in Ukrainian
          if ((btn.label === "undefined" || !btn.label) && isUkrainian) {
            console.log("Found undefined button label, attempting translation for key:", btn.key);
            
            // Map of Ukrainian translations for specialist buttons
            const ukLabels = {
              "greeter": "Початок діалогу",
              "design": "Дизайн",
              "development": "Розробка",
              "marketing": "Маркетинг",
              "portfolio": "Портфоліо",
              "requirements": "Технічне завдання",
              "quiz": "Калькулятор",
              "consultation": "Консультація"
            };
            
            // Try to get label from map or fall back to capitalized key
            btn.label = ukLabels[btn.key] || btn.key.charAt(0).toUpperCase() + btn.key.slice(1);
          }
          
          button.append(btn.label || btn.key || 'Опція');
          
          if (btn.action) {
            // Direct click handler
            button.addEventListener('click', (e) => {
              e.preventDefault();
              if (btn.action === 'select-specialist') {
                metadata.selected_agent = btn.key;
                localStorage.setItem('rozoom_metadata', JSON.stringify(metadata));
              }
              input.value = btn.action === 'text' ? btn.text : btn.key || btn.label;
              handleSendMessage();
            });
          } else {
            // Default action - send button text as message
            button.addEventListener('click', (e) => {
              e.preventDefault();
              input.value = btn.text || btn.key || btn.label;
              handleSendMessage();
            });
          }
          
          buttonContainer.appendChild(button);
        });
        
        messagesEl.appendChild(buttonContainer);
        messagesEl.scrollTop = messagesEl.scrollHeight;
      }
    }
    
    // Record in conversation history
    conversationHistory.push({
      text,
      cls,
      timestamp: new Date().toISOString()
    });
    
    // Save to localStorage (limited to last 10 messages)
    localStorage.setItem('rozoom_history', JSON.stringify(conversationHistory.slice(-10)));
    
    return div;
  }
  
  /**
   * Restores the chat session from localStorage if available
   * Returns true if session was restored, false otherwise
   */
  function restoreChatSession() {
    if (conversationHistory && conversationHistory.length > 0) {
      // Limit to last 5 messages for better performance
      const recentMessages = conversationHistory.slice(-5);
      
      recentMessages.forEach(msg => {
        appendMessage(msg.text, msg.cls);
      });
      
      return true;
    }
    return false;
  }

  /**
   * Shows a typing indicator while waiting for response
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
      
      // Show typing indicator
      const thinking = showTypingIndicator();
      
      const resp = await fetch('/api/chat', {
        method: 'POST', 
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          message, 
          metadata: {
            ...metadata,
            // Ensure these keys are always present for Assistants API
            user_id: metadata.user_id || getStableUserId(),
            language: metadata.language || detectLanguage(),
            suppress_greeting: !!metadata.suppress_greeting
          }
        })
      });
      
      // Remove typing indicator
      if (thinking) thinking.remove();
      
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
      
      if (result.answer) {
        appendMessage(result.answer, 'bot', result.interactive);
      } else {
        appendMessage('Вибачте, сталася помилка. Спробуйте ще раз.', 'bot');
      }

      // Reset suppress_greeting after one request
      metadata.suppress_greeting = false;
      localStorage.setItem('rozoom_metadata', JSON.stringify(metadata));
      
      return result;
    } catch (error) {
      console.error('Chat API error:', error);
      appendMessage('Проблема зі з'єднанням. Спробуйте пізніше.', 'bot');
      return { error: error.message || 'Failed to connect to chat service' };
    }
  }

  /**
   * Initializes the chat with a greeter message
   */
  function startGreeter() {
    // Use active agent from metadata or default to greeter
    const agent = metadata.active_agent || 'greeter';
    
    // Show typing indicator first
    const thinking = showTypingIndicator();
    
    // Clear greeting suppression flag
    metadata.suppress_greeting = false;
    localStorage.setItem('rozoom_metadata', JSON.stringify(metadata));
    
    // Make the API call with empty message to trigger greeting
    setTimeout(async () => {
      thinking && thinking.remove();
      await postChat('');
    }, 700);  // Short delay for visual effect
  }

  /**
   * Handle sending a message to the chat
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
    
    try {
      // Send to API
      await postChat(txt);
      
    } catch (error) {
      console.error('Error sending message:', error);
      appendMessage('Вибачте, сталася помилка. Спробуйте ще раз.', 'bot');
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
      toggle.classList.remove('bounce');
    } else {
      // Remove active class when chat is closed
      toggle.classList.remove('active');
    }
  });

  closeBtn.addEventListener('click', () => {
    windowEl.classList.add('hidden');
    toggle.classList.remove('active');
  });

  // Send message on button click
  send.addEventListener('click', handleSendMessage);

  // Send message on Enter key (but allow Shift+Enter for new line)
  input.addEventListener('keydown', async (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      await handleSendMessage();
    }
  });

})();
