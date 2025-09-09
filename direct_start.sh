#!/bin/bash
# direct_start.sh - Альтернативный скрипт для запуска приложения на Render.com
# Игнорирует миграции и напрямую создаёт таблицы

set -e

# Инициализируем схемы
python init_postgres_schemas.py

# Исправляем проблемы с app/database.py
echo "Исправление проблем с app/database.py..."
python fix_app_database.py || echo "Продолжаем несмотря на ошибки в fix_app_database.py"

# Используем прямую инициализацию базы данных
echo "Прямая инициализация базы данных..."
python direct_db_init.py

if [ $? -ne 0 ]; then
    echo "Основной метод прямой инициализации базы данных не сработал. Пробуем упрощенный метод..."
    python simple_create_tables.py
    
    if [ $? -ne 0 ]; then
        echo "КРИТИЧЕСКАЯ ОШИБКА: Не удалось инициализировать базу данных!"
        exit 1
    fi
fi

# Запускаем приложение
gunicorn -c gunicorn_config.py run:app
