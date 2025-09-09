#!/usr/bin/env python3
"""
fix_duplicate_columns.py

Скрипт для исправления ошибок с дублирующимися столбцами.
Игнорирует ошибки DuplicateColumn при добавлении столбцов в таблицы.
"""

import os
import sys
import re
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def fix_duplicate_columns():
    """
    Исправляет проблемы с дублирующимися столбцами в базе данных
    путем проверки их существования перед добавлением
    """
    try:
        # Получаем строку подключения из переменных окружения
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            print("Ошибка: Переменная окружения DATABASE_URL не найдена")
            return False
        
        # Исправляем URL для PostgreSQL, если он начинается с "postgres://" вместо "postgresql://"
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        
        # Add SSL parameters for PostgreSQL connections (required for Render.com)
        if 'postgresql://' in database_url:
            if '?' not in database_url:
                database_url += '?sslmode=require'
            else:
                database_url += '&sslmode=require'
            
        # Создаем подключение к базе данных
        print("Подключение к базе данных...")
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Проверяем существование столбцов в таблице leads
            print("Проверка и исправление структуры таблицы leads...")
            
            # Получаем список существующих столбцов в таблице leads
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'leads'
            """))
            
            existing_columns = [row[0] for row in result]
            print(f"Существующие столбцы в таблице leads: {existing_columns}")
            
            # Проверяем и добавляем столбцы, только если они не существуют
            columns_to_check = [
                {"name": "data", "sql": "ALTER TABLE leads ADD COLUMN IF NOT EXISTS data TEXT"},
                {"name": "source", "sql": "ALTER TABLE leads ADD COLUMN IF NOT EXISTS source VARCHAR(100)"},
                {"name": "status", "sql": "ALTER TABLE leads ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'new'"}
            ]
            
            for column in columns_to_check:
                if column["name"] not in existing_columns:
                    print(f"Добавление столбца '{column['name']}' в таблицу leads...")
                    conn.execute(text(column["sql"]))
                else:
                    print(f"Столбец '{column['name']}' уже существует в таблице leads")
            
            print("Структура таблицы leads успешно исправлена")
            return True
            
    except Exception as e:
        print(f"Ошибка при исправлении структуры таблиц: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_duplicate_columns()
    sys.exit(0 if success else 1)
