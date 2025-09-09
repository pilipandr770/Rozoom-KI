#!/usr/bin/env python3
"""
Скрипт для создания таблиц в базе данных PostgreSQL
и автоматического переноса данных из SQLite (если указано)

Использует прямое выполнение SQL через SQLAlchemy для создания необходимых таблиц,
минуя систему миграций Flask-Migrate, чтобы избежать проблем с ревизиями.

Этот скрипт полезен при деплое на новый сервер или при переходе с SQLite на PostgreSQL.
"""

import os
import json
import sqlite3
import tempfile
import argparse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from app import create_app

# Загрузка переменных окружения
load_dotenv()

def create_tables():
    """Создаёт все таблицы напрямую через SQLAlchemy"""
    app = create_app()
    
    with app.app_context():
        from app import db
        
        # Создаём все таблицы на основе определённых моделей
        try:
            db.create_all()
            print("Таблицы базы данных успешно созданы.")
            return True
        except Exception as e:
            print(f"Ошибка при создании таблиц: {str(e)}")
            return False

def export_sqlite_data(sqlite_path):
    """Экспортирует данные из SQLite базы данных в JSON формат"""
    if not os.path.exists(sqlite_path):
        print(f"Файл SQLite базы данных не найден: {sqlite_path}")
        return None
    
    data = {}
    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    
    # Получаем список всех таблиц
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    
    # Экспортируем данные из каждой таблицы
    for table in tables:
        table_name = table[0]
        if table_name == 'alembic_version' or table_name == 'sqlite_sequence':
            continue
            
        rows = conn.execute(f"SELECT * FROM {table_name}").fetchall()
        data[table_name] = [dict(row) for row in rows]
        print(f"Экспортировано {len(data[table_name])} строк из таблицы {table_name}")
    
    conn.close()
    return data

def import_to_postgres(data):
    """Импортирует данные в PostgreSQL"""
    app = create_app()
    
    with app.app_context():
        from app import db
        
        # Получаем соединение с базой данных
        conn = db.engine.connect()
        
        try:
            for table_name, rows in data.items():
                if not rows:
                    continue
                    
                print(f"Импорт данных в таблицу {table_name}...")
                
                # Для каждой строки таблицы формируем SQL запрос для вставки
                for row in rows:
                    # Удаляем ключи с None значениями
                    row = {k: v for k, v in row.items() if v is not None}
                    
                    if not row:
                        continue
                        
                    columns = ", ".join(row.keys())
                    placeholders = ", ".join([f":{col}" for col in row.keys()])
                    
                    # Формируем запрос на вставку
                    query = text(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
                    
                    # Выполняем запрос с параметрами
                    conn.execute(query, row)
                
                print(f"Успешно импортировано {len(rows)} строк в таблицу {table_name}")
                
            # Фиксируем транзакцию
            conn.commit()
            print("Данные успешно импортированы в PostgreSQL.")
            return True
            
        except Exception as e:
            # Откатываем транзакцию в случае ошибки
            conn.rollback()
            print(f"Ошибка при импорте данных: {str(e)}")
            return False
        finally:
            # Закрываем соединение
            conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Создание таблиц в PostgreSQL и опциональная миграция данных из SQLite")
    parser.add_argument("--sqlite", help="Путь к файлу SQLite базы данных для миграции")
    args = parser.parse_args()
    
    # Создаем таблицы
    if create_tables():
        # Если указан путь к SQLite, мигрируем данные
        if args.sqlite:
            data = export_sqlite_data(args.sqlite)
            if data:
                import_to_postgres(data)
    
    print("Скрипт завершил работу.")
