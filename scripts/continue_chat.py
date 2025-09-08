"""
Скрипт для продолжения диалога с чатом с использованием существующего conversation_id
"""
import requests
import sys
import json
from pprint import pprint

def continue_chat_conversation(conversation_id, message):
    """Продолжить существующий диалог с чатом"""
    # Базовый URL для локального сервера Flask
    base_url = "http://127.0.0.1:5000"
    
    # Заголовки для запроса
    headers = {
        'Content-Type': 'application/json',
        'Accept-Language': 'de'
    }
    
    # Данные для запроса
    data = {
        'message': message,
        'metadata': {
            'conversation_id': conversation_id,
            'page': '/contact',  # Имитируем запрос с другой страницы
            'language': 'ru'     # Продолжаем общаться на русском
        }
    }
    
    # Отправляем запрос
    print(f"Продолжаем диалог (ID: {conversation_id})...")
    response = requests.post(f"{base_url}/api/chat", headers=headers, json=data)
    
    # Проверяем результат
    if response.status_code == 200:
        result = response.json()
        print("\nУспешный ответ:")
        pprint(result)
        
        # Показываем conversation_id для дальнейшего использования
        print(f"\nConversation ID: {result.get('conversation_id')}")
        return result
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)
        return None

if __name__ == "__main__":
    # Проверяем, передан ли conversation_id в аргументах командной строки
    if len(sys.argv) < 3:
        print("Использование: python continue_chat.py <conversation_id> <сообщение>")
        sys.exit(1)
    
    conversation_id = sys.argv[1]
    message = sys.argv[2]
    
    continue_chat_conversation(conversation_id, message)
