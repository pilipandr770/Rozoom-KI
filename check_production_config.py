#!/usr/bin/env python3
"""
Скрипт для проверки конфигурации OpenAI API в production
"""
import os
from dotenv import load_dotenv

def check_openai_config():
    """Проверяет наличие и корректность OpenAI API ключа"""
    load_dotenv()

    api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("❌ OPENAI_API_KEY не найден в переменных окружения")
        return False

    if len(api_key.strip()) == 0:
        print("❌ OPENAI_API_KEY пустой")
        return False

    if not api_key.startswith('sk-'):
        print("❌ OPENAI_API_KEY не начинается с 'sk-' (неправильный формат)")
        return False

    print("✅ OPENAI_API_KEY найден и имеет правильный формат")
    print(f"   Длина ключа: {len(api_key)} символов")

    return True

def check_database_config():
    """Проверяет конфигурацию базы данных"""
    load_dotenv()

    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("❌ DATABASE_URL не найден в переменных окружения")
        return False

    print("✅ DATABASE_URL найден")
    print(f"   URL: {database_url[:50]}...")

    # Проверяем SSL параметры
    if 'sslmode=require' in database_url:
        print("✅ SSL параметры настроены правильно")
    else:
        print("⚠️  SSL параметры могут быть не настроены")

    return True

if __name__ == "__main__":
    print("🔍 Проверка конфигурации production...\n")

    print("1. Проверка OpenAI API:")
    openai_ok = check_openai_config()

    print("\n2. Проверка базы данных:")
    db_ok = check_database_config()

    print("\n" + "="*50)
    if openai_ok and db_ok:
        print("✅ Все конфигурации корректны")
    else:
        print("❌ Найдены проблемы с конфигурацией")
