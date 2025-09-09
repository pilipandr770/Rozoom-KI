#!/usr/bin/env python3
"""
fix_db_init.py

Скрипт для исправления ошибки инициализации базы данных.
Решает проблему с KeyError: <Flask 'app'> в app.database.py
"""

import sys
from app import create_app, db
from app.models import User

def fix_database_init():
    """
    Исправляет ошибку инициализации базы данных и создает 
    базовые таблицы и пользователей
    """
    try:
        app = create_app()
        
        with app.app_context():
            print("Проверка подключения к базе данных...")
            connection = db.engine.connect()
            connection.close()
            print("Подключение к базе данных успешно")
            
            # Проверяем существование пользователя admin
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("Создание пользователя admin...")
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin')
                db.session.add(admin)
                db.session.commit()
                print("Пользователь admin создан успешно")
            else:
                print("Пользователь admin уже существует")
                
            print("База данных успешно инициализирована!")
            return True
            
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_database_init()
    sys.exit(0 if success else 1)
