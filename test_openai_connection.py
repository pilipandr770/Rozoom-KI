#!/usr/bin/env python3
"""
Тест для проверки генерации контента с улучшенной обработкой ошибок
"""
from app import create_app
from app.services.openai_service import OpenAIService
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_openai_connection():
    """Тестирует подключение к OpenAI API"""
    app = create_app()

    with app.app_context():
        try:
            print("🔍 Тестируем подключение к OpenAI API...")

            # Создаем сервис
            openai_service = OpenAIService()
            print("✅ OpenAI сервис инициализирован")

            # Тестируем генерацию контента
            print("📝 Тестируем генерацию контента...")
            result = openai_service.generate_blog_content(
                topic="Test AI Technology",
                keywords="AI, machine learning, automation",
                language="en"
            )

            if result and 'title' in result and 'content' in result:
                print("✅ Контент успешно сгенерирован")
                print(f"   Заголовок: {result['title'][:50]}...")
                print(f"   Длина контента: {len(result['content'])} символов")
            else:
                print("❌ Контент не сгенерирован или имеет неправильный формат")

        except Exception as e:
            print(f"❌ Ошибка при тестировании: {str(e)}")
            return False

    return True

if __name__ == "__main__":
    success = test_openai_connection()
    if success:
        print("\n🎉 Тест пройден успешно!")
    else:
        print("\n💥 Тест провален!")
