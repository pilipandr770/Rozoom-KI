#!/bin/bash
# fix_migrations.sh - Скрипт для исправления проблем с миграциями на Render.com

set -e  # Выход при любой ошибке

# Проверяем переменные окружения
if [ -z "$DATABASE_URL" ]; then
    echo "ОШИБКА: Переменная окружения DATABASE_URL не установлена"
    exit 1
fi

# Сначала исправляем проблему с ревизией 'ac4cda9e7cef'
echo "0. Исправление проблемы с ревизией 'ac4cda9e7cef'"
python fix_migration_issue.py

echo "Фиксация проблем с миграциями на Render.com"
echo "================================================="

echo "1. Инициализация схем PostgreSQL"
python init_postgres_schemas.py

echo "2. Попытка безопасного удаления всех таблиц с CASCADE"
python drop_all_tables.py || echo "Продолжаем, несмотря на ошибки при удалении таблиц"

echo "3. Очистка таблицы alembic_version"
python fix_migration_issue.py

echo "4. Инициализация миграций с нуля"
python init_migrations.py

echo "5. Создание таблиц напрямую (если миграции не сработали)"
python setup_postgres_tables.py

echo "4. Проверка состояния базы данных"
flask db current

echo "================================================="
echo "Процесс исправления миграций завершен."
echo "Теперь можно перезапустить веб-сервис на Render.com"
