/**
 * CSRF Token management script
 * Handles automatic refreshing of CSRF tokens and retrying form submissions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Add CSRF token refresh functionality to all forms on the page
    setupCsrfTokenHandling();
});

function setupCsrfTokenHandling() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        // Skip forms that might be handled by other scripts
        if (form.classList.contains('no-csrf-handler')) {
            return;
        }
        
        form.addEventListener('submit', function(event) {
            const csrfToken = form.querySelector('input[name="csrf_token"]');
            if (!csrfToken || !csrfToken.value) {
                event.preventDefault();
                console.log('CSRF token missing, attempting to refresh...');
                refreshCsrfToken(form).then(() => {
                    form.submit();
                }).catch(error => {
                    console.error('Failed to refresh CSRF token:', error);
                    alert('Ошибка безопасности: Не удалось обновить токен CSRF. Пожалуйста, перезагрузите страницу.');
                });
            }
        });
    });
}

/**
 * Refreshes the CSRF token for a specific form by making an AJAX request
 * @param {HTMLFormElement} form - The form element to update with a new token
 * @returns {Promise} - Promise that resolves when the token is refreshed
 */
function refreshCsrfToken(form) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '/refresh-csrf-token', true);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        if (response.csrf_token) {
                            const tokenInput = form.querySelector('input[name="csrf_token"]');
                            if (tokenInput) {
                                tokenInput.value = response.csrf_token;
                                console.log('CSRF token successfully refreshed');
                                resolve();
                            } else {
                                const newInput = document.createElement('input');
                                newInput.type = 'hidden';
                                newInput.name = 'csrf_token';
                                newInput.value = response.csrf_token;
                                form.appendChild(newInput);
                                console.log('CSRF token input created and added to form');
                                resolve();
                            }
                        } else {
                            reject(new Error('CSRF token not found in response'));
                        }
                    } catch (e) {
                        reject(new Error('Failed to parse CSRF token response'));
                    }
                } else {
                    reject(new Error(`Failed to refresh CSRF token: ${xhr.status}`));
                }
            }
        };
        xhr.onerror = function() {
            reject(new Error('Network error occurred while refreshing CSRF token'));
        };
        xhr.send();
    });
}
