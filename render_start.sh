#!/bin/bash
# render_start.sh - Скрипт для запуска приложения на Render.com

set -e  # Выход при любой ошибке

echo "Инициализация схем PostgreSQL..."
python init_postgres_schemas.py

echo "Запуск миграций базы данных..."
flask db upgrade

echo "Запуск Gunicorn с конфигурационным файлом..."
gunicorn -c gunicorn_config.py run:app
