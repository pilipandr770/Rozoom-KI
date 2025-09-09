#!/usr/bin/env python3
"""
direct_db_init.py

Этот скрипт напрямую инициализирует базу данных, минуя систему миграций.
Скрипт создает все необходимые таблицы и базового пользователя администратора.
Используется как часть развертывания на Render.com при проблемах с миграциями.
"""

import os
import sys
from sqlalchemy.exc import SQLAlchemyError
from app import create_app, db
from app.models import User

def initialize_database():
    """
    Напрямую инициализирует базу данных, создавая все таблицы
    и добавляя базового пользователя администратора
    """
    app = create_app()
    
    with app.app_context():
        try:
            print("Проверка подключения к базе данных...")
            db.engine.execute("SELECT 1")
            print("Подключение к базе данных успешно")
            
            print("Удаление существующих таблиц (если есть)...")
            try:
                db.drop_all()
                print("Существующие таблицы успешно удалены")
            except Exception as e:
                print(f"Ошибка при удалении существующих таблиц: {str(e)}")
                print("Продолжаем работу...")
            
            print("Создание всех таблиц...")
            db.create_all()
            
            print("Добавление базового пользователя администратора...")
            # Проверяем наличие админа
            admin = User.query.filter_by(username='admin').first()
            if not admin:
                print("Создание пользователя admin...")
                admin = User(
                    username='admin',
                    email='admin@example.com',
                    is_admin=True
                )
                admin.set_password('admin')  # В реальном проекте использовать безопасный пароль
                db.session.add(admin)
                db.session.commit()
                print("Пользователь admin успешно создан")
            else:
                print("Пользователь admin уже существует")
                
            print("База данных успешно инициализирована!")
            return True
            
        except SQLAlchemyError as e:
            print(f"Ошибка при инициализации базы данных: {str(e)}")
            return False
        except Exception as e:
            print(f"Неожиданная ошибка: {str(e)}")
            return False

if __name__ == "__main__":
    success = initialize_database()
    sys.exit(0 if success else 1)
