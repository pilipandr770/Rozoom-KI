#!/usr/bin/env python3
"""
Скрипт для диагностики проблем с OpenAI API в production
"""
import os
import logging
from app import create_app
from app.services.openai_service import OpenAIService

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def diagnose_openai_issues():
    """Диагностика проблем с OpenAI API"""
    print("🔍 Диагностика проблем с OpenAI API...\n")

    app = create_app()

    with app.app_context():
        try:
            # 1. Проверяем конфигурацию
            print("1. Проверка конфигурации:")
            api_key = app.config.get('OPENAI_API_KEY')
            if not api_key:
                print("❌ OPENAI_API_KEY не найден в конфигурации")
                return

            print(f"✅ OPENAI_API_KEY найден (длина: {len(api_key)})")
            print(f"   Начинается с: {api_key[:10]}...")

            # 2. Создаем сервис
            print("\n2. Создание OpenAI сервиса:")
            try:
                openai_service = OpenAIService()
                print("✅ OpenAI сервис создан успешно")
            except Exception as e:
                print(f"❌ Ошибка создания сервиса: {str(e)}")
                return

            # 3. Тестируем подключение
            print("\n3. Тест подключения:")
            connection_ok = openai_service.test_connection()
            if connection_ok:
                print("✅ Подключение к OpenAI API работает")
            else:
                print("❌ Подключение к OpenAI API не работает")
                return

            # 4. Тестируем генерацию с минимальными данными
            print("\n4. Тест генерации контента:")
            try:
                result = openai_service.generate_blog_content(
                    topic="Test",
                    keywords="test",
                    language="en"
                )
                if result and 'title' in result:
                    print("✅ Генерация контента работает")
                    print(f"   Заголовок: {result['title'][:50]}...")
                else:
                    print("❌ Генерация контента вернула некорректный результат")
            except Exception as e:
                print(f"❌ Ошибка генерации контента: {str(e)}")

        except Exception as e:
            print(f"❌ Неожиданная ошибка: {str(e)}")

if __name__ == "__main__":
    diagnose_openai_issues()
