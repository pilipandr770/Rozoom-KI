#!/usr/bin/env python3
"""
Скрипт для тестирования fallback системы OpenAI
"""
from app import create_app
from app.services.openai_service import OpenAIService
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_fallback_system():
    """Тестирует fallback систему генерации контента"""
    print("🔄 Тестирование fallback системы OpenAI...\n")

    app = create_app()

    with app.app_context():
        try:
            print("1. Создание OpenAI сервиса...")
            openai_service = OpenAIService()
            print("✅ OpenAI сервис создан")

            print("\n2. Тестирование fallback генерации...")
            result = openai_service.generate_blog_content_fallback(
                topic="Artificial Intelligence",
                keywords="AI, machine learning, automation",
                language="en"
            )

            if result and 'title' in result and 'content' in result:
                print("✅ Fallback генерация работает")
                print(f"   Заголовок: {result['title']}")
                print(f"   Длина контента: {len(result['content'])} символов")
                print(f"   Мета-описание: {result['meta_description'][:50]}...")
            else:
                print("❌ Fallback генерация вернула некорректный результат")

            print("\n3. Проверка переменной окружения OPENAI_FALLBACK_ENABLED...")
            import os
            fallback_enabled = os.getenv('OPENAI_FALLBACK_ENABLED', 'true').lower() in ('true', 'yes', '1')
            print(f"   Fallback режим: {'включен' if fallback_enabled else 'отключен'}")

        except Exception as e:
            print(f"❌ Ошибка при тестировании: {str(e)}")
            return False

    return True

if __name__ == "__main__":
    success = test_fallback_system()
    if success:
        print("\n🎉 Тестирование fallback системы завершено успешно!")
    else:
        print("\n💥 Тестирование fallback системы провалено!")
