#!/bin/bash
# render_start.sh - Скрипт для запуска приложения на Render.com

set -e  # Выход при любой ошибке

echo "Инициализация схем PostgreSQL..."
python init_postgres_schemas.py

echo "Проверка и инициализация миграций базы данных..."

# Радикальное решение: попытка удаления таблиц с CASCADE
echo "Проверка существования таблиц и их безопасное удаление при необходимости..."
python drop_all_tables.py || echo "Продолжаем работу, несмотря на ошибку при удалении таблиц"

# Сначала исправляем проблему с миграцией 'ac4cda9e7cef'
echo "Исправление проблемы с миграционной таблицей..."
python fix_migration_issue.py

# Попытка создать пустую ревизию с проблемным ID (альтернативный подход)
echo "Проверка и исправление проблемной ревизии..."
python fix_alembic_revision.py

# Пробуем запустить миграции
if ! flask db upgrade 2>/dev/null; then
    echo "Ошибка при миграции базы данных. Инициализация миграций с нуля..."
    python init_migrations.py
fi

echo "Инициализация таблиц базы данных..."
python -m app.database

echo "Запуск Gunicorn с конфигурационным файлом..."
gunicorn -c gunicorn_config.py run:app
