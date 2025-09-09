#!/usr/bin/env python3
"""
simple_create_tables.py

Простой скрипт для создания таблиц напрямую через SQLAlchemy,
без использования миграций. Не требует прав superuser.
"""

import os
import sys
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from app import create_app

# Загружаем переменные окружения
load_dotenv()

def create_tables_directly():
    """Создает таблицы напрямую через SQLAlchemy"""
    app = create_app()
    
    try:
        with app.app_context():
            from app import db
            
            # Создаем все таблицы
            print("Создание таблиц напрямую через SQLAlchemy...")
            db.create_all()
            
            # Добавляем базовые данные (если нужно)
            print("Проверка и добавление базовых данных...")
            try:
                from app.models import User
                
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
                    print("Пользователь admin создан")
                else:
                    print("Пользователь admin уже существует")
            except Exception as e:
                print(f"Ошибка при создании базовых данных: {str(e)}")
                
            print("Таблицы успешно созданы!")
            return True
            
    except SQLAlchemyError as e:
        print(f"Ошибка при создании таблиц: {str(e)}")
        return False

if __name__ == "__main__":
    success = create_tables_directly()
    sys.exit(0 if success else 1)
