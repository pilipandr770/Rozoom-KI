#!/bin/bash
# direct_start.sh - Альтернативный скрипт для запуска приложения на Render.com
# Игнорирует миграции и напрямую создаёт таблицы

set -e

# Инициализируем схемы
python init_postgres_schemas.py

# Создаем таблицы напрямую
python setup_postgres_tables.py

# Запускаем приложение
gunicorn -c gunicorn_config.py run:app
