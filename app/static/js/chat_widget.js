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
  // Check for essential elements right away
  if (!document.getElementById('chat-widget')) {
    console.error('Element #chat-widget not found! Chat widget initialization failed.');
    return;
  }
  
  // Make sure the DOM is fully loaded
  function initChatWidget() {
  // Production: silent init

    // DOM Elements
    const toggle = document.getElementById('chat-toggle');
    const closeBtn = document.getElementById('chat-close');
    const windowEl = document.getElementById('chat-window');
    const messagesEl = document.getElementById('chat-messages');
    const input = document.getElementById('chat-input');
    const send = document.getElementById('chat-send');
    const chatWidget = document.getElementById('chat-widget');
    
    // Make global references available for debugging and emergency fixes
    window.chatElements = {toggle, closeBtn, windowEl, messagesEl, input, send, chatWidget};
    
    // Verify that all required elements exist
    const requiredElements = {toggle, closeBtn, windowEl, messagesEl, input, send};
    const missingElements = Object.entries(requiredElements)
      .filter(([name, el]) => !el)
      .map(([name]) => name);
    
    if (missingElements.length > 0) {
      console.error(`Missing required chat elements: ${missingElements.join(', ')}`);
      console.log({toggle, closeBtn, windowEl, messagesEl, input, send});
      return; // Don't initialize if essential elements are missing
    }
    
    // Make absolutely sure the toggle button is clickable
    toggle.style.position = 'fixed';
    toggle.style.zIndex = '9999';
    toggle.style.cursor = 'pointer';
    toggle.style.pointerEvents = 'auto';
    
    // Make sure the send button is properly clickable too
    send.style.cursor = 'pointer';
    send.style.pointerEvents = 'auto';

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

  // === Мова користувача з перемикача або браузера ===
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
      toggle.style.position = 'fixed';
      toggle.style.right = window.innerWidth <= 480 ? '15px' : '30px';
      toggle.style.bottom = window.innerWidth <= 480 ? '15px' : '30px';
      toggle.style.zIndex = '9999';
      toggle.style.pointerEvents = 'auto'; // Always ensure it's clickable
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
            const ukrLabels = {
              "greeter": "Привітання",
              "consultation": "Консультація",
              "completion": "Консультація",
              "portfolio": "Портфоліо",
              "design": "Дизайн",
              "development": "Розробка",
              "marketing": "Маркетинг",
              "requirements": "Технічне завдання",
              "quiz": "Калькулятор вартості"
            };
            
            // Check if we have a translation for this key
            if (ukrLabels[btn.key]) {
              btn.label = ukrLabels[btn.key];
            } else if (btn.key && btn.key.includes("back")) {
              btn.label = "Назад";
            } else {
              // Fallback for unknown keys
              btn.label = btn.key || "Опція";
            }
          }
          
          button.innerHTML += btn.label;
          
          // Add tooltip if available
          if (btn.description) {
            const isUkrainian = metadata.language === "uk";
            
            // Handle undefined descriptions in Ukrainian
            if ((btn.description === "undefined" || !btn.description) && isUkrainian) {
              console.log("Found undefined description, attempting translation for key:", btn.key);
              
              // Map of Ukrainian translations for specialist descriptions
              const ukrDescriptions = {
                "greeter": "Повернутися до початку розмови",
                "consultation": "Консультація зі спеціалістом",
                "completion": "Отримати консультацію з питань проекту",
                "portfolio": "Перегляд портфоліо проектів",
                "design": "Питання з веб-дизайну, UI/UX та графічного дизайну",
                "development": "Питання з веб-розробки та програмування",
                "marketing": "Питання з цифрового маркетингу та SEO",
                "requirements": "Створення технічного завдання для вашого проекту",
                "quiz": "Розрахунок приблизної вартості вашого веб-сайту"
              };
              
              // Check if we have a translation for this key
              if (ukrDescriptions[btn.key]) {
                btn.description = ukrDescriptions[btn.key];
              } else if (btn.key && btn.key.includes("back")) {
                btn.description = "Повернутися назад";
              } else {
                // Fallback for unknown keys
                btn.description = btn.label || "Опція";
              }
            }
            button.title = btn.description;
          }          button.onclick = () => {
            // Add selection to chat
            appendMessage(`${btn.label}`, 'user');
            
            // Update metadata with selection and transition info
            metadata.selected_agent = btn.key;
            metadata.agent_transition = true;
            
            // Показываем индикатор переключения на нового агента
            const transferIndicator = document.createElement('div');
            transferIndicator.className = 'chat-transfer-indicator';
            const switchingText = window.translateChat ? window.translateChat('switchingToSpecialist') : 'Переключение на специалиста...';
            transferIndicator.innerHTML = `<div class="transfer-animation"></div><span>${switchingText}</span>`;
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
          // Используем локализованный плейсхолдер
          input.placeholder = window.translateChat ? window.translateChat('optionsPlaceholder') : "Вы можете выбрать опцию выше или задать свой вопрос...";
        } else {
          // Используем локализованный плейсхолдер
          input.placeholder = window.translateChat ? window.translateChat('inputPlaceholder') : "Введите сообщение...";
        }
      }
      
      // Add restart button as a normal option
      if (interactive.show_restart) {
        if (!document.querySelector('.restart-button')) { // Добавляем только если еще нет
          const buttonContainer = document.createElement('div');
          buttonContainer.className = 'chat-options';
          
          const restartBtn = document.createElement('button');
          restartBtn.className = 'restart-button';
          
          // Используем локализованный текст для кнопки
          let startOverText = 'Начать сначала';
          
          if (window.translateChat) {
            startOverText = window.translateChat('startOver');
          } else {
            // Fallback if translations aren't loaded yet
            if (metadata.language === 'en') {
              startOverText = 'Start over';
            } else if (metadata.language === 'de') {
              startOverText = 'Neustart';
            } else if (metadata.language === 'uk') {
              startOverText = 'Почати знову';
            } else if (metadata.language === 'ru') {
              startOverText = 'Начать сначала';
            }
          }
          
          restartBtn.innerHTML = '<i class="fas fa-redo"></i> ' + startOverText;
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
      
      // Always detect language from browser
      metadata.language = detectLanguage();
      
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
            // Ensure these keys are always present for API
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
        appendMessage(result.answer, 'bot');
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
   * Initialize chat with greeting message
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
    
  //
    
    // Clear input and disable while processing
    input.value = '';
    input.disabled = true;
    send.disabled = true;
    
    // Show user message
    appendMessage(txt, 'user');
    
    try {
      // Send to API
  const result = await postChat(txt);
      
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
  
  // Make sure global function is available 
  window.handleSendMessage = handleSendMessage;

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
  
  // Also handle keydown for better browser support
  input.addEventListener('keydown', (e) => {
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
  
  // Export the handleSendMessage function globally for emergency usage
  window.handleSendMessage = handleSendMessage;
})();
