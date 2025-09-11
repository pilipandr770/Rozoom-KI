/**
 * Локализация чат-виджета
 * Поддержка языков: DE, EN, RU, UK
 */

document.addEventListener('DOMContentLoaded', function() {
    // Переводы для интерфейса чата
    const chatTranslations = {
        // Немецкий
        'de': {
            'startOver': 'Neustart',
            'sendButton': 'Senden',
            'inputPlaceholder': 'Nachricht eingeben...',
            'optionsPlaceholder': 'Sie können eine Option oben auswählen oder Ihre eigene Frage stellen...',
            'loadingMessage': 'Wird geladen...',
            'switchingToSpecialist': 'Wechseln zum Spezialisten...',
            'connectionError': 'Entschuldigung, es gab ein Problem mit der Verbindung. Bitte versuchen Sie es später noch einmal.',
            'somethingWentWrong': 'Entschuldigung, etwas ist schief gelaufen. Bitte versuchen Sie es erneut.'
        },
        // Английский
        'en': {
            'startOver': 'Start over',
            'sendButton': 'Send',
            'inputPlaceholder': 'Type a message...',
            'optionsPlaceholder': 'You can choose an option above or ask your own question...',
            'loadingMessage': 'Loading...',
            'switchingToSpecialist': 'Switching to specialist...',
            'connectionError': 'Sorry, there was a problem with the connection. Please try again later.',
            'somethingWentWrong': 'Sorry, something went wrong. Please try again.'
        },
        // Русский
        'ru': {
            'startOver': 'Начать сначала',
            'sendButton': 'Отправить',
            'inputPlaceholder': 'Введите сообщение...',
            'optionsPlaceholder': 'Вы можете выбрать опцию выше или задать свой вопрос...',
            'loadingMessage': 'Загрузка...',
            'switchingToSpecialist': 'Переключение на специалиста...',
            'connectionError': 'Извините, возникла проблема с подключением. Пожалуйста, попробуйте позже.',
            'somethingWentWrong': 'Извините, что-то пошло не так. Пожалуйста, попробуйте еще раз.'
        },
        // Украинский
        'uk': {
            'startOver': 'Почати знову',
            'sendButton': 'Надіслати',
            'inputPlaceholder': 'Введіть повідомлення...',
            'optionsPlaceholder': 'Ви можете вибрати опцію вище або поставити своє запитання...',
            'loadingMessage': 'Завантаження...',
            'switchingToSpecialist': 'Перемикання на спеціаліста...',
            'connectionError': 'Вибачте, виникла проблема з підключенням. Будь ласка, спробуйте пізніше.',
            'somethingWentWrong': 'Вибачте, щось пішло не так. Будь ласка, спробуйте ще раз.'
        }
    };

    // Глобальный объект для доступа к переводам
    window.chatTranslations = chatTranslations;
    
    // Текущий язык (по умолчанию 'de')
    let currentLang = 'de';
    
    // Функция для получения текущего языка из метаданных чата
    function getCurrentLanguage() {
        if (window.chatWidget && window.chatWidget.getMetadata) {
            const metadata = window.chatWidget.getMetadata();
            if (metadata && metadata.language) {
                return metadata.language;
            }
        }
        
        // Если не можем получить из метаданных, пытаемся найти активную кнопку языка
        const activeButton = document.querySelector('.lang-button.active');
        if (activeButton && activeButton.getAttribute('data-lang')) {
            return activeButton.getAttribute('data-lang');
        }
        
        return currentLang;
    }
    
    // Функция для получения перевода
    function translate(key) {
        const lang = getCurrentLanguage();
        
        // Если есть перевод для этого языка и ключа
        if (chatTranslations[lang] && chatTranslations[lang][key]) {
            return chatTranslations[lang][key];
        }
        
        // Если нет, пробуем вернуть английский перевод
        if (chatTranslations['en'] && chatTranslations['en'][key]) {
            return chatTranslations['en'][key];
        }
        
        // Если и его нет, возвращаем ключ
        return key;
    }
    
    // Экспортируем функцию перевода в глобальный объект
    window.translateChat = translate;
    
    // Функция для обновления текстов интерфейса
    function updateChatUITexts() {
        // Обновляем кнопку отправки сообщения
        const sendButton = document.getElementById('chat-send');
        if (sendButton) {
            sendButton.title = translate('sendButton');
        }
        
        // Обновляем плейсхолдер поля ввода
        const inputField = document.getElementById('chat-input');
        if (inputField) {
            inputField.placeholder = translate('inputPlaceholder');
        }
        
        // Обновляем кнопку "Начать сначала", если она есть
        const restartButton = document.querySelector('.restart-button');
        if (restartButton) {
            // Сохраняем иконку, если она есть
            const iconHtml = restartButton.innerHTML.match(/<i[^>]*><\/i>/);
            restartButton.innerHTML = (iconHtml ? iconHtml[0] + ' ' : '') + translate('startOver');
        }
    }
    
    // Функция для наблюдения за изменениями в DOM
    function observeChatUI() {
        // Создаем observer для отслеживания изменений в DOM
        const observer = new MutationObserver(function(mutations) {
            mutations.forEach(function(mutation) {
                if (mutation.addedNodes.length) {
                    updateChatUITexts();
                }
            });
        });
        
        // Находим элемент чата
        const chatContainer = document.getElementById('chat-widget');
        if (chatContainer) {
            // Настраиваем наблюдение
            observer.observe(chatContainer, {
                childList: true,
                subtree: true
            });
        }
    }
    
    // Инициализация после загрузки чата
    function waitForChatWidget() {
        if (window.chatWidget) {
            // Обновляем тексты и начинаем наблюдение за изменениями
            updateChatUITexts();
            observeChatUI();
            
            // Переопределяем методы для локализации
            const originalRestartChat = window.chatWidget.restartChat;
            window.chatWidget.restartChat = function() {
                originalRestartChat.call(window.chatWidget);
                // Обновляем тексты после перезапуска чата
                setTimeout(updateChatUITexts, 500);
            };
            
        } else {
            setTimeout(waitForChatWidget, 100);
        }
    }
    
    // Запускаем инициализацию
    waitForChatWidget();
});
