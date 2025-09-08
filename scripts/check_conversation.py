"""
Скрипт для проверки сообщений с указанным conversation_id
"""
import sys
import os
# Добавляем родительскую директорию в путь импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import db, create_app
from app.models.base import ChatMessage

def check_conversation_messages(conversation_id):
    """Проверка сообщений с указанным conversation_id"""
    app = create_app()
    with app.app_context():
        try:
            # Получаем сообщения по conversation_id
            messages = ChatMessage.query.filter_by(
                conversation_id=conversation_id
            ).order_by(ChatMessage.timestamp).all()
            
            if not messages:
                print(f"Не найдено сообщений с conversation_id: {conversation_id}")
                return
            
            print(f"Найдено {len(messages)} сообщений с conversation_id: {conversation_id}")
            print("-" * 80)
            
            for i, msg in enumerate(messages, 1):
                print(f"[{i}] Сообщение ID: {msg.id}")
                print(f"    Роль: {msg.role}")
                print(f"    Timestamp: {msg.timestamp}")
                content_preview = msg.content[:100] + "..." if len(msg.content) > 100 else msg.content
                print(f"    Содержание: {content_preview}")
                print("-" * 80)
                
        except Exception as e:
            print(f"Ошибка при проверке сообщений: {e}")
            return

if __name__ == "__main__":
    # Проверяем, передан ли conversation_id в аргументах командной строки
    if len(sys.argv) < 2:
        print("Использование: python check_conversation.py <conversation_id>")
        sys.exit(1)
    
    conversation_id = sys.argv[1]
    check_conversation_messages(conversation_id)
