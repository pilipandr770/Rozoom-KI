#!/usr/bin/env python3
"""
init_postgres_schemas.py

Этот скрипт создает необходимые схемы PostgreSQL для проекта Rozoom-KI при деплое на Render.com.
Он запускается перед первым запуском приложения, чтобы гарантировать, что все необходимые схемы существуют.
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла (если он существует)
load_dotenv()

def init_postgres_schemas():
    """Инициализирует необходимые схемы PostgreSQL"""
    
    # Получаем строку подключения к базе данных из переменных окружения
    database_url = os.getenv('DATABASE_URL')
    
    if not database_url:
        print("ERROR: DATABASE_URL не найден в переменных окружения")
        sys.exit(1)
    
    # Исправляем URL для PostgreSQL, если он начинается с "postgres://" вместо "postgresql://"
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Add SSL parameters for PostgreSQL connections (required for Render.com)
    if 'postgresql://' in database_url:
        if '?' not in database_url:
            database_url += '?sslmode=require'
        else:
            database_url += '&sslmode=require'
    
    print(f"Подключение к базе данных...")
    
    # Создаем движок SQLAlchemy
    engine = create_engine(database_url)
    
    # Получаем имена схем из переменных окружения
    schemas = {
        'main': os.getenv('POSTGRES_SCHEMA', 'rozoom_ki_schema'),
        'clients': os.getenv('POSTGRES_SCHEMA_CLIENTS', 'rozoom_ki_clients'),
        'shop': os.getenv('POSTGRES_SCHEMA_SHOP', 'rozoom_ki_shop'),
        'projects': os.getenv('POSTGRES_SCHEMA_PROJECTS', 'rozoom_ki_projects')
    }
    
    # Создаем схемы, если они не существуют
    try:
        with engine.connect() as connection:
            for schema_name, schema_value in schemas.items():
                if schema_value:
                    print(f"Создание схемы '{schema_value}'...")
                    connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema_value}'))
                    print(f"Схема '{schema_value}' успешно создана или уже существует.")
        
        print("Все схемы успешно созданы!")
        return True
    except Exception as e:
        print(f"Ошибка при создании схем: {str(e)}")
        return False

if __name__ == "__main__":
    success = init_postgres_schemas()
    sys.exit(0 if success else 1)
