#!/bin/bash
# render_start.sh - Скрипт для запуска приложения на Render.com

set -e  # Выход при любой ошибке

echo "=== НАЧАЛО РАЗВЕРТЫВАНИЯ ==="
echo "Текущая дата: $(date)"
echo "Python версия: $(python --version)"
echo "Pip версия: $(pip --version)"

# Проверяем наличие необходимых файлов
echo "Проверка наличия необходимых файлов..."
if [ ! -f "run.py" ]; then
    echo "ОШИБКА: run.py не найден!"
    exit 1
fi

if [ ! -f "gunicorn_config.py" ]; then
    echo "ОШИБКА: gunicorn_config.py не найден!"
    exit 1
fi

echo "Все необходимые файлы найдены."

echo "Инициализация схем PostgreSQL..."
if python init_postgres_schemas.py; then
    echo "✅ Схемы PostgreSQL успешно инициализированы"
else
    echo "⚠️  Предупреждение: проблемы с инициализацией схем, продолжаем..."
fi

echo "Исправление проблем с app/database.py..."
if python fix_app_database.py; then
    echo "✅ app/database.py успешно исправлен"
else
    echo "⚠️  Предупреждение: проблемы с fix_app_database.py, продолжаем..."
fi

echo "Исправление проблем с дублирующимися столбцами..."
if python fix_duplicate_columns.py; then
    echo "✅ Дублирующиеся столбцы исправлены"
else
    echo "⚠️  Предупреждение: проблемы с fix_duplicate_columns.py, продолжаем..."
fi

echo "Исправление проблем с ревизией миграции..."
if python fix_revision_issue.py; then
    echo "✅ Проблемы с ревизией миграции исправлены"
else
    echo "⚠️  Предупреждение: проблемы с fix_revision_issue.py, продолжаем..."
fi

echo "Проверка и инициализация миграций базы данных..."

# Пытаемся сначала инициализировать миграции с нуля
echo "Инициализация миграций с поддержкой CASCADE..."
if python init_migrations.py; then
    echo "✅ Миграции успешно инициализированы"
else
    echo "⚠️  Ошибка при инициализации миграций. Используем прямое создание таблиц..."
    if python simple_create_tables.py; then
        echo "✅ Таблицы созданы через simple_create_tables.py"
    else
        echo "⚠️  Попытка использования альтернативного метода инициализации базы данных..."
        if python direct_db_init.py; then
            echo "✅ База данных инициализирована через direct_db_init.py"
        else
            echo "⚠️  Попытка исправления проблем с инициализацией базы данных..."
            if python fix_db_init.py; then
                echo "✅ Проблемы с инициализацией исправлены через fix_db_init.py"
            else
                echo "❌ КРИТИЧЕСКАЯ ОШИБКА: Не удалось создать таблицы!"
                exit 1
            fi
        fi
    fi
fi

echo "Инициализация таблиц базы данных..."
if python -m app.database; then
    echo "✅ Таблицы базы данных инициализированы"
else
    echo "⚠️  Предупреждение: проблемы с инициализацией таблиц, продолжаем..."
fi

echo "Запуск Gunicorn с конфигурационным файлом..."
echo "=== ЗАПУСК ПРИЛОЖЕНИЯ ==="
echo "Время запуска: $(date)"
echo "Команда: gunicorn -c gunicorn_config.py run:app"

# Запускаем Gunicorn
exec gunicorn -c gunicorn_config.py run:app
