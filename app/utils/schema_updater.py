"""
Утилита для миграции схемы базы данных на лету.
Позволяет добавлять недостающие столбцы без использования миграций Alembic.
"""

from sqlalchemy import inspect, text
from sqlalchemy.exc import OperationalError, ProgrammingError
from app import db, create_app
from flask import current_app

def add_column_if_not_exists(table_name, column_name, column_type):
    """
    Добавляет столбец в таблицу, если он не существует
    
    :param table_name: Имя таблицы
    :param column_name: Имя столбца для добавления
    :param column_type: Тип данных столбца (например, 'VARCHAR(255)', 'INTEGER')
    :return: True если столбец добавлен, False если столбец уже существует
    """
    inspector = inspect(db.engine)
    columns = [c['name'] for c in inspector.get_columns(table_name)]
    
    if column_name not in columns:
        try:
            # PostgreSQL синтаксис
            query = text(f'ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {column_type}')
            db.session.execute(query)
            
            # Создаем индекс для column_name
            index_name = f'ix_{table_name}_{column_name}'
            index_query = text(f'CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column_name})')
            db.session.execute(index_query)
            
            db.session.commit()
            return True
        except (OperationalError, ProgrammingError) as e:
            db.session.rollback()
            current_app.logger.error(f"Failed to add column {column_name} to {table_name}: {e}")
            return False
    else:
        return False

def ensure_conversation_id_exists():
    """
    Убедиться, что столбец conversation_id существует в таблице chat_messages
    """
    app = create_app()
    with app.app_context():
        try:
            added = add_column_if_not_exists('chat_messages', 'conversation_id', 'VARCHAR(36)')
            if added:
                current_app.logger.info("Added conversation_id column to chat_messages table")
            else:
                current_app.logger.info("conversation_id column already exists in chat_messages table")
        except Exception as e:
            current_app.logger.error(f"Error checking/adding conversation_id column: {e}")

if __name__ == '__main__':
    ensure_conversation_id_exists()
