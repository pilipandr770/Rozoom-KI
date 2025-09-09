#!/usr/bin/env python3
"""
drop_all_tables.py

Скрипт для безопасного удаления всех таблиц в базе данных,
включая зависимые таблицы (CASCADE). Используется для исправления проблем миграций
при деплое на Render.com.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def drop_all_tables_with_cascade():
    """Удаляет все таблицы в базе данных с CASCADE"""
    try:
        # Получаем строку подключения из переменных окружения
        database_url = os.environ.get('DATABASE_URL')
        
        if not database_url:
            print("ОШИБКА: Переменная окружения DATABASE_URL не найдена")
            return False
        
        # Убеждаемся, что URL начинается с postgresql://
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        print(f"Подключение к базе данных для удаления всех таблиц...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Отключаем ограничения внешних ключей временно
            conn.execute(text("SET session_replication_role = 'replica';"))
            
            # Получаем список всех таблиц во всех схемах
            result = conn.execute(text("""
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema') 
                AND table_type = 'BASE TABLE'
            """))
            
            tables = result.fetchall()
            print(f"Найдено {len(tables)} таблиц для удаления")
            
            # Удаляем таблицы
            for schema, table in tables:
                try:
                    # Формируем имя таблицы с указанием схемы
                    table_name = f'"{schema}"."{table}"'
                    print(f"Удаление таблицы {table_name}...")
                    conn.execute(text(f'DROP TABLE IF EXISTS {table_name} CASCADE;'))
                except Exception as e:
                    print(f"Ошибка при удалении таблицы {schema}.{table}: {str(e)}")
            
            # Удаляем таблицу alembic_version
            try:
                print("Удаление таблицы alembic_version...")
                conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
                print("Таблица alembic_version удалена")
            except Exception as e:
                print(f"Ошибка при удалении таблицы alembic_version: {str(e)}")
            
            # Возвращаем ограничения внешних ключей
            conn.execute(text("SET session_replication_role = 'origin';"))
            
            # Фиксируем изменения
            conn.commit()
                
        print("Все таблицы успешно удалены!")
        return True
    
    except SQLAlchemyError as e:
        print(f"ОШИБКА при удалении таблиц: {e}")
        return False

if __name__ == "__main__":
    success = drop_all_tables_with_cascade()
    sys.exit(0 if success else 1)
