// Скрипт для исправления проблем с футером
document.addEventListener('DOMContentLoaded', function() {
    // Получаем все ссылки в футере
    const footerLinks = document.querySelectorAll('.footer-link, .site-footer a');
    
    // Применяем корректировки к каждой ссылке
    footerLinks.forEach(link => {
        // Убеждаемся, что ссылки кликабельны
        link.style.pointerEvents = 'auto';
        link.style.cursor = 'pointer';
        link.style.zIndex = '1000';
        
        // Проверяем и исправляем URL если нужно
        if (link.getAttribute('href') && link.getAttribute('href').startsWith('/')) {
            const path = link.getAttribute('href');
            const origin = window.location.origin;
            
            // Проверяем, что URL правильно формируется
            console.log(`Ссылка в футере: ${path} (полный URL: ${origin}${path})`);
        }
        
        // Добавляем обработчик события клика для отладки
        link.addEventListener('click', function(e) {
            console.log(`Клик по ссылке: ${this.href}`);
            
            // Проверка, если ссылка не работает
            if (e.defaultPrevented) {
                console.error('Клик был предотвращен по умолчанию!');
            }
        });
    });
    
    // Проверяем, нет ли перекрывающих элементов
    const footer = document.querySelector('.site-footer');
    if (footer) {
        const footerRect = footer.getBoundingClientRect();
        const elements = document.elementsFromPoint(
            footerRect.left + footerRect.width/2,
            footerRect.top + footerRect.height/2
        );
        
        // Проверяем, какие элементы могут перекрывать футер
        elements.forEach(el => {
            if (el !== footer && !footer.contains(el) && 
                getComputedStyle(el).zIndex !== 'auto' && 
                parseInt(getComputedStyle(el).zIndex) > parseInt(getComputedStyle(footer).zIndex)) {
                console.warn('Элемент может перекрывать футер:', el);
            }
        });
    }
});
