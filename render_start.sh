#!/bin/bash
# render_start.sh - Оптимизированный скрипт для запуска приложения на Render.com

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

# Оптимизированная инициализация базы данных - объединяем операции для экономии памяти
echo "Инициализация базы данных и исправление проблем..."
if python -c "
import sys
import gc
import os
os.environ['PYTHONPATH'] = '.'

try:
    # Инициализация схем
    print('Инициализация схем PostgreSQL...')
    import init_postgres_schemas
    print('✅ Схемы PostgreSQL инициализированы')
    
    # Очистка памяти
    gc.collect()
    
    # Исправление проблем с database.py
    print('Исправление проблем с app/database.py...')
    import fix_app_database
    print('✅ app/database.py исправлен')
    
    # Очистка памяти
    gc.collect()
    
    # Исправление дублирующихся столбцов
    print('Исправление дублирующихся столбцов...')
    import fix_duplicate_columns
    print('✅ Дублирующиеся столбцы исправлены')
    
    # Очистка памяти
    gc.collect()
    
    # Исправление ревизии миграции
    print('Исправление проблем с ревизией миграции...')
    import fix_revision_issue
    print('✅ Проблемы с ревизией миграции исправлены')
    
    print('✅ Все исправления выполнены успешно')
    
except Exception as e:
    print(f'⚠️  Предупреждение: {e}, продолжаем...')
" 2>/dev/null; then
    echo "✅ База данных подготовлена"
else
    echo "⚠️  Предупреждение: проблемы с подготовкой базы данных, продолжаем..."
fi

# Очистка памяти перед запуском миграций
echo "Очистка памяти..."
python -c "import gc; gc.collect()"

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

# Финальная очистка памяти
echo "Финальная очистка памяти перед запуском приложения..."
python -c "import gc; gc.collect()"

echo "Запуск Gunicorn с конфигурационным файлом..."
echo "=== ЗАПУСК ПРИЛОЖЕНИЯ ==="
echo "Время запуска: $(date)"
echo "Команда: gunicorn -c gunicorn_config.py run:app"

# Проверяем использование памяти перед запуском
echo "Проверка доступной памяти..."
if command -v free >/dev/null 2>&1; then
    free -h
elif python -c "import psutil; print(f'Доступно памяти: {psutil.virtual_memory().available / 1024 / 1024:.1f} MB')"; then
    echo "✅ Проверка памяти выполнена"
else
    echo "⚠️  Не удалось проверить память, продолжаем..."
fi

# Запускаем Gunicorn
echo "Попытка запуска с оптимизированной конфигурацией..."
if exec gunicorn -c gunicorn_config.py run:app; then
    echo "✅ Приложение запущено успешно"
else
    echo "⚠️  Оптимизированная конфигурация не удалась, пробуем облегченную..."
    echo "Команда: gunicorn -c gunicorn_config_light.py run:app"
    exec gunicorn -c gunicorn_config_light.py run:app
fi
