#!/usr/bin/env python3
"""
Тест подключения к базе данных с SSL
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Загрузка переменных окружения
load_dotenv()

def test_database_connection():
    """Тестирует подключение к базе данных с SSL"""

    # Получаем URL базы данных
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Переменная DATABASE_URL не найдена")
        return False

    print(f"Оригинальный URL: {database_url}")

    # Исправляем URL для PostgreSQL
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    # Добавляем SSL параметры
    if 'postgresql://' in database_url:
        if '?' not in database_url:
            database_url += '?sslmode=require'
        else:
            database_url += '&sslmode=require'

    print(f"Исправленный URL: {database_url}")

    try:
        # Создаем движок SQLAlchemy
        engine = create_engine(database_url, echo=True)

        with engine.connect() as conn:
            # Простой тест подключения
            result = conn.execute(text("SELECT 1 as test"))
            row = result.fetchone()
            print(f"✅ Подключение успешно! Результат теста: {row[0]}")

            # Тест запроса пользователя
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            print(f"✅ Найдено пользователей: {count}")

            return True

    except Exception as e:
        print(f"❌ Ошибка подключения: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_database_connection()
    if success:
        print("\n🎉 Тест подключения прошел успешно!")
    else:
        print("\n❌ Тест подключения провален.")
