/**
 * Provides a debugging overlay for the chat widget
 * Helps diagnose issues with sending messages
 */
(function() {
  console.log('Initializing chat debug overlay...');
  
  // Create debugging overlay
  function createDebugOverlay() {
    const overlay = document.createElement('div');
    overlay.id = 'chat-debug-overlay';
    overlay.style.position = 'fixed';
    overlay.style.bottom = '10px';
    overlay.style.left = '10px';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    overlay.style.color = '#0f0';
    overlay.style.padding = '10px';
    overlay.style.borderRadius = '5px';
    overlay.style.fontSize = '12px';
    overlay.style.fontFamily = 'monospace';
    overlay.style.maxWidth = '400px';
    overlay.style.maxHeight = '200px';
    overlay.style.overflow = 'auto';
    overlay.style.zIndex = '10001';
    overlay.style.display = 'none';
    
    const header = document.createElement('div');
    header.innerHTML = 'Chat Debug <span style="float:right; cursor:pointer;" onclick="document.getElementById(\'chat-debug-overlay\').style.display=\'none\'">✕</span>';
    header.style.borderBottom = '1px solid #0f0';
    header.style.marginBottom = '5px';
    header.style.paddingBottom = '5px';
    
    const content = document.createElement('div');
    content.id = 'chat-debug-content';
    
    overlay.appendChild(header);
    overlay.appendChild(content);
    document.body.appendChild(overlay);
    
    return overlay;
  }
  
  // Add logging
  const originalLog = console.log;
  const originalError = console.error;
  
  // Wait for DOM to be fully loaded
  document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
      const overlay = createDebugOverlay();
      const content = document.getElementById('chat-debug-content');
      
      // Add toggle button
      const toggleButton = document.createElement('button');
      toggleButton.textContent = '🛠️';
      toggleButton.style.position = 'fixed';
      toggleButton.style.left = '10px';
      toggleButton.style.bottom = '10px';
      toggleButton.style.zIndex = '10000';
      toggleButton.style.borderRadius = '50%';
      toggleButton.style.width = '30px';
      toggleButton.style.height = '30px';
      toggleButton.style.cursor = 'pointer';
      
      toggleButton.addEventListener('click', function() {
        overlay.style.display = overlay.style.display === 'none' ? 'block' : 'none';
      });
      
      document.body.appendChild(toggleButton);
      
      // Override console methods to capture chat-related logs
      console.log = function() {
        originalLog.apply(console, arguments);
        
        // Check if log is related to chat
        const logString = Array.from(arguments).join(' ');
        if (logString.includes('chat') || logString.includes('Chat')) {
          // Add to debug overlay
          const logEntry = document.createElement('div');
          logEntry.textContent = `✓ ${logString}`;
          logEntry.style.marginBottom = '3px';
          if (content.children.length > 20) {
            content.removeChild(content.firstChild);
          }
          content.appendChild(logEntry);
          content.scrollTop = content.scrollHeight;
        }
      };
      
      console.error = function() {
        originalError.apply(console, arguments);
        
        // Add to debug overlay regardless of content
        const logString = Array.from(arguments).join(' ');
        const logEntry = document.createElement('div');
        logEntry.textContent = `⚠️ ${logString}`;
        logEntry.style.color = '#ff5555';
        logEntry.style.marginBottom = '3px';
        if (content.children.length > 20) {
          content.removeChild(content.firstChild);
        }
        content.appendChild(logEntry);
        content.scrollTop = content.scrollHeight;
      };
      
      // Add network request interceptor
      const originalFetch = window.fetch;
      window.fetch = async function(url, options) {
        // Only intercept chat API calls
        if (url.includes('/api/chat')) {
          console.log(`API Request to ${url}`, options?.body ? JSON.parse(options.body) : {});
          
          try {
            const response = await originalFetch(url, options);
            const clone = response.clone();
            
            try {
              const data = await clone.json();
              console.log(`API Response from ${url}:`, data);
            } catch(e) {
              console.error(`Failed to parse API response: ${e.message}`);
            }
            
            return response;
          } catch(error) {
            console.error(`API Error for ${url}: ${error.message}`);
            throw error;
          }
        }
        
        return originalFetch(url, options);
      };
      
      console.log('Chat debug overlay initialized');
    }, 1000);
  });
})();
