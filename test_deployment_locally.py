#!/usr/bin/env python3
"""
test_deployment_locally.py

Скрипт для локального тестирования процесса развертывания.
Проверяет все компоненты без реального запуска сервера.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_file_exists(filepath, description):
    """Проверяет существование файла"""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - НЕ НАЙДЕН")
        return False

def check_python_imports():
    """Проверяет основные импорты Python"""
    print("\n=== ПРОВЕРКА PYTHON ИМПОРТОВ ===")

    imports = [
        ('flask', 'Flask'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('flask_sqlalchemy', 'Flask-SQLAlchemy'),
        ('psycopg2', 'psycopg2-binary'),
        ('gunicorn', 'Gunicorn'),
        ('openai', 'OpenAI'),
        ('flask_migrate', 'Flask-Migrate'),
        ('dotenv', 'python-dotenv'),
        ('stripe', 'Stripe'),
        ('flask_wtf', 'Flask-WTF'),
        ('flask_login', 'Flask-Login'),
        ('flask_babel', 'Flask-Babel'),
        ('flask_mail', 'Flask-Mail'),
        ('apscheduler', 'APScheduler'),
        ('gevent', 'Gevent'),
    ]

    failed_imports = []
    for module, description in imports:
        try:
            __import__(module)
            print(f"✅ {description}")
        except ImportError as e:
            print(f"❌ {description}: {e}")
            failed_imports.append(module)

    return len(failed_imports) == 0

def test_database_connection():
    """Тестирует подключение к базе данных"""
    print("\n=== ТЕСТ ПОДКЛЮЧЕНИЯ К БД ===")

    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("⚠️  DATABASE_URL не установлена - пропускаем тест БД")
        return True

    try:
        from sqlalchemy import create_engine, text

        # Исправляем URL для PostgreSQL
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        # Add SSL parameters for PostgreSQL connections (required for Render.com)
        if 'postgresql://' in database_url:
            if '?' not in database_url:
                database_url += '?sslmode=require'
            else:
                database_url += '&sslmode=require'

        engine = create_engine(database_url)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Подключение к базе данных успешно")
            return True
    except Exception as e:
        print(f"❌ Ошибка подключения к БД: {e}")
        return False

def test_app_creation():
    """Тестирует создание Flask приложения"""
    print("\n=== ТЕСТ СОЗДАНИЯ ПРИЛОЖЕНИЯ ===")

    try:
        # Добавляем текущую директорию в путь
        sys.path.insert(0, str(Path(__file__).parent))

        from app import create_app

        app = create_app()
        print("✅ Flask приложение создано успешно")
        print(f"   Режим: {os.getenv('FLASK_ENV', 'development')}")
        print(f"   Debug: {app.debug}")
        print(f"   Testing: {app.testing}")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания приложения: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("=== ЛОКАЛЬНОЕ ТЕСТИРОВАНИЕ РАЗВЕРТЫВАНИЯ ===\n")

    # Проверяем наличие файлов
    print("=== ПРОВЕРКА ФАЙЛОВ ===")
    files_ok = True

    critical_files = [
        ('render.yaml', 'Конфигурация Render'),
        ('render_start.sh', 'Основной скрипт запуска'),
        ('direct_start.sh', 'Альтернативный скрипт запуска'),
        ('run.py', 'Точка входа приложения'),
        ('gunicorn_config.py', 'Конфигурация Gunicorn'),
        ('requirements.txt', 'Зависимости Python'),
        ('init_postgres_schemas.py', 'Инициализация схем PostgreSQL'),
        ('init_migrations.py', 'Инициализация миграций'),
        ('direct_db_init.py', 'Прямая инициализация БД'),
        ('simple_create_tables.py', 'Простое создание таблиц'),
    ]

    for filepath, description in critical_files:
        if not check_file_exists(filepath, description):
            files_ok = False

    # Проверяем импорты
    imports_ok = check_python_imports()

    # Тестируем подключение к БД
    db_ok = test_database_connection()

    # Тестируем создание приложения
    app_ok = test_app_creation()

    # Итоговый отчет
    print("\n" + "="*50)
    print("=== РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ ===")

    all_ok = files_ok and imports_ok and db_ok and app_ok

    if all_ok:
        print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("✅ Развертывание готово к запуску на Render.com")
    else:
        print("⚠️  ОБНАРУЖЕНЫ ПРОБЛЕМЫ:")
        if not files_ok:
            print("   - Отсутствуют критические файлы")
        if not imports_ok:
            print("   - Проблемы с импортами Python")
        if not db_ok:
            print("   - Проблемы с подключением к БД")
        if not app_ok:
            print("   - Проблемы с созданием Flask приложения")

    print("\nРекомендации:")
    print("- Убедитесь, что все зависимости установлены: pip install -r requirements.txt")
    print("- Проверьте переменные окружения в Render dashboard")
    print("- Мониторьте логи развертывания в Render")

    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
