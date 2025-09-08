"""
Скрипт для добавления столбца timestamp в таблицу chat_messages
"""
from sqlalchemy import inspect, text
from app import db, create_app

def add_timestamp_to_chat_messages():
    """
    Добавляет столбец timestamp в таблицу chat_messages, если его еще нет
    """
    app = create_app()
    with app.app_context():
        engine = db.get_engine(app)
        inspector = inspect(engine)
        
        if 'chat_messages' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('chat_messages')]
            
            if 'timestamp' not in columns:
                try:
                    with engine.begin() as conn:
                        # Добавляем столбец timestamp
                        conn.execute(text("ALTER TABLE chat_messages ADD COLUMN timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
                        
                        # Создаем индекс для timestamp
                        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_chat_messages_timestamp ON chat_messages (timestamp)"))
                        
                        print("Успешно добавлен столбец timestamp в таблицу chat_messages")
                except Exception as e:
                    print(f"Ошибка при добавлении столбца timestamp: {e}")
            else:
                print("Столбец timestamp уже существует в таблице chat_messages")
        else:
            print("Таблица chat_messages не найдена")

if __name__ == "__main__":
    add_timestamp_to_chat_messages()
