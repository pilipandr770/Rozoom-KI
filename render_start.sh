#!/bin/bash
# render_start.sh - Скрипт для запуска приложения на Render.com

set -e  # Выход при любой ошибке

echo "Инициализация схем PostgreSQL..."
python init_postgres_schemas.py

echo "Исправление проблем с app/database.py..."
python fix_app_database.py || echo "Продолжаем несмотря на ошибки в fix_app_database.py"

echo "Проверка и инициализация миграций базы данных..."

# Пытаемся сначала инициализировать миграции с нуля
echo "Инициализация миграций с поддержкой CASCADE..."
if ! python init_migrations.py; then
    echo "Ошибка при инициализации миграций. Используем прямое создание таблиц..."
    python simple_create_tables.py
    
    if [ $? -ne 0 ]; then
        echo "Попытка использования альтернативного метода инициализации базы данных..."
        python direct_db_init.py
        
        if [ $? -ne 0 ]; then
            echo "Попытка исправления проблем с инициализацией базы данных..."
            python fix_db_init.py
            
            if [ $? -ne 0 ]; then
                echo "КРИТИЧЕСКАЯ ОШИБКА: Не удалось создать таблицы!"
                exit 1
            fi
        fi
    fi
fi

echo "Инициализация таблиц базы данных..."
python -m app.database

echo "Запуск Gunicorn с конфигурационным файлом..."
gunicorn -c gunicorn_config.py run:app
