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
        # Сначала отключаем ограничения внешних ключей для всей сессии
        engine = db.engine
        with engine.connect() as conn:
            execute_sql_command(conn, "SET session_replication_role = 'replica';")
            print("Ограничения внешних ключей временно отключены")
            
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
                setup_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'setup_cascade_migrations.py')
                if os.path.exists(setup_script):
                    subprocess.run([sys.executable, setup_script], check=True)
                else:
                    print("Предупреждение: скрипт setup_cascade_migrations.py не найден")
                
                # Создаем первоначальную миграцию на основе моделей
                print("Создание первоначальной миграции...")
                migrate(message="initial migration")
                
                # Применяем миграцию к базе данных
                print("Применение миграции к базе данных...")
                upgrade()
                
                print("Миграции успешно инициализированы!")
                return True
            finally:
                # Возвращаем ограничения внешних ключей
                execute_sql_command(conn, "SET session_replication_role = 'origin';")
                print("Ограничения внешних ключей восстановлены")
    
if __name__ == "__main__":
    success = init_migrations()
    sys.exit(0 if success else 1)
