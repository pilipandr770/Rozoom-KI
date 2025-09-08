// Инициализация админ-функций
document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация скрипта админ-панели...');
    
    // Обработчик для форм удаления
    var deleteForms = document.querySelectorAll('.delete-post-form');
    console.log('Найдено форм удаления:', deleteForms.length);
    
    deleteForms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            // Проверка наличия CSRF токена
            var csrfToken = form.querySelector('input[name="csrf_token"]');
            if (!csrfToken || !csrfToken.value) {
                e.preventDefault();
                console.error('CSRF токен отсутствует!');
                alert('Ошибка безопасности: CSRF токен отсутствует. Пожалуйста, обновите страницу и попробуйте снова.');
            } else {
                console.log('Форма отправляется с CSRF токеном:', csrfToken.value);
            }
        });
    });
});
