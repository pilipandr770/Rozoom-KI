/**
 * JavaScript для улучшенного переключения языков
 */
document.addEventListener('DOMContentLoaded', function() {
    initLanguageSwitcher();
});

function initLanguageSwitcher() {
    // Находим все кнопки переключения языка
    const langButtons = document.querySelectorAll('.lang-button');
    
    langButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            // Если текущий язык уже активен, не делаем ничего
            if (this.classList.contains('active')) {
                event.preventDefault();
                return;
            }
            
            // Получаем URL для переключения языка
            const langUrl = this.getAttribute('href');
            
            // Предотвращаем стандартное поведение ссылки
            event.preventDefault();
            
            // Анимация нажатия
            this.classList.add('clicked');
            setTimeout(() => this.classList.remove('clicked'), 300);
            
            // Делаем AJAX запрос для переключения языка
            fetch(langUrl, {
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Обновляем активный класс на кнопках
                    langButtons.forEach(btn => btn.classList.remove('active'));
                    this.classList.add('active');
                    
                    // Перезагружаем страницу для применения изменений
                    location.reload();
                }
            })
            .catch(error => {
                console.error('Ошибка при переключении языка:', error);
                // В случае ошибки просто перенаправляем
                window.location.href = langUrl;
            });
        });
    });
}
