# gunicorn_config.py
import multiprocessing

# Основные настройки
bind = "0.0.0.0:10000"  # Render автоматически переназначает порт через $PORT, но здесь указываем дефолтный
workers = multiprocessing.cpu_count() * 2 + 1  # Рекомендуемое количество воркеров
worker_class = "gevent"  # Используем gevent для асинхронной обработки запросов
timeout = 120  # Увеличиваем таймаут для долгих операций с API OpenAI
keepalive = 5

# Логирование
accesslog = "-"  # Вывод логов в stdout для Render
errorlog = "-"
loglevel = "info"

# Настройки для повышения производительности
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50  # Предотвращение одновременного перезапуска всех воркеров

# Настройки безопасности
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190
