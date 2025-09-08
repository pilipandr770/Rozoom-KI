/**
 * Функционал переключения языка для чат-виджета
 */

document.addEventListener('DOMContentLoaded', function() {
    // Находим селектор языка на странице
    const languageSelector = document.querySelector('.language-selector');
    if (!languageSelector) return;
    
    // Находим все кнопки переключения языка
    const langButtons = languageSelector.querySelectorAll('.lang-button');
    
    // Проверяем, инициализирован ли чат
    function waitForChatWidget() {
        if (window.chatWidget) {
            setupLanguageHandlers();
        } else {
            setTimeout(waitForChatWidget, 100);
        }
    }
    
    // Настраиваем обработчики для кнопок языка
    function setupLanguageHandlers() {
        langButtons.forEach(button => {
            button.addEventListener('click', function() {
                const lang = this.getAttribute('data-lang');
                if (lang && window.chatWidget) {
                    // Устанавливаем язык в метаданные чата
                    const currentMetadata = window.chatWidget.getMetadata() || {};
                    currentMetadata.language = lang;
                    
                    // Обновляем метаданные
                    window.chatWidget.setMetadata(currentMetadata);
                    
                    // Перезапускаем чат для применения нового языка
                    window.chatWidget.restartChat();
                    
                    // Обновляем активный класс для кнопок
                    langButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                }
            });
        });
    }
    
    // Запускаем проверку наличия чат-виджета
    waitForChatWidget();
});
