#!/bin/bash
# render_start.sh - Оптимизированный скрипт для запуска приложения на Render.com

set -e  # Выход при любой ошибке

echo "=== НАЧАЛО РАЗВЕРТЫВАНИЯ ==="
echo "Текущая дата: $(date)"
echo "Python версия: $(python --version)"
echo "Pip версия: $(pip --version)"

# ВАЖНО: Компилируем переводы в самом начале, чтобы убедиться, что они доступны
echo "Компиляция файлов переводов (.po -> .mo)..."
if pybabel compile -d app/translations; then
    echo "✅ Файлы переводов успешно скомпилированы"
else
    echo "⚠️ Ошибка компиляции переводов, пробуем альтернативный метод..."
    python -c "
import os, glob
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

for po_file in glob.glob('app/translations/**/LC_MESSAGES/*.po', recursive=True):
    mo_file = po_file[:-3] + '.mo'
    print(f'Компиляция {po_file} -> {mo_file}')
    try:
        with open(po_file, 'rb') as f_in:
            catalog = read_po(f_in)
        with open(mo_file, 'wb') as f_out:
            write_mo(f_out, catalog)
    except Exception as e:
        print(f'Ошибка компиляции {po_file}: {e}')
print('Компиляция завершена')
"
    echo "✅ Файлы переводов скомпилированы через python"
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

# Компилируем файлы переводов (.po -> .mo)
echo "Компиляция файлов переводов..."
if pybabel compile -d app/translations; then
    echo "✅ Файлы переводов успешно скомпилированы"
else
    echo "⚠️ Ошибка компиляции переводов, пытаемся использовать альтернативный метод..."
    python -c "
import os, glob
from babel.messages.mofile import write_mo
from babel.messages.pofile import read_po

for po_file in glob.glob('app/translations/**/LC_MESSAGES/*.po', recursive=True):
    mo_file = po_file[:-3] + '.mo'
    print(f'Компиляция {po_file} -> {mo_file}')
    try:
        with open(po_file, 'rb') as f_in:
            catalog = read_po(f_in)
        with open(mo_file, 'wb') as f_out:
            write_mo(f_out, catalog)
    except Exception as e:
        print(f'Ошибка компиляции {po_file}: {e}')
print('Компиляция завершена')
"
    echo "✅ Компиляция переводов через временный скрипт завершена"
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
    if python -c "
import sys
import os
from sqlalchemy import inspect, create_engine, Column, String, text
from sqlalchemy.orm import sessionmaker

try:
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
    
    # Проверяем и добавляем колонки для хранения оригинальных URL изображений
    with engine.connect() as conn:
        # Проверяем таблицу blog_posts
        if not inspector.has_table('blog_posts'):
            print('Таблица blog_posts не существует, пропускаем миграцию изображений')
        else:
            columns = [col['name'] for col in inspector.get_columns('blog_posts')]
            if 'original_image_url' not in columns:
                print('Добавляем original_image_url в blog_posts...')
                conn.execute(text('ALTER TABLE blog_posts ADD COLUMN original_image_url VARCHAR(500)'))
                print('✅ Колонка original_image_url добавлена в blog_posts')
            
            if 'image_url' not in columns:
                print('Добавляем image_url в blog_posts...')
                conn.execute(text('ALTER TABLE blog_posts ADD COLUMN image_url VARCHAR(500)'))
                print('✅ Колонка image_url добавлена в blog_posts')
        
        # Проверяем таблицу generated_content
        if not inspector.has_table('generated_content'):
            print('Таблица generated_content не существует, пропускаем миграцию изображений')
        else:
            columns = [col['name'] for col in inspector.get_columns('generated_content')]
            if 'original_image_url' not in columns:
                print('Добавляем original_image_url в generated_content...')
                conn.execute(text('ALTER TABLE generated_content ADD COLUMN original_image_url VARCHAR(500)'))
                print('✅ Колонка original_image_url добавлена в generated_content')
            
            if 'image_url' not in columns:
                print('Добавляем image_url в generated_content...')
                conn.execute(text('ALTER TABLE generated_content ADD COLUMN image_url VARCHAR(500)'))
                print('✅ Колонка image_url добавлена в generated_content')
        
        conn.commit()
    
    print('✅ Миграция изображений выполнена успешно')
    
except Exception as e:
    print(f'⚠️ Ошибка при миграции изображений: {e}')
    sys.exit(1)
"; then
        echo "✅ Миграция изображений успешно выполнена"
    else
        echo "⚠️ Ошибка при миграции изображений, продолжаем..."
    fi
fi

# Пытаемся сначала инициализировать миграции с нуля
echo "Инициализация миграций с поддержкой CASCADE..."
if python -c "
import sys
import os
from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import text

try:
    # Создаем Flask приложение для работы с миграциями
    app = Flask(__name__)
    
    # Настраиваем базу данных
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    database_url = database_url or 'sqlite:///app/dev.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Импортируем модели
    from app.models import db
    db.init_app(app)
    
    # Инициализируем миграции
    migrate = Migrate(app, db)
    
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        
        # Включаем поддержку CASCADE для внешних ключей
        if 'postgresql' in database_url:
            db.session.execute(text('SET CONSTRAINTS ALL DEFERRED'))
        
        print('✅ Миграции инициализированы успешно')
        
except Exception as e:
    print(f'⚠️ Ошибка при инициализации миграций: {e}')
    sys.exit(1)
