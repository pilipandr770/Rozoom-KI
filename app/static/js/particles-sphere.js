// Particles Sphere Animation
document.addEventListener('DOMContentLoaded', function() {
  // Проверяем наличие контейнера для сферы частиц
  const container = document.getElementById('particles-sphere-container');
  
  if (!container) return;
  
  // Создаем canvas для отрисовки частиц
  const canvas = document.createElement('canvas');
  canvas.width = container.offsetWidth;
  canvas.height = container.offsetHeight;
  canvas.style.position = 'absolute';
  canvas.style.top = '0';
  canvas.style.left = '0';
  canvas.style.width = '100%';
  canvas.style.height = '100%';
  container.appendChild(canvas);
  
  const ctx = canvas.getContext('2d');
  
  // Параметры для сферы
  const radius = Math.min(canvas.width, canvas.height) * 0.2; // радиус сферы
  const particleCount = 500; // количество частиц
  const particles = [];
  
  // Параметры вращения
  let rotationX = 0;
  let rotationY = 0;
  const rotationSpeed = 0.001;
  
  // Функция для создания частиц
  function createParticles() {
    for (let i = 0; i < particleCount; i++) {
      // Случайные углы для распределения по сфере
      const theta = Math.random() * Math.PI * 2; // по горизонтали
      const phi = Math.acos((Math.random() * 2) - 1); // по вертикали
      
      // Преобразование сферических координат в декартовы
      const x = radius * Math.sin(phi) * Math.cos(theta);
      const y = radius * Math.sin(phi) * Math.sin(theta);
      const z = radius * Math.cos(phi);
      
      // Добавляем частицу
      particles.push({
        x, y, z,
        size: 1 + Math.random() * 2,
        color: `rgba(${100 + Math.random() * 155}, ${150 + Math.random() * 105}, 255, ${0.4 + Math.random() * 0.6})`,
        originalX: x,
        originalY: y,
        originalZ: z
      });
    }
  }
  
  // Функция анимации
  function animate() {
    requestAnimationFrame(animate);
    
    // Очищаем canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Обновляем вращение
    rotationX += rotationSpeed;
    rotationY += rotationSpeed * 0.7;
    
    // Центр canvas
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    
    // Отрисовываем все частицы
    particles.forEach(particle => {
      // Применяем вращение к координатам частиц
      let x = particle.originalX;
      let y = particle.originalY;
      let z = particle.originalZ;
      
      // Вращение по Y (вокруг вертикальной оси)
      const cosY = Math.cos(rotationY);
      const sinY = Math.sin(rotationY);
      const rotatedX = x * cosY - z * sinY;
      const rotatedZ = z * cosY + x * sinY;
      
      // Вращение по X (вокруг горизонтальной оси)
      const cosX = Math.cos(rotationX);
      const sinX = Math.sin(rotationX);
      const finalY = y * cosX - rotatedZ * sinX;
      const finalZ = rotatedZ * cosX + y * sinX;
      
      // Используем финальные координаты
      x = rotatedX;
      y = finalY;
      z = finalZ;
      
      // Масштабирование частиц в зависимости от Z-координаты для эффекта перспективы
      const scale = 700 / (700 - z);
      const screenX = centerX + x * scale;
      const screenY = centerY + y * scale;
      
      // Изменение размера и прозрачности в зависимости от позиции
      const alpha = (z + radius) / (radius * 2);
      const size = particle.size * scale;
      
      // Отрисовка частицы
      ctx.fillStyle = particle.color.replace(')', `, ${alpha})`).replace('rgba', 'rgba');
      ctx.beginPath();
      ctx.arc(screenX, screenY, size, 0, Math.PI * 2);
      ctx.fill();
    });
  }
  
  // Создаем частицы
  createParticles();
  
  // Адаптивность при изменении размера окна
  window.addEventListener('resize', function() {
    canvas.width = container.offsetWidth;
    canvas.height = container.offsetHeight;
  });
  
  // Запускаем анимацию
  animate();
});
