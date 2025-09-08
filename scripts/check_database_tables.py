"""
Скрипт для проверки таблиц в базе данных
"""
import sys
import os
# Добавляем родительскую директорию в путь импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, create_app
from sqlalchemy import inspect

def check_database_tables():
    """Проверка таблиц в базе данных"""
    app = create_app()
    with app.app_context():
        try:
            # Получаем инспектор базы данных
            inspector = inspect(db.engine)
            
            # Получаем список всех таблиц
            tables = inspector.get_table_names()
            
            print(f"Найдено {len(tables)} таблиц в базе данных:")
            for i, table in enumerate(tables, 1):
                print(f"{i}. {table}")
                
            # Проверяем наличие таблицы chat_messages
            if 'chat_messages' in tables:
                print("\nТаблица chat_messages существует.")
                
                # Получаем структуру таблицы chat_messages
                columns = inspector.get_columns('chat_messages')
                
                print("\nСтруктура таблицы chat_messages:")
                for col in columns:
                    print(f"  - {col['name']} ({col['type']})")
            else:
                print("\nТаблица chat_messages отсутствует в базе данных!")
                
        except Exception as e:
            print(f"Ошибка при проверке таблиц: {e}")
            return

if __name__ == "__main__":
    check_database_tables()
