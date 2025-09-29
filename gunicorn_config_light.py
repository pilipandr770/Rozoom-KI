# gunicorn_config_light.py - lightweight gunicorn config for small instances
import multiprocessing

bind = "0.0.0.0:10000"
workers = 1
worker_class = "sync"
timeout = 60
keepalive = 2

accesslog = "-"
errorlog = "-"
loglevel = "info"

worker_connections = 100
max_requests = 200
max_requests_jitter = 10

limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

preload_app = True
worker_tmp_dir = "/tmp"
