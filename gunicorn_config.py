# gunicorn_config.py
import multiprocessing
import os

# Основные настройки
bind = "0.0.0.0:10000"  # Render автоматически переназначает порт через $PORT, но здесь указываем дефолтный

# Оптимизация для Render (512 MB памяти)
# Используем минимальное количество воркеров для экономии памяти
cpu_count = multiprocessing.cpu_count()
workers = min(2, cpu_count)  # Максимум 2 воркера для экономии памяти

worker_class = "gevent"  # Используем gevent для асинхронной обработки запросов
timeout = 120  # Увеличиваем таймаут для долгих операций с API OpenAI
keepalive = 5

# Логирование
accesslog = "-"  # Вывод логов в stdout для Render
errorlog = "-"
loglevel = "info"

# Настройки для повышения производительности с учетом ограничений памяти
worker_connections = 500  # Уменьшаем для экономии памяти
max_requests = 500  # Уменьшаем для предотвращения утечек памяти
max_requests_jitter = 25  # Предотвращение одновременного перезапуска всех воркеров

# Настройки безопасности
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Дополнительные настройки для экономии памяти
preload_app = True  # Предварительная загрузка приложения для экономии памяти
worker_tmp_dir = "/tmp"  # Использование tmp для временных файлов
