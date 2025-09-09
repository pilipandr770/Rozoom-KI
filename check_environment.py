#!/usr/bin/env python3
"""
Скрипт для проверки переменных окружения в production
"""
import os
import logging
from app import create_app

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment_variables():
    """Проверяет критически важные переменные окружения"""
    print("🔍 Проверка переменных окружения...\n")

    app = create_app()

    with app.app_context():
        print("1. Переменные окружения Flask:")
        print(f"   FLASK_ENV: {os.getenv('FLASK_ENV', 'не установлена')}")
        print(f"   FLASK_APP: {os.getenv('FLASK_APP', 'не установлена')}")

        print("\n2. Переменные базы данных:")
        database_url = os.getenv('DATABASE_URL', 'не установлена')
        if database_url != 'не установлена':
            print(f"   DATABASE_URL: {database_url[:50]}...")
            print(f"   Содержит sslmode: {'sslmode' in database_url}")
        else:
            print("   DATABASE_URL: не установлена")

        print("\n3. Переменные OpenAI:")
        openai_key = os.getenv('OPENAI_API_KEY', 'не установлена')
        if openai_key != 'не установлена':
            print(f"   OPENAI_API_KEY: установлена (длина: {len(openai_key)})")
            print(f"   Начинается с 'sk-': {openai_key.startswith('sk-')}")
            print(f"   Формат: {'sk-proj-' if openai_key.startswith('sk-proj-') else 'sk-' if openai_key.startswith('sk-') else 'неизвестный'}")
        else:
            print("   OPENAI_API_KEY: не установлена")

        print("\n4. Переменные почты:")
        mail_vars = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USERNAME', 'MAIL_PASSWORD']
        for var in mail_vars:
            value = os.getenv(var, 'не установлена')
            if value != 'не установлена':
                print(f"   {var}: установлена")
            else:
                print(f"   {var}: не установлена")

        print("\n5. Конфигурация приложения:")
        print(f"   SECRET_KEY: {'установлен' if app.config.get('SECRET_KEY') else 'не установлен'}")
        print(f"   SQLALCHEMY_DATABASE_URI: {'установлен' if app.config.get('SQLALCHEMY_DATABASE_URI') else 'не установлен'}")
        print(f"   OPENAI_API_KEY (из app.config): {'установлен' if app.config.get('OPENAI_API_KEY') else 'не установлен'}")

        # Проверяем доступность OpenAI API ключа
        if app.config.get('OPENAI_API_KEY'):
            try:
                from app.services.openai_service import OpenAIService
                service = OpenAIService()
                success, message = service.test_connection()
                print(f"\n6. Тест OpenAI API: {'✅' if success else '❌'} {message}")
            except Exception as e:
                print(f"\n6. Тест OpenAI API: ❌ Ошибка при создании сервиса: {str(e)}")
        else:
            print("\n6. Тест OpenAI API: ❌ API ключ не доступен в приложении")

if __name__ == "__main__":
    check_environment_variables()
