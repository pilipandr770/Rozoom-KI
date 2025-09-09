# gunicorn_config_light.py - Облегченная конфигурация для ограниченной памяти
import multiprocessing

# Основные настройки для минимального потребления памяти
bind = "0.0.0.0:10000"
workers = 1  # Только 1 воркер для экономии памяти
worker_class = "sync"  # Синхронный воркер вместо gevent для меньшего потребления памяти
timeout = 60  # Уменьшаем таймаут
keepalive = 2

# Логирование
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Минимальные настройки производительности
worker_connections = 100
max_requests = 200
max_requests_jitter = 10

# Настройки безопасности
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Оптимизации памяти
preload_app = True
worker_tmp_dir = "/tmp"</content>
<parameter name="filePath">c:\Users\ПК\Rozoom-KI\gunicorn_config_light.py
