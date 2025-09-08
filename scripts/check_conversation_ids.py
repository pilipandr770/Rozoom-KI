"""
Скрипт для проверки всех уникальных conversation_id в базе данных
"""
import sys
import os
# Добавляем родительскую директорию в путь импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, create_app
from app.models.base import ChatMessage
from sqlalchemy import distinct

def check_conversation_ids():
    """Проверка всех уникальных conversation_id в базе данных"""
    app = create_app()
    with app.app_context():
        try:
            # Получаем все сообщения
            all_messages = ChatMessage.query.all()
            
            if not all_messages:
                print("В базе данных нет сообщений.")
                return
            
            print(f"Всего найдено {len(all_messages)} сообщений в базе данных.")
            
            # Собираем уникальные conversation_id
            unique_conv_ids = set()
            for msg in all_messages:
                if msg.conversation_id:
                    unique_conv_ids.add(msg.conversation_id)
            
            print(f"Найдено {len(unique_conv_ids)} уникальных conversation_id:")
            
            # Перечисляем все сообщения
            print("\nСписок всех сообщений:")
            print("-" * 80)
            
            for i, msg in enumerate(all_messages, 1):
                print(f"[{i}] ID: {msg.id}")
                print(f"    Роль: {msg.role}")
                print(f"    Conversation ID: {msg.conversation_id}")
                print(f"    Timestamp: {msg.timestamp}")
                content_preview = msg.content[:50] + "..." if len(msg.content) > 50 else msg.content
                print(f"    Содержание: {content_preview}")
                print("-" * 80)
                
        except Exception as e:
            print(f"Ошибка при проверке conversation_ids: {e}")
            return

if __name__ == "__main__":
    check_conversation_ids()
