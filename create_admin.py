#!/usr/bin/env python3
"""
Скрипт для создания или проверки админа
"""
import os
import sys

# Добавляем текущую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.auth import AdminUser
from app import db

def create_specific_admin():
    """Создание админа с указанными данными"""
    app = create_app()

    with app.app_context():
        try:
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

            print("✅ Админ успешно создан!")
            print(f"   Username: {admin.username}")
            print(f"   Email: {admin.email}")
            print(f"   ID: {admin.id}")
            return True

        except Exception as e:
            print(f"❌ Ошибка при создании админа: {e}")
            db.session.rollback()
            return False

def list_all_admins():
    """Показать всех админов"""
    app = create_app()

    with app.app_context():
        try:
            admins = AdminUser.query.all()
            if not admins:
                print("❌ Админов не найдено")
                return

            print("📋 Список всех админов:")
            for admin in admins:
                print(f"   ID: {admin.id}")
                print(f"   Username: {admin.username}")
                print(f"   Email: {admin.email}")
                print("   ---")

        except Exception as e:
            print(f"❌ Ошибка при получении списка админов: {e}")

if __name__ == '__main__':
    print("🔧 Скрипт управления админами")
    print("=" * 40)

    if len(sys.argv) > 1 and sys.argv[1] == 'list':
        list_all_admins()
    else:
        print("Создание админа с данными:")
        print("Email: pylypchukandrii770@gmail.com")
        print("Пароль: Dnepr75ok10")
        print("-" * 40)
        create_specific_admin()