"; then
    echo "✅ Миграции успешно инициализированы"
else
    echo "⚠️  Ошибка при инициализации миграций. Используем прямое создание таблиц..."
    if python -c "
import sys
import os
from flask import Flask
from sqlalchemy import text

try:
    # Создаем Flask приложение
    app = Flask(__name__)
    
    # Настраиваем базу данных
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    database_url = database_url or 'sqlite:///app/dev.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Импортируем модели
    from app.models import db
    db.init_app(app)
    
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        print('✅ Все таблицы созданы успешно')
        
except Exception as e:
    print(f'⚠️ Ошибка при создании таблиц: {e}')
    sys.exit(1)
"; then
        echo "✅ Таблицы созданы через inline код"
    else
        echo "⚠️  Попытка использования альтернативного метода инициализации базы данных..."
        if python -c "
import sys
import os
from flask import Flask
from sqlalchemy import text, inspect

try:
    # Создаем Flask приложение
    app = Flask(__name__)
    
    # Настраиваем базу данных
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    database_url = database_url or 'sqlite:///app/dev.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Импортируем модели
    from app.models import db
    db.init_app(app)
    
    with app.app_context():
        # Проверяем существование таблиц
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        # Создаем таблицы, которые отсутствуют
        if 'users' not in existing_tables:
            db.session.execute(text('''
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(80) UNIQUE NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    password_hash VARCHAR(128),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
        
        if 'blog_posts' not in existing_tables:
            db.session.execute(text('''
                CREATE TABLE blog_posts (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    content TEXT,
                    image_url VARCHAR(500),
                    original_image_url VARCHAR(500),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
        
        if 'generated_content' not in existing_tables:
            db.session.execute(text('''
                CREATE TABLE generated_content (
                    id SERIAL PRIMARY KEY,
                    title VARCHAR(200),
                    content TEXT,
                    image_url VARCHAR(500),
                    original_image_url VARCHAR(500),
                    content_type VARCHAR(50),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            '''))
        
        db.session.commit()
        print('✅ База данных инициализирована успешно')
        
except Exception as e:
    print(f'⚠️ Ошибка при прямой инициализации БД: {e}')
    sys.exit(1)
"; then
            echo "✅ База данных инициализирована через inline код"
        else
            echo "⚠️  Попытка исправления проблем с инициализацией базы данных..."
            if python -c "
import sys
import os
from flask import Flask
from sqlalchemy import text, inspect

try:
    # Создаем Flask приложение
    app = Flask(__name__)
    
    # Настраиваем базу данных
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    database_url = database_url or 'sqlite:///app/dev.db'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Импортируем модели
    from app.models import db
    db.init_app(app)
    
    with app.app_context():
        # Проверяем и исправляем структуру таблиц
        inspector = inspect(db.engine)
        
        # Исправляем таблицу users
        if inspector.has_table('users'):
            columns = [col['name'] for col in inspector.get_columns('users')]
            if 'id' not in columns:
                db.session.execute(text('ALTER TABLE users ADD COLUMN id SERIAL PRIMARY KEY'))
            if 'username' not in columns:
                db.session.execute(text('ALTER TABLE users ADD COLUMN username VARCHAR(80) UNIQUE'))
            if 'email' not in columns:
                db.session.execute(text('ALTER TABLE users ADD COLUMN email VARCHAR(120) UNIQUE'))
        
        # Исправляем таблицу blog_posts
        if inspector.has_table('blog_posts'):
            columns = [col['name'] for col in inspector.get_columns('blog_posts')]
            if 'id' not in columns:
                db.session.execute(text('ALTER TABLE blog_posts ADD COLUMN id SERIAL PRIMARY KEY'))
            if 'title' not in columns:
                db.session.execute(text('ALTER TABLE blog_posts ADD COLUMN title VARCHAR(200)'))
            if 'content' not in columns:
                db.session.execute(text('ALTER TABLE blog_posts ADD COLUMN content TEXT'))
            if 'image_url' not in columns:
                db.session.execute(text('ALTER TABLE blog_posts ADD COLUMN image_url VARCHAR(500)'))
            if 'original_image_url' not in columns:
                db.session.execute(text('ALTER TABLE blog_posts ADD COLUMN original_image_url VARCHAR(500)'))
        
        # Исправляем таблицу generated_content
        if inspector.has_table('generated_content'):
            columns = [col['name'] for col in inspector.get_columns('generated_content')]
            if 'id' not in columns:
                db.session.execute(text('ALTER TABLE generated_content ADD COLUMN id SERIAL PRIMARY KEY'))
            if 'title' not in columns:
                db.session.execute(text('ALTER TABLE generated_content ADD COLUMN title VARCHAR(200)'))
            if 'content' not in columns:
                db.session.execute(text('ALTER TABLE generated_content ADD COLUMN content TEXT'))
            if 'image_url' not in columns:
                db.session.execute(text('ALTER TABLE generated_content ADD COLUMN image_url VARCHAR(500)'))
            if 'original_image_url' not in columns:
                db.session.execute(text('ALTER TABLE generated_content ADD COLUMN original_image_url VARCHAR(500)'))
        
        db.session.commit()
        print('✅ Проблемы с инициализацией исправлены')
        
except Exception as e:
    print(f'❌ КРИТИЧЕСКАЯ ОШИБКА: {e}')
    sys.exit(1)
"; then
                echo "✅ Проблемы с инициализацией исправлены через inline код"
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
