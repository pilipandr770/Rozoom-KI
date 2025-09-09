#!/usr/bin/env python3
"""
Тест функции load_user
"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

def test_load_user():
    """Тестирует функцию load_user"""
    from app import create_app
    from app.auth import load_user

    app = create_app()

    with app.app_context():
        # Тестируем загрузку пользователя с ID 1 (обычно admin)
        user = load_user(1)
        if user:
            print(f"✅ Пользователь найден: {user}")
            print(f"   Email: {getattr(user, 'email', 'N/A')}")
            print(f"   Is admin: {getattr(user, 'is_admin', 'N/A')}")
            print(f"   Type: {type(user).__name__}")
        else:
            print("❌ Пользователь не найден")

        # Тестируем загрузку несуществующего пользователя
        user_none = load_user(999)
        if user_none is None:
            print("✅ Несуществующий пользователь правильно возвращает None")
        else:
            print(f"❌ Несуществующий пользователь вернул: {user_none}")

if __name__ == "__main__":
    test_load_user()
