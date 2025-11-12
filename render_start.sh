#!/bin/bash
# render_start.sh - Оптимизированный скрипт для запуска приложения на Render.com

set -e  # Выход при любой ошибке

echo "=== НАЧАЛО РАЗВЕРТЫВАНИЯ ==="
echo "Текущая дата: $(date)"
echo "Python версия: $(python --version)"
echo "Pip версия: $(pip --version)"

# ВАЖНО: Компилируем все переводы в самом начале, включая доменные переводы
echo "Компиляция всех файлов переводов (.po -> .mo)..."
if python compile_all_translations.py; then
    echo "✅ Все файлы переводов успешно скомпилированы"
else
    echo "⚠️ Ошибка при выполнении скрипта компиляции переводов, пробуем резервный метод..."
    
    # Компилируем основные файлы переводов
    if pybabel compile -d app/translations; then
        echo "✅ Основные файлы переводов успешно скомпилированы"
    else
        echo "⚠️ Ошибка компиляции основных переводов"
    fi
    
    # Компилируем доменные файлы переводов
    if pybabel compile -d app/translations -D payment_translations -f; then
        echo "✅ Файлы переводов платежей успешно скомпилированы"
    else
        echo "⚠️ Ошибка компиляции файлов переводов платежей"
    fi
    
    # Другие важные домены
    for domain in "form_translations" "contact_translations" "pricing_translations"; do
        if pybabel compile -d app/translations -D $domain -f; then
            echo "✅ Домен $domain успешно скомпилирован"
        else
            echo "⚠️ Ошибка компиляции домена $domain"
        fi
    done
fi

# Настраиваем хранилище для изображений
echo "Настраиваем хранилище для изображений..."
if [ -n "$RENDER_PERSISTENT_DIR" ]; then
    mkdir -p "$RENDER_PERSISTENT_DIR/static/img/blog"
    echo "✅ Хранилище изображений создано в: $RENDER_PERSISTENT_DIR/static/img"
else
    mkdir -p "app/static/img/blog"
    echo "⚠️ RENDER_PERSISTENT_DIR не установлен. Изображения будут храниться во временной файловой системе."
fi

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

# Переводы уже были скомпилированы в начале скрипта
echo "Пропуск повторной компиляции файлов переводов..."

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
    if init_postgres_schemas.create_schema():
        print('✅ Схемы PostgreSQL инициализированы')
    else:
        print('⚠️ Не удалось инициализировать схемы PostgreSQL')
    
    # Очистка памяти
    gc.collect()
    
    print('✅ Схема инициализирована')
    
except Exception as e:
    print(f'⚠️  Предупреждение: {e}, продолжаем...')
" 2>/dev/null; then
    echo "✅ База данных подготовлена"
else
    echo "⚠️  Предупреждение: проблемы с подготовкой базы данных, продолжаем..."
fi

# Create database tables using dedicated script
echo "Создание таблиц базы данных..."
if bash create_tables.sh; then
    echo "✅ Таблицы базы данных созданы успешно"
else
    echo "⚠️ Предупреждение: проблемы с созданием таблиц, приложение попытается создать их при запуске..."
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

# Old migration code removed - end marker
# This comment prevents duplicate code below
OLD_CODE_REMOVED_MARKER=1
