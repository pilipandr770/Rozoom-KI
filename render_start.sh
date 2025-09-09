#!/bin/bash
# render_start.sh - Скрипт для запуска приложения на Render.com

set -e  # Выход при любой ошибке

echo "Инициализация схем PostgreSQL..."
python init_postgres_schemas.py

echo "Проверка и инициализация миграций базы данных..."
# Пробуем запустить миграции
if ! flask db upgrade 2>/dev/null; then
    echo "Ошибка при миграции базы данных. Инициализация миграций с нуля..."
    python init_migrations.py
fi

echo "Инициализация таблиц базы данных..."
python -m app.database

echo "Запуск Gunicorn с конфигурационным файлом..."
gunicorn -c gunicorn_config.py run:app
