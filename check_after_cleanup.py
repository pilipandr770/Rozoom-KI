#!/usr/bin/env python3
"""
Скрипт для проверки работоспособности проекта после очистки.
Запускайте после удаления файлов, чтобы убедиться, что ничего не сломалось.
"""

import os
import sys
import subprocess

def check_file_exists(filepath, description):
    """Проверяет существование файла"""
    if os.path.exists(filepath):
        print(f"✅ {description}: найден")
        return True
    else:
        print(f"❌ {description}: НЕ НАЙДЕН - {filepath}")
        return False

def check_directory_exists(dirpath, description):
    """Проверяет существование директории"""
    if os.path.exists(dirpath):
        print(f"✅ {description}: найдена")
        return True
    else:
        print(f"❌ {description}: НЕ НАЙДЕНА - {dirpath}")
        return False

def run_command(command, description):
    """Запускает команду и проверяет результат"""
    try:
        print(f"\n🔍 Проверка: {description}")
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)

        if result.returncode == 0:
            print(f"✅ {description}: успешно")
            return True
        else:
            print(f"❌ {description}: ошибка")
            print(f"   Код выхода: {result.returncode}")
            if result.stderr:
                print(f"   Ошибка: {result.stderr[:200]}...")
            return False
    except subprocess.TimeoutExpired:
        print(f"❌ {description}: таймаут")
        return False
    except Exception as e:
        print(f"❌ {description}: исключение - {e}")
        return False

def main():
    """Основная функция проверки"""
    print("🔍 ПРОВЕРКА ПРОЕКТА ПОСЛЕ ОЧИСТКИ")
    print("=" * 50)

    all_good = True

    # Проверка критически важных файлов
    print("\n📁 Проверка наличия критически важных файлов:")

    critical_files = [
        ("run.py", "Точка входа приложения"),
        ("requirements.txt", "Файл зависимостей"),
        ("Procfile", "Конфигурация Heroku/Render"),
        ("render.yaml", "Конфигурация Render"),
        (".env", "Переменные окружения"),
        ("app/__init__.py", "Основной модуль приложения"),
        ("app/models.py", "Модели базы данных"),
        ("app/routes.py", "Маршруты приложения"),
        ("app/templates/base.html", "Базовый шаблон"),
        ("app/templates/index.html", "Главная страница"),
        ("app/templates/services.html", "Страница услуг"),
    ]

    for filepath, description in critical_files:
        if not check_file_exists(filepath, description):
            all_good = False

    # Проверка важных директорий
    print("\n📂 Проверка наличия важных директорий:")

    critical_dirs = [
        ("app", "Основное приложение"),
        ("app/templates", "Шаблоны"),
        ("app/static", "Статические файлы"),
        ("migrations", "Миграции базы данных"),
        ("logs", "Логи приложения"),
    ]

    for dirpath, description in critical_dirs:
        if not check_directory_exists(dirpath, description):
            all_good = False

    # Проверка работоспособности Python
    print("\n🐍 Проверка Python и зависимостей:")

    python_checks = [
        ("python --version", "Версия Python"),
        ("python -c \"import flask\"", "Импорт Flask"),
        ("python -c \"import sqlalchemy\"", "Импорт SQLAlchemy"),
        ("python -c \"from app import create_app\"", "Импорт приложения"),
    ]

    for command, description in python_checks:
        if not run_command(command, description):
            all_good = False

    # Проверка конфигурации
    print("\n⚙️  Проверка конфигурации:")

    try:
        from app import create_app
        app = create_app()
        with app.app_context():
            print("✅ Конфигурация приложения: загружена успешно")
    except Exception as e:
        print(f"❌ Конфигурация приложения: ошибка - {e}")
        all_good = False

    # Проверка базы данных
    print("\n🗄️  Проверка базы данных:")

    try:
        from app import create_app, db
        app = create_app()
        with app.app_context():
            # Простая проверка подключения
            db.engine.execute("SELECT 1")
            print("✅ Подключение к базе данных: успешно")
    except Exception as e:
        print(f"❌ Подключение к базе данных: ошибка - {e}")
        all_good = False

    # Финальный результат
    print("\n" + "=" * 50)
    if all_good:
        print("🎉 ВСЕ ПРОВЕРКИ ПРОШЛИ УСПЕШНО!")
        print("✅ Проект готов к работе после очистки")
    else:
        print("⚠️  ОБНАРУЖЕНЫ ПРОБЛЕМЫ!")
        print("❌ Проверьте ошибки выше и исправьте их")
        print("💡 Возможно, нужно восстановить некоторые файлы из git")

    print("\n📋 РЕКОМЕНДАЦИИ:")
    print("1. Если все проверки прошли - проект готов к развертыванию")
    print("2. Если есть ошибки - восстановите файлы из предыдущего коммита:")
    print("   git checkout HEAD~1")
    print("3. Протестируйте основные функции приложения вручную")

    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
