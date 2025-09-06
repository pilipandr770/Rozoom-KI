/**
 * Скрипт для управления темным анимированным фоном
 */

document.addEventListener('DOMContentLoaded', function() {
  // Проверяем, существует ли анимированный фон на странице
  const backgroundContainer = document.querySelector('.dark-animated-background');
  
  if (backgroundContainer) {
    // Инициализация анимированного фона
    initDarkAnimatedBackground();
    
    // Добавляем обработчик изменения размера окна
    window.addEventListener('resize', function() {
      initDarkAnimatedBackground();
    });
  }
});

/**
 * Инициализирует темный анимированный фон с частицами
 */
function initDarkAnimatedBackground() {
  // Создаем контейнер для частиц, если его еще нет
  let particlesContainer = document.querySelector('.particles-container');
  if (particlesContainer) {
    // Очищаем существующие частицы для обновления
    particlesContainer.innerHTML = '';
    
    // Создаем новые частицы
    createParticles(particlesContainer);
  }

}

/**
 * Создает набор частиц в указанном контейнере
 * @param {HTMLElement} container - DOM элемент для добавления частиц
 */
function createParticles(container) {
  // Количество частиц зависит от размера экрана
  const width = window.innerWidth;
  const height = window.innerHeight;
  const particleCount = Math.floor((width * height) / 25000); // Примерно 30-40 частиц на обычном экране
  
  // Создаем новые частицы
  for (let i = 0; i < particleCount; i++) {
    createFloatingParticle(container);
  }
}

/**
 * Создает плавающую частицу с уникальными параметрами
 * @param {HTMLElement} container - DOM элемент для размещения частицы
 */
function createFloatingParticle(container) {
  // Создаем DOM элемент
  const particle = document.createElement('div');
  particle.classList.add('particle');
  
  // Случайный размер
  const size = Math.random() * 6 + 1; // 1-7px
  
  // Позиция
  const posX = Math.random() * 100; // В процентах
  const posY = Math.random() * 100; // В процентах
  
  // Настраиваем стили
  particle.style.width = `${size}px`;
  particle.style.height = `${size}px`;
  particle.style.left = `${posX}%`;
  particle.style.top = `${posY}%`;
  
  // Прозрачность
  const opacity = Math.random() * 0.5 + 0.1; // 0.1-0.6
  particle.style.opacity = opacity;
  
  // Скорость анимации
  const duration = Math.random() * 50 + 30; // 30-80s
  particle.style.animationDuration = `${duration}s`;
  
  // Задержка старта анимации
  const delay = Math.random() * 10;
  particle.style.animationDelay = `-${delay}s`;
  
  // Добавляем частицу в контейнер
  container.appendChild(particle);
}

/**
 * Создает эффект волны на фоне
 * Этот эффект добавляет движущиеся волны в нижней части экрана
 */
function createWaveEffect() {
  // Проверяем, есть ли уже волны
  let waveContainer = document.querySelector('.wave-container');
  
  if (!waveContainer) {
    waveContainer = document.createElement('div');
    waveContainer.classList.add('wave-container');
    
    // Создаем три волны с разными свойствами
    for (let i = 1; i <= 3; i++) {
      const wave = document.createElement('div');
      wave.classList.add('wave', `wave-${i}`);
      waveContainer.appendChild(wave);
    }
    
    const backgroundContainer = document.querySelector('.dark-animated-background');
    if (backgroundContainer) {
      backgroundContainer.appendChild(waveContainer);
    }
  }
}

// Добавляем эффект волны после загрузки страницы
window.addEventListener('load', function() {
  setTimeout(createWaveEffect, 100);
});
