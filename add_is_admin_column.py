#!/usr/bin/env python3
"""
Скрипт для добавления столбца is_admin в таблицу admin_users
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Загрузка переменных окружения
load_dotenv()

def add_is_admin_column():
    """Добавляет столбец is_admin в таблицу admin_users"""

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
            # Проверяем, существует ли столбец is_admin в таблице admin_users
            result = conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns
                    WHERE table_name = 'admin_users'
                    AND column_name = 'is_admin'
                )
            """))

            if result.scalar():
                print("✅ Столбец is_admin уже существует в таблице admin_users")
                return True

            # Добавляем столбец is_admin
            print("Добавление столбца is_admin в таблицу admin_users...")
            conn.execute(text("""
                ALTER TABLE admin_users
                ADD COLUMN is_admin BOOLEAN DEFAULT TRUE
            """))

            # Обновляем существующие записи, устанавливая is_admin = TRUE
            conn.execute(text("""
                UPDATE admin_users
                SET is_admin = TRUE
                WHERE is_admin IS NULL
            """))

            conn.commit()
            print("✅ Столбец is_admin успешно добавлен в таблицу admin_users")
            return True

    except Exception as e:
        print(f"❌ Ошибка при добавлении столбца: {str(e)}")
        return False

if __name__ == "__main__":
    success = add_is_admin_column()
    if success:
        print("\n🎉 Скрипт выполнен успешно!")
        print("Теперь попробуйте войти в админ-панель с вашими учетными данными.")
    else:
        print("\n❌ Скрипт выполнен с ошибками.")
