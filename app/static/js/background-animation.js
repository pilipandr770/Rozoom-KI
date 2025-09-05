/**
 * Скрипт для создания плавающих частиц в фоне
 */

document.addEventListener('DOMContentLoaded', function() {
  // Инициализация анимированного фона
  initAnimatedBackground();
});

/**
 * Инициализирует анимированный фон с частицами
 */
function initAnimatedBackground() {
  const container = document.querySelector('.particles-container');
  if (!container) return;

  // Очистим существующие частицы
  container.innerHTML = '';
  
  // Количество частиц зависит от размера экрана
  const width = window.innerWidth;
  const particleCount = width < 768 ? 15 : 30;

  // Создаем частицы
  for (let i = 0; i < particleCount; i++) {
    createParticle(container);
  }
}

/**
 * Создает отдельную частицу в контейнере
 * @param {HTMLElement} container - DOM элемент для добавления частицы
 */
function createParticle(container) {
  // Создаем DOM элемент
  const particle = document.createElement('div');
  particle.classList.add('particle');
  
  // Случайный размер
  const size = Math.random() * 8 + 2;
  
  // Случайное положение
  const x = Math.random() * 100;
  const y = Math.random() * 100;
  
  // Случайная прозрачность
  const opacity = Math.random() * 0.4 + 0.1;
  
  // Случайная задержка анимации
  const delay = Math.random() * -30;
  
  // Случайная длительность анимации
  const duration = Math.random() * 20 + 15;
  
  // Применяем стили
  particle.style.cssText = `
    width: ${size}px;
    height: ${size}px;
    left: ${x}%;
    top: ${y}%;
    opacity: ${opacity};
    animation-delay: ${delay}s;
    animation-duration: ${duration}s;
  `;
  
  // Добавляем в контейнер
  container.appendChild(particle);
}

/**
 * Обработка изменения размера окна
 */
window.addEventListener('resize', function() {
  // Пересоздаем частицы при изменении размера окна
  initAnimatedBackground();
});
