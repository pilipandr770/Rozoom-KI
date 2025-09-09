#!/usr/bin/env python3
"""
Скрипт для создания админа на Render
Запускать на сервере после развертывания
"""
import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_admin_on_render():
    """Создание админа на Render"""
    try:
        from app import create_app
        from app.auth import AdminUser
        from app import db

        app = create_app()

        with app.app_context():
            # Проверяем, существует ли уже админ с таким email
            existing_admin = AdminUser.query.filter_by(email='pylypchukandrii770@gmail.com').first()

            if existing_admin:
                print(f"✅ Админ с email pylypchukandrii770@gmail.com уже существует!")
                print(f"   Username: {existing_admin.username}")
                print(f"   ID: {existing_admin.id}")
                return True

            # Создаем нового админа
            admin = AdminUser(
                username='pylypchukandrii770',
                email='pylypchukandrii770@gmail.com'
            )
            admin.set_password('Dnepr75ok10')

            db.session.add(admin)
            db.session.commit()

            print("✅ Админ успешно создан на Render!")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   ID: {admin.id}")
            print("\n🔐 Данные для входа:")
            print(f"   Email: pylypchukandrii770@gmail.com")
            print(f"   Пароль: Dnepr75ok10")
            return True

    except Exception as e:
        print(f"❌ Ошибка при создании админа: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Создание админа на Render")
    print("=" * 40)
    print("Email: pylypchukandrii770@gmail.com")
    print("Пароль: Dnepr75ok10")
    print("-" * 40)

    success = create_admin_on_render()

    if success:
        print("\n🎉 Готово! Теперь вы можете войти в админ-панель.")
    else:
        print("\n❌ Произошла ошибка. Проверьте логи приложения.")
