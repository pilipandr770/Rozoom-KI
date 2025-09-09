#!/bin/bash
# render_start.sh - Оптимизированный скрипт для запуска приложения на Render.com

set -e  # Выход при любой ошибке

echo "=== НАЧАЛО РАЗВЕРТЫВАНИЯ ==="
echo "Текущая дата: $(date)"
echo "Python версия: $(python --version)"
echo "Pip версия: $(pip --version)"

# ВАЖНО: Компилируем переводы в самом начале, чтобы убедиться, что они доступны
echo "Компиляция файлов переводов (.po -> .mo)..."
if python check_translations.py --compile; then
    echo "✅ Файлы переводов успешно скомпилированы"
else
    echo "⚠️ Ошибка компиляции переводов, пробуем альтернативный метод..."
    if pybabel compile -d app/translations; then
        echo "✅ Файлы переводов скомпилированы через pybabel"
    else 
        echo "⚠️ Пробуем еще один метод компиляции..."
        python -c "
import os, glob
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

for po_file in glob.glob('app/translations/**/LC_MESSAGES/*.po', recursive=True):
    mo_file = po_file[:-3] + '.mo'
    print(f'Компиляция {po_file} -> {mo_file}')
    with open(po_file, 'rb') as f_in:
        catalog = read_po(f_in)
    with open(mo_file, 'wb') as f_out:
        write_mo(f_out, catalog)
print('Компиляция завершена')
"
        echo "✅ Файлы переводов скомпилированы через python"
    fi
fi

# Настраиваем хранилище для изображений с использованием скрипта
echo "Настраиваем хранилище для изображений..."
if python setup_render_storage.py; then
    echo "✅ Хранилище изображений настроено"
else
    echo "⚠️ Ошибка при настройке хранилища изображений. Создаем базовые директории..."
    if [ -n "$RENDER_PERSISTENT_DIR" ]; then
        mkdir -p "$RENDER_PERSISTENT_DIR/static/img/blog"
        echo "✅ Хранилище изображений создано в: $RENDER_PERSISTENT_DIR/static/img"
    else
        mkdir -p "app/static/img/blog"
        echo "⚠️ RENDER_PERSISTENT_DIR не установлен. Изображения будут храниться во временной файловой системе."
    fi
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

# Компилируем файлы переводов (.po -> .mo)
echo "Компиляция файлов переводов..."
if python compile_translations.py; then
    echo "✅ Файлы переводов успешно скомпилированы"
else
    echo "⚠️ Ошибка компиляции переводов, пытаемся использовать альтернативный метод..."
    # Используем pybabel напрямую если доступен
    if command -v pybabel > /dev/null; then
        echo "Используем pybabel для компиляции переводов..."
        pybabel compile -d app/translations
        echo "✅ Компиляция с помощью pybabel завершена"
    else
        echo "⚠️ pybabel не доступен, используем интеграцию с Flask-Babel..."
        # Создаем временный скрипт для компиляции через Flask-Babel
        cat > compile_mo.py << 'EOF'
import os
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

def compile_all():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    translations_dir = os.path.join(base_dir, 'app', 'translations')
    
    for lang in os.listdir(translations_dir):
        lang_path = os.path.join(translations_dir, lang)
        if os.path.isdir(lang_path):
            lc_path = os.path.join(lang_path, 'LC_MESSAGES')
            if os.path.isdir(lc_path):
                for file in os.listdir(lc_path):
                    if file.endswith('.po'):
                        po_path = os.path.join(lc_path, file)
                        mo_path = os.path.join(lc_path, file[:-3] + '.mo')
                        try:
                            with open(po_path, 'rb') as po_file:
                                catalog = read_po(po_file)
                            with open(mo_path, 'wb') as mo_file:
                                write_mo(mo_file, catalog)
                            print(f"Compiled: {po_path} -> {mo_path}")
                        except Exception as e:
                            print(f"Error compiling {po_path}: {e}")

compile_all()
EOF
        python compile_mo.py
        echo "✅ Компиляция переводов через временный скрипт завершена"
    fi
fi

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

# Проверяем и запускаем миграцию для обновления структуры БД с новыми полями для хранения оригинальных URL изображений
echo "Проверка миграции для изображений блога..."
if python -c "
import sys
try:
    # Проверяем наличие колонок для хранения оригинальных URL изображений
    import os
    from app.models.blog import BlogPost
    from app.models.content_generation import GeneratedContent
    from sqlalchemy import inspect, create_engine
    from sqlalchemy.orm import sessionmaker
    
    # Получаем URL базы данных из переменной окружения
    database_url = os.environ.get('DATABASE_URL')
    
    # Исправляем URL для PostgreSQL, если необходимо
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Используем SQLite, если нет PostgreSQL URL
    database_url = database_url or 'sqlite:///app/dev.db'
    
    # Создаем соединение с базой данных
    engine = create_engine(database_url)
    inspector = inspect(engine)
    
    # Проверяем наличие колонки original_image_url в таблицах
    blog_columns = [col['name'] for col in inspector.get_columns('blog_posts')]
    content_columns = [col['name'] for col in inspector.get_columns('generated_content')]
    
    has_blog_original = 'original_image_url' in blog_columns
    has_content_original = 'original_image_url' in content_columns
    
    if not has_blog_original or not has_content_original:
        print(f'✅ Требуется миграция. blog_posts: {has_blog_original}, generated_content: {has_content_original}')
        sys.exit(1)
    else:
        print('✅ Колонки для хранения оригинальных URL изображений уже существуют.')
        sys.exit(0)
except Exception as e:
    print(f'⚠️ Ошибка при проверке колонок: {str(e)}')
    sys.exit(1)
"; then
    echo "✅ Структура БД для изображений актуальна"
else
    echo "⚠️ Запускаем миграцию для обновления структуры БД..."
    if python migrate_images.py; then
        echo "✅ Миграция изображений успешно выполнена"
    else
        echo "⚠️ Ошибка при миграции изображений, продолжаем..."
    fi
fi

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
