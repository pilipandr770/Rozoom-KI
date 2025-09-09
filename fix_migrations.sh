#!/bin/bash
# fix_migrations.sh - Скрипт для исправления проблем с миграциями на Render.com

set -e  # Выход при любой ошибке

# Проверяем переменные окружения
if [ -z "$DATABASE_URL" ]; then
    echo "ОШИБКА: Переменная окружения DATABASE_URL не установлена"
    exit 1
fi

echo "Фиксация проблем с миграциями на Render.com"
echo "================================================="

echo "1. Инициализация схем PostgreSQL"
python init_postgres_schemas.py

echo "2. Инициализация миграций с нуля"
python init_migrations.py

echo "3. Создание таблиц напрямую"
python setup_postgres_tables.py

echo "4. Проверка состояния базы данных"
flask db current

echo "================================================="
echo "Процесс исправления миграций завершен."
echo "Теперь можно перезапустить веб-сервис на Render.com"
