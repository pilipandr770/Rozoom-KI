#!/bin/bash
# direct_start.sh - Альтернативный скрипт для запуска приложения на Render.com
# Игнорирует миграции и напрямую создаёт таблицы

set -e

echo "=== АЛЬТЕРНАТИВНЫЙ ЗАПУСК (БЕЗ МИГРАЦИЙ) ==="
echo "Текущая дата: $(date)"

# Инициализируем схемы
echo "Инициализация схем PostgreSQL..."
if python init_postgres_schemas.py; then
    echo "✅ Схемы PostgreSQL успешно инициализированы"
else
    echo "⚠️  Предупреждение: проблемы с инициализацией схем, продолжаем..."
fi

# Исправляем проблемы с app/database.py
echo "Исправление проблем с app/database.py..."
if python fix_app_database.py; then
    echo "✅ app/database.py успешно исправлен"
else
    echo "⚠️  Предупреждение: проблемы с fix_app_database.py, продолжаем..."
fi

# Исправляем проблемы с дублирующимися столбцами
echo "Исправление проблем с дублирующимися столбцами..."
if python fix_duplicate_columns.py; then
    echo "✅ Дублирующиеся столбцы исправлены"
else
    echo "⚠️  Предупреждение: проблемы с fix_duplicate_columns.py, продолжаем..."
fi

# Исправляем проблемы с ревизией миграции
echo "Исправление проблем с ревизией миграции..."
if python fix_revision_issue.py; then
    echo "✅ Проблемы с ревизией миграции исправлены"
else
    echo "⚠️  Предупреждение: проблемы с fix_revision_issue.py, продолжаем..."
fi

# Используем прямую инициализацию базы данных
echo "Прямая инициализация базы данных..."
if python direct_db_init.py; then
    echo "✅ База данных инициализирована через direct_db_init.py"
else
    echo "⚠️  Основной метод прямой инициализации базы данных не сработал. Пробуем упрощенный метод..."
    if python simple_create_tables.py; then
        echo "✅ Таблицы созданы через simple_create_tables.py"
    else
        echo "❌ КРИТИЧЕСКАЯ ОШИБКА: Не удалось инициализировать базу данных!"
        exit 1
    fi
fi

# Запускаем приложение
echo "=== ЗАПУСК ПРИЛОЖЕНИЯ ==="
echo "Время запуска: $(date)"
echo "Команда: gunicorn -c gunicorn_config.py run:app"

exec gunicorn -c gunicorn_config.py run:app
