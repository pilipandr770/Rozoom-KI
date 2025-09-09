#!/usr/bin/env python3
"""
init_migrations.py

Этот скрипт инициализирует миграции Flask-Migrate с нуля для чистой установки на Render.com.
Используйте этот скрипт, если при выполнении миграций возникают ошибки, связанные с отсутствующими ревизиями.
Включает поддержку CASCADE для удаления таблиц.
"""

import os
import sys
import shutil
import subprocess
from flask_migrate import init, migrate, upgrade
from app import create_app, db
from sqlalchemy import text

def execute_sql_command(conn, sql):
    """Выполняет SQL команду"""
    try:
        conn.execute(text(sql))
        return True
    except Exception as e:
        print(f"Ошибка при выполнении SQL: {str(e)}")
        return False

def init_migrations():
    """Инициализирует миграции Flask-Migrate с нуля"""
    app = create_app()
    
    with app.app_context():
        try:
            # Проверяем, существует ли директория migrations
            migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
            
            # Удаляем существующую директорию миграций, если она есть
            if os.path.exists(migrations_dir):
                print(f"Удаление существующей директории миграций: {migrations_dir}")
                shutil.rmtree(migrations_dir)
                
            # Инициализируем новую структуру миграций
            print("Инициализация новой структуры миграций...")
            init()
            
            # Устанавливаем модифицированный env.py с поддержкой CASCADE
            print("Настройка поддержки CASCADE для миграций...")
            try:
                # Копируем модифицированный шаблон env.py напрямую
                template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                           'migration_templates', 'modified_env.py.template')
                env_path = os.path.join(migrations_dir, 'env.py')
                
                if os.path.exists(template_path):
                    shutil.copy2(template_path, env_path)
                    print(f"Модифицированный env.py успешно установлен: {env_path}")
                else:
                    print("Предупреждение: шаблон modified_env.py.template не найден")
            except Exception as e:
                print(f"Ошибка при установке modified_env.py: {str(e)}")
            
            # Создаем первоначальную миграцию на основе моделей
            print("Создание первоначальной миграции...")
            migrate(message="initial migration")
            
            # Применяем миграцию к базе данных
            print("Применение миграции к базе данных...")
            upgrade()
            
            print("Миграции успешно инициализированы!")
            return True
        except Exception as e:
            print(f"Ошибка при инициализации миграций: {str(e)}")
            return False
    
if __name__ == "__main__":
    success = init_migrations()
    sys.exit(0 if success else 1)
