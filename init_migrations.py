#!/usr/bin/env python3
"""
init_migrations.py

Этот скрипт инициализирует миграции Flask-Migrate с нуля для чистой установки на Render.com.
Используйте этот скрипт, если при выполнении миграций возникают ошибки, связанные с отсутствующими ревизиями.
"""

import os
import sys
import shutil
from flask_migrate import init, migrate, upgrade
from app import create_app, db

def init_migrations():
    """Инициализирует миграции Flask-Migrate с нуля"""
    app = create_app()
    
    with app.app_context():
        # Проверяем, существует ли директория migrations
        migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
        
        # Удаляем существующую директорию миграций, если она есть
        if os.path.exists(migrations_dir):
            print(f"Удаление существующей директории миграций: {migrations_dir}")
            shutil.rmtree(migrations_dir)
            
        # Инициализируем новую структуру миграций
        print("Инициализация новой структуры миграций...")
        init()
        
        # Создаем первоначальную миграцию на основе моделей
        print("Создание первоначальной миграции...")
        migrate(message="initial migration")
        
        # Применяем миграцию к базе данных
        print("Применение миграции к базе данных...")
        upgrade()
        
        print("Миграции успешно инициализированы!")
        return True
    
if __name__ == "__main__":
    success = init_migrations()
    sys.exit(0 if success else 1)
