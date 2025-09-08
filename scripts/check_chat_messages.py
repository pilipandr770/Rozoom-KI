"""
Скрипт для проверки сохраненных сообщений чата в базе данных
"""
import sys
import os
# Добавляем родительскую директорию в путь импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, create_app
from app.models.base import ChatMessage
from datetime import datetime, timedelta
import sys

def check_chat_messages():
    """Проверка сохраненных сообщений чата с timestamp"""
    app = create_app()
    with app.app_context():
        try:
            # Получаем все сообщения, сортируем по времени создания
            recent_messages = ChatMessage.query.order_by(
                ChatMessage.timestamp.desc()
            ).limit(20).all()  # Получаем последние 20 сообщений
            
            if not recent_messages:
                print("Не найдено сообщений чата в базе данных.")
                return
            
            print(f"Найдено {len(recent_messages)} последних сообщений:")
            print("-" * 80)
            
            for i, msg in enumerate(recent_messages, 1):
                print(f"[{i}] Сообщение ID: {msg.id}")
                print(f"    Роль: {msg.role}")
                print(f"    Timestamp: {msg.timestamp}")
                print(f"    Conversation ID: {msg.conversation_id}")
                content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                print(f"    Содержание: {content_preview}")
                print("-" * 80)
                
        except Exception as e:
            print(f"Ошибка при проверке сообщений чата: {e}")
            return

if __name__ == "__main__":
    check_chat_messages()
