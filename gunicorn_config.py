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
timeout = 300                       # OpenAI/Telegram calls can be slow
graceful_timeout = 30               # time to finish in-flight requests on shutdown
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


def post_fork(server, worker):
    """Reset the asyncio event loop in each forked worker.

    Python 3.12+ (especially 3.14) raises RuntimeError if a worker inherits
    an event loop from the master process.  Calling close() on the inherited
    loop triggers its pending callbacks, which then fail with
    "loop is not the running loop" because a new loop was already installed.
    Safe fix: just install a fresh loop without touching the inherited one.
    """
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
