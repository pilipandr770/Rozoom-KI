/**
 * This file contains a diagnostic script to check if the chat widget is functioning correctly.
 * It will log the status of key DOM elements and event listeners.
 */

// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('Chat widget diagnostic script running...');
    
    // Check if essential elements exist
    const elements = {
        chatWidget: document.getElementById('chat-widget'),
        toggle: document.getElementById('chat-toggle'),
        closeBtn: document.getElementById('chat-close'),
        windowEl: document.getElementById('chat-window'),
        messagesEl: document.getElementById('chat-messages'),
        input: document.getElementById('chat-input'),
        send: document.getElementById('chat-send')
    };
    
    console.log('Chat widget elements status:');
    Object.entries(elements).forEach(([name, element]) => {
        console.log(`${name}: ${element ? 'Found ✓' : 'Missing ✗'}`);
    });
    
    // Verify that the toggle button is clickable
    if (elements.toggle) {
        // Get computed styles
        const style = window.getComputedStyle(elements.toggle);
        console.log('Toggle button styles:');
        console.log(`- Position: ${style.position}`);
        console.log(`- Z-index: ${style.zIndex}`);
        console.log(`- Display: ${style.display}`);
        console.log(`- Pointer-events: ${style.pointerEvents}`);
        
        // Apply a manual fix if needed
        if (style.pointerEvents === 'none') {
            console.log('⚠️ Fixing pointer-events on toggle button');
            elements.toggle.style.pointerEvents = 'auto';
        }
        
        // Test if event listeners are working
        console.log('Adding test click handler to toggle button...');
        elements.toggle.addEventListener('click', function testClickHandler() {
            console.log('Toggle button clicked! 🎉');
            // Remove this test handler after first click
            elements.toggle.removeEventListener('click', testClickHandler);
        });
        
        // Force z-index to be high
        elements.toggle.style.zIndex = '9999';
        
        // Add a visual indicator
        elements.toggle.style.boxShadow = '0 0 0 3px red';
        setTimeout(() => {
            elements.toggle.style.boxShadow = '';
        }, 2000);
    }
    
    // Add a manual toggle function to the window for emergency usage
    window.forceToggleChat = function() {
        console.log('Forcing chat toggle...');
        if (elements.windowEl) {
            elements.windowEl.classList.toggle('hidden');
            if (!elements.windowEl.classList.contains('hidden')) {
                console.log('Chat window opened');
                if (elements.messagesEl && elements.messagesEl.children.length === 0) {
                    console.log('Chat is empty, would normally trigger greeting');
                }
            } else {
                console.log('Chat window closed');
            }
        }
    };
    
    console.log('Chat diagnostic complete. Try clicking the chat button or run window.forceToggleChat() in the console');
});
