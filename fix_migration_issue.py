#!/usr/bin/env python3
"""
fix_migration_issue.py

Этот скрипт исправляет проблему с ошибкой "Не удается найти ревизию, идентифицированную как 'ac4cda9e7cef'"
путем прямого взаимодействия с таблицей alembic_version.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def fix_migration_issue():
    """Исправляет проблему с миграцией, удаляя проблемную запись из alembic_version"""
    try:
        # Получаем строку подключения из переменных окружения
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            print("ОШИБКА: Переменная окружения DATABASE_URL не найдена")
            return False
        
        # Убеждаемся, что URL начинается с postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        print(f"Подключение к базе данных для исправления миграций...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            try:
                # Проверяем существование таблицы alembic_version
                result = conn.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'alembic_version')"))
                if not result.scalar():
                    print("Таблица alembic_version не найдена, создаем её...")
                    conn.execute(text("CREATE TABLE IF NOT EXISTS alembic_version (version_num VARCHAR(32) NOT NULL)"))
                    conn.commit()
                    print("Таблица alembic_version создана")
                else:
                    # Удаляем все записи из таблицы alembic_version
                    print("Очистка таблицы alembic_version...")
                    conn.execute(text("DELETE FROM alembic_version"))
                    conn.commit()
                    print("Таблица alembic_version очищена")
                    
                # Проверяем, что таблица пуста
                result = conn.execute(text("SELECT COUNT(*) FROM alembic_version"))
                count = result.scalar()
                if count == 0:
                    print("Таблица alembic_version успешно очищена!")
                else:
                    print(f"ВНИМАНИЕ: В таблице alembic_version остались {count} записей")
                    
            except Exception as e:
                print(f"Ошибка при работе с таблицей alembic_version: {str(e)}")
                print("Пробуем альтернативный способ - удаление таблицы alembic_version...")
                
                try:
                    conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
                    conn.commit()
                    print("Таблица alembic_version удалена")
                except Exception as e2:
                    print(f"Ошибка при удалении таблицы alembic_version: {str(e2)}")
                    return False
                
        print("Миграционная проблема исправлена!")
        return True
    
    except SQLAlchemyError as e:
        print(f"ОШИБКА при исправлении миграции: {e}")
        return False

if __name__ == "__main__":
    success = fix_migration_issue()
    sys.exit(0 if success else 1)
