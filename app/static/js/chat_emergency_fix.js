/**
 * Enhanced Chat Widget Diagnostics
 * 
 * This script helps diagnose and fix issues with the chat widget
 */

// Run diagnostics when the script loads
document.addEventListener('DOMContentLoaded', function() {
  setTimeout(runChatDiagnostics, 1000);
});

function runChatDiagnostics() {
  console.group('🔍 Chat Widget Diagnostics');
  
  // Check DOM elements
  const elements = {
    widget: document.getElementById('chat-widget'),
    toggle: document.getElementById('chat-toggle'),
    window: document.getElementById('chat-window'),
    messages: document.getElementById('chat-messages'),
    input: document.getElementById('chat-input'),
    send: document.getElementById('chat-send'),
    close: document.getElementById('chat-close')
  };
  
  console.log('DOM Elements:', elements);
  
  const missingElements = Object.entries(elements)
    .filter(([_, el]) => !el)
    .map(([name]) => name);
  
  if (missingElements.length > 0) {
    console.error('❌ Missing elements:', missingElements.join(', '));
  } else {
    console.log('✅ All required elements are present');
  }
  
  // Enhanced send button functionality check
  if (elements.send) {
    console.log('Enhancing send button...');
    elements.send.addEventListener('click', function(e) {
      console.log('Send button clicked via diagnostics');
      // The original event will still fire
    });
  }
  
  // Check CSRF tokens
  console.log('Checking CSRF protection...');
  
  fetch('/api/health')
    .then(response => {
      if (response.ok) {
        console.log('✅ API endpoint is accessible');
      } else {
        console.error('❌ API health check failed:', response.status);
      }
      return response.text();
    })
    .catch(error => {
      console.error('❌ API request failed:', error);
    });

  // Apply fixes
  applyEmergencyFixes(elements);
  
  console.groupEnd();
}

function applyEmergencyFixes(elements) {
  console.log('Applying emergency fixes...');
  
  // Fix 1: Ensure input field is properly initialized
  if (elements.input) {
    elements.input.value = elements.input.value || '';
    elements.input.disabled = false;
    elements.input.focus();
    
    // Add extra event listener for input field
    elements.input.addEventListener('input', function() {
      console.log('Input changed:', elements.input.value);
    });
  }
  
  // Fix 2: Force enable the send button
  if (elements.send) {
    elements.send.disabled = false;
    elements.send.style.opacity = '1';
    elements.send.style.cursor = 'pointer';
    
    // Add a direct click handler in case the original one is broken
    elements.send.onclick = function(event) {
      console.log('Send button clicked through emergency handler');
      const inputValue = elements.input ? elements.input.value.trim() : '';
      
      if (inputValue && window.chatWidget && typeof window.handleSendMessage === 'function') {
        console.log('Trying to send message through emergency handler:', inputValue);
        window.handleSendMessage();
      } else {
        console.log('Cannot send message: input is empty or handler missing');
      }
    };
  }
  
  // Fix 3: Make the chat window visible if needed
  if (elements.window && elements.window.classList.contains('hidden')) {
    console.log('Chat window is currently hidden');
  }
  
  // Fix 4: Add global emergency send function
  window.emergencySendChatMessage = function(text) {
    if (!text || !elements.input) return false;
    
    console.log('Sending message through emergency function:', text);
    elements.input.value = text;
    
    if (typeof window.handleSendMessage === 'function') {
      window.handleSendMessage();
      return true;
    }
    
    return false;
  };
  
  console.log('Emergency fixes applied. You can use window.emergencySendChatMessage("Your message") to force-send a message');
}
