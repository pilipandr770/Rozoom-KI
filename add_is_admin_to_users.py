#!/usr/bin/env python3
"""
Скрипт для добавления столбца is_admin в таблицу users (если отсутствует)
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Загрузка переменных окружения
load_dotenv()

def add_is_admin_to_users():
    """Добавляет столбец is_admin в таблицу users"""

    # Получаем URL базы данных
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Переменная DATABASE_URL не найдена")
        return False

    # Добавляем SSL параметры для PostgreSQL
    if 'postgresql://' in database_url:
        if '?' not in database_url:
            database_url += '?sslmode=require'
        else:
            database_url += '&sslmode=require'

    print("Подключение к базе данных...")

    try:
        # Создаем движок SQLAlchemy
        engine = create_engine(database_url)

        with engine.connect() as conn:
            # Проверяем, существует ли столбец is_admin в таблице users
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns
                    WHERE table_name = 'users'
                    AND column_name = 'is_admin'
                )
            """))

            if result.scalar():
                print("✅ Столбец is_admin уже существует в таблице users")
                return True

            # Добавляем столбец is_admin
            print("Добавление столбца is_admin в таблицу users...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN is_admin BOOLEAN DEFAULT FALSE
            """))

            conn.commit()
            print("✅ Столбец is_admin успешно добавлен в таблицу users")
            return True

    except Exception as e:
        print(f"❌ Ошибка при добавлении столбца: {str(e)}")
        return False

if __name__ == "__main__":
    success = add_is_admin_to_users()
    if success:
        print("\n🎉 Скрипт выполнен успешно!")
    else:
        print("\n❌ Скрипт выполнен с ошибками.")
