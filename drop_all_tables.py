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
        
        # Add SSL parameters for PostgreSQL connections (required for Render.com)
        if 'postgresql://' in database_url:
            if '?' not in database_url:
                database_url += '?sslmode=require'
            else:
                database_url += '&sslmode=require'
        
        print(f"Подключение к базе данных для удаления всех таблиц...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Метод альтернативный отключению ограничений - удаление таблиц в правильном порядке
            
            # Получаем список всех таблиц во всех схемах
            result = conn.execute(text("""
                SELECT table_schema, table_name 
                FROM information_schema.tables 
                WHERE table_schema NOT IN ('pg_catalog', 'information_schema') 
                AND table_type = 'BASE TABLE'
            """))
            
            tables = result.fetchall()
            print(f"Найдено {len(tables)} таблиц для анализа")
            
            # Получаем информацию о зависимостях таблиц (внешние ключи)
            result = conn.execute(text("""
                SELECT
                    tc.table_schema, 
                    tc.table_name, 
                    ccu.table_schema AS foreign_table_schema,
                    ccu.table_name AS foreign_table_name
                FROM 
                    information_schema.table_constraints AS tc 
                JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
            """))
            
            # Создаем структуру зависимостей
            dependencies = {}
            for table_schema, table_name, foreign_schema, foreign_table in result.fetchall():
                full_name = f'"{table_schema}"."{table_name}"'
                foreign_full_name = f'"{foreign_schema}"."{foreign_table}"'
                
                if full_name not in dependencies:
                    dependencies[full_name] = []
                
                dependencies[full_name].append(foreign_full_name)
                
            # Сначала пытаемся удалить alembic_version, если она существует
            try:
                print("Удаление таблицы alembic_version...")
                conn.execute(text("DROP TABLE IF EXISTS alembic_version CASCADE;"))
                print("Таблица alembic_version удалена")
            except Exception as e:
                print(f"Ошибка при удалении таблицы alembic_version: {str(e)}")
            
            # Сначала пытаемся удалить таблицы с опцией CASCADE
            for schema, table in tables:
                try:
                    # Формируем имя таблицы с указанием схемы
                    table_name = f'"{schema}"."{table}"'
                    print(f"Удаление таблицы {table_name} с CASCADE...")
                    conn.execute(text(f'DROP TABLE IF EXISTS {table_name} CASCADE;'))
                except Exception as e:
                    print(f"Ошибка при удалении таблицы {schema}.{table} с CASCADE: {str(e)}")
            
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
