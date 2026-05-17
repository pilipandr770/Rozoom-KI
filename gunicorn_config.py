# gunicorn_config.py
import multiprocessing
import os

# Bind to the PORT env var Render injects; fall back to 10000 for local runs
bind = f"0.0.0.0:{os.getenv('PORT', '10000')}"
cpu_count = multiprocessing.cpu_count()

# gthread: thread-based workers — no gevent monkey-patching, safe with SSL
worker_class = "gthread"
workers = min(2, cpu_count)   # keep memory footprint small on Render free tier
threads = 4                   # 2 workers × 4 threads = 8 concurrent requests
timeout = 120                 # hard cap per request (OpenAI streaming ≤ 60 s)
graceful_timeout = 30         # time for in-flight requests on shutdown
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Stability
max_requests = 500
max_requests_jitter = 50      # randomise restart to avoid thundering herd

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Hide Gunicorn version from Server header
import gunicorn
gunicorn.SERVER_SOFTWARE = 'Undisclosed'

# Preload app once in master; workers get a CoW copy — saves ~30 MB RAM per worker
preload_app = True
worker_tmp_dir = "/tmp"


def post_fork(server, worker):
    """Give each forked worker a fresh asyncio event loop.

    Required with preload_app=True on Python 3.12+: the master's loop must not
    be reused by child processes — install a new one instead of closing the old.
    """
    import asyncio
    asyncio.set_event_loop(asyncio.new_event_loop())
