#!/usr/bin/env python3
"""
Проверка состояния базы данных в production
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect

# Загрузка переменных окружения
load_dotenv()

def check_database_status():
    """Проверяет состояние базы данных"""

    # Получаем URL базы данных
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ Переменная DATABASE_URL не найдена")
        return False

    # Исправляем URL для PostgreSQL
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)

    # Добавляем SSL параметры
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
            print("✅ Подключение к базе данных успешно")

            # Проверяем таблицы
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"📋 Найденные таблицы: {tables}")

            # Проверяем таблицу users
            if 'users' in tables:
                columns = [col['name'] for col in inspector.get_columns('users')]
                print(f"📋 Столбцы таблицы users: {columns}")

                # Проверяем наличие is_admin
                if 'is_admin' in columns:
                    print("✅ Столбец is_admin найден в таблице users")
                else:
                    print("❌ Столбец is_admin НЕ найден в таблице users")

                # Считаем пользователей
                result = conn.execute(text("SELECT COUNT(*) FROM users"))
                count = result.scalar()
                print(f"👥 Всего пользователей: {count}")

            # Проверяем таблицу admin_users
            if 'admin_users' in tables:
                columns = [col['name'] for col in inspector.get_columns('admin_users')]
                print(f"📋 Столбцы таблицы admin_users: {columns}")

                # Проверяем наличие is_admin
                if 'is_admin' in columns:
                    print("✅ Столбец is_admin найден в таблице admin_users")
                else:
                    print("❌ Столбец is_admin НЕ найден в таблице admin_users")

                # Считаем админов
                result = conn.execute(text("SELECT COUNT(*) FROM admin_users"))
                count = result.scalar()
                print(f"👑 Всего админов: {count}")

            return True

    except Exception as e:
        print(f"❌ Ошибка при проверке базы данных: {str(e)}")
        return False

if __name__ == "__main__":
    success = check_database_status()
    if success:
        print("\n🎉 Проверка базы данных завершена успешно!")
    else:
        print("\n❌ Проверка базы данных провалена.")
