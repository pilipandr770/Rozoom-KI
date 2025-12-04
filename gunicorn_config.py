# gunicorn_config.py
import multiprocessing
import os

# Базові настройки
bind = "0.0.0.0:10000"  # Render сам підставить PORT
cpu_count = multiprocessing.cpu_count()

# Воркер на потоках замість gevent, щоб уникнути проблем із SSL monkey-patch
worker_class = "gthread"
workers = min(2, cpu_count)         # небагато воркерів для економії пам'яті
threads = 4                         # пара потоків на воркер — достатньо
timeout = 120                       # щоб не обривати повільні запити до OpenAI
keepalive = 5

# Логування
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Ліміти/стабільність
worker_connections = 100
max_requests = 500
max_requests_jitter = 25

# Безпека
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Скрыть версию Gunicorn из заголовка Server
import gunicorn
gunicorn.SERVER_SOFTWARE = 'Undisclosed'

# ВАЖЛИВО: не pre-load з gthread це не критично, але краще лишити False для передбачуваності
preload_app = False
worker_tmp_dir = "/tmp"
