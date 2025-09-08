"""
Простой скрипт для тестирования API чата
"""
import requests
import uuid
import json
from pprint import pprint

def test_chat_api():
    # Базовый URL для локального сервера Flask
    base_url = "http://127.0.0.1:5000"
    
    # Создаем уникальный conversation_id для теста
    conversation_id = str(uuid.uuid4())
    print(f"Сгенерирован новый conversation_id: {conversation_id}")
    
    # Заголовки для запроса
    headers = {
        'Content-Type': 'application/json',
        'Accept-Language': 'de'  # Тестируем немецкий язык по умолчанию
    }
    
    # Данные для запроса
    data = {
        'message': 'Привет! Расскажи, пожалуйста, о вашем сайте.',
        'metadata': {
            'conversation_id': conversation_id,
            'page': '/services',  # Имитируем запрос со страницы services
            'language': 'ru'      # Пользователь хочет общаться на русском
        }
    }
    
    # Печатаем данные запроса для отладки
    print("\nОтправляемые данные:")
    print(f"conversation_id: {data['metadata']['conversation_id']}")
    print(f"message: {data['message']}")
    print(f"page: {data['metadata']['page']}")
    print(f"language: {data['metadata']['language']}")
    
    # Отправляем запрос
    print("\nОтправляем запрос...")
    response = requests.post(f"{base_url}/api/chat", headers=headers, json=data)
    
    # Проверяем результат
    if response.status_code == 200:
        result = response.json()
        print("\nУспешный ответ:")
        pprint(result)
        
        # Показываем conversation_id для дальнейшего использования
        print(f"\nConversation ID: {result.get('conversation_id')}")
    else:
        print(f"Ошибка: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    test_chat_api()
