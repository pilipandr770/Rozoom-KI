// Minimal production chat widget (clean, no debug hints)
(function() {
  function init() {
    var input = document.getElementById('chat-input');
    var send = document.getElementById('chat-send');
    var messages = document.getElementById('chat-messages');
    var toggle = document.getElementById('chat-toggle');
    var closeBtn = document.getElementById('chat-close');
    var chatWindow = document.getElementById('chat-window');
    var btnGreeter = document.getElementById('agent-btn-greeter');
    var btnSpec = document.getElementById('agent-btn-spec');
    var btnPm = document.getElementById('agent-btn-pm');
    if (!input || !send || !messages || !toggle || !chatWindow) return;

    // IDs
    var conversationId = localStorage.getItem('chat_conversation_id');
    if (!conversationId) {
      conversationId = genUUID();
      localStorage.setItem('chat_conversation_id', conversationId);
    }
    var userId = localStorage.getItem('rozoom_user_id');
    if (!userId) {
      userId = genUUID();
      localStorage.setItem('rozoom_user_id', userId);
    }

    function genUUID() {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
    }

    function detectLanguage() {
      var htmlLang = (document.documentElement.lang || '').toLowerCase();
      if (htmlLang.includes('uk')) return 'uk';
      if (htmlLang.includes('ru')) return 'ru';
      if (htmlLang.includes('de')) return 'de';
      if (htmlLang.includes('en')) return 'en';
      var lang = (navigator.language || navigator.userLanguage || 'uk').toLowerCase();
      if (lang.includes('uk') || lang === 'ua') return 'uk';
      if (lang.includes('ru')) return 'ru';
      if (lang.includes('de')) return 'de';
      if (lang.includes('en')) return 'en';
      return 'uk';
    }

    // Agent selection state
    var selectedAgent = localStorage.getItem('rozoom_selected_agent') || 'greeter';
    function setSelectedAgent(agent) {
      selectedAgent = agent || 'greeter';
      localStorage.setItem('rozoom_selected_agent', selectedAgent);
      // Update UI state
      [btnGreeter, btnSpec, btnPm].forEach(function(b){ if (!b) return; b.classList.remove('active'); });
      var map = { greeter: btnGreeter, spec: btnSpec, pm: btnPm };
      if (map[selectedAgent]) map[selectedAgent].classList.add('active');
    }
    setSelectedAgent(selectedAgent);

    function appendMsg(text, cls) {
      var div = document.createElement('div');
      div.className = 'chat-msg ' + (cls || 'bot');
      div.innerHTML = (text || '').replace(/\n/g, '<br>');
      messages.appendChild(div);
      messages.scrollTop = messages.scrollHeight;
      return div;
    }

    function showThinking() {
      var d = document.createElement('div');
      d.className = 'chat-msg bot thinking';
      for (var i = 0; i < 3; i++) {
        var dot = document.createElement('div');
        dot.className = 'thinking-dot';
        d.appendChild(dot);
      }
      messages.appendChild(d);
      messages.scrollTop = messages.scrollHeight;
      return d;
    }

    function sendMessage() {
      var text = (input.value || '').trim();
      if (!text) return;

      appendMsg(text, 'user');
      input.value = '';

      var thinking = showThinking();

      var headers = { 'Content-Type': 'application/json' };
      var tokenMeta = document.querySelector('meta[name="csrf-token"]');
      if (tokenMeta) headers['X-CSRFToken'] = tokenMeta.getAttribute('content');

      var metadata = {
        language: detectLanguage(),
        page: window.location.pathname,
        user_id: userId,
        conversation_id: conversationId,
        selected_agent: selectedAgent
      };

      fetch('/api/chat', {
        method: 'POST',
        headers: headers,
        body: JSON.stringify({ message: text, metadata: metadata })
      })
      .then(function(res){ return res.json().catch(function(){ return {}; }); })
      .then(function(data){
        if (thinking && thinking.remove) thinking.remove();
        var ans = (data && data.answer) ? data.answer : (
          metadata.language === 'uk' ? 'Сталася помилка. Спробуйте ще раз.' :
          metadata.language === 'ru' ? 'Произошла ошибка. Попробуйте еще раз.' :
          metadata.language === 'de' ? 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es erneut.' :
          'An error occurred. Please try again.'
        );
        appendMsg(ans, 'bot');
        if (data && data.conversation_id) {
          conversationId = data.conversation_id;
          localStorage.setItem('chat_conversation_id', conversationId);
        }
      })
      .catch(function(){
        if (thinking && thinking.remove) thinking.remove();
        var lang = detectLanguage();
        var err = lang === 'uk' ? 'Проблема зі з\'єднанням. Спробуйте пізніше.' :
                  lang === 'ru' ? 'Проблема с подключением. Попробуйте позже.' :
                  lang === 'de' ? 'Verbindungsproblem. Bitte später erneut versuchen.' :
                                   'Connection problem. Please try later.';
        appendMsg(err, 'bot');
      });
    }

    // Agent toggle events
    function wireAgentButton(btn, agentKey, presetMessage) {
      if (!btn) return;
      btn.addEventListener('click', function(){
        setSelectedAgent(agentKey);
        // Send a silent handoff message (empty) to keep the same conversation and context
        var thinking = showThinking();
        var headers = { 'Content-Type': 'application/json' };
        var tokenMeta = document.querySelector('meta[name="csrf-token"]');
        if (tokenMeta) headers['X-CSRFToken'] = tokenMeta.getAttribute('content');
        var metadata = {
          language: detectLanguage(),
          page: window.location.pathname,
          user_id: userId,
          conversation_id: conversationId,
          selected_agent: selectedAgent,
          suppress_greeting: true
        };
        fetch('/api/chat', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({ message: presetMessage || '', metadata: metadata })
        })
        .then(function(res){ return res.json().catch(function(){ return {}; }); })
        .then(function(data){ if (thinking && thinking.remove) thinking.remove(); if (data && data.answer) appendMsg(data.answer, 'bot'); })
        .catch(function(){ if (thinking && thinking.remove) thinking.remove(); });
      });
    }
    wireAgentButton(btnGreeter, 'greeter');
    wireAgentButton(btnSpec, 'spec');
    wireAgentButton(btnPm, 'pm');

    // Expose openChat to allow templates to open with a specific agent and optional message
    window.openChat = function(agentKey, text){
      try { if (toggle && chatWindow && chatWindow.classList.contains('hidden')) { toggle.click(); } } catch(e){}
      if (agentKey) setSelectedAgent(agentKey);
      if (typeof text === 'string' && text.trim()) {
        input.value = text;
        sendMessage();
      } else {
        // Send silent to fetch agent greeting/state without losing history
        var thinking = showThinking();
        var headers = { 'Content-Type': 'application/json' };
        var tokenMeta = document.querySelector('meta[name="csrf-token"]');
        if (tokenMeta) headers['X-CSRFToken'] = tokenMeta.getAttribute('content');
        var metadata = {
          language: detectLanguage(),
          page: window.location.pathname,
          user_id: userId,
          conversation_id: conversationId,
          selected_agent: selectedAgent,
          suppress_greeting: true
        };
        fetch('/api/chat', {
          method: 'POST',
          headers: headers,
          body: JSON.stringify({ message: '', metadata: metadata })
        })
        .then(function(res){ return res.json().catch(function(){ return {}; }); })
        .then(function(data){ if (thinking && thinking.remove) thinking.remove(); if (data && data.answer) appendMsg(data.answer, 'bot'); })
        .catch(function(){ if (thinking && thinking.remove) thinking.remove(); });
      }
    };

    // Events
    send.addEventListener('click', function(e){ e.preventDefault(); sendMessage(); });
    input.addEventListener('keypress', function(e){ if (e.key === 'Enter') { e.preventDefault(); sendMessage(); } });
    if (toggle && chatWindow) {
      toggle.addEventListener('click', function(){
        var isHidden = chatWindow.classList.contains('hidden');
        if (isHidden) { chatWindow.classList.remove('hidden'); toggle.classList.add('active'); }
        else { chatWindow.classList.add('hidden'); toggle.classList.remove('active'); }
      });
    }
    if (closeBtn && chatWindow) {
      closeBtn.addEventListener('click', function(){ chatWindow.classList.add('hidden'); if (toggle) toggle.classList.remove('active'); });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
