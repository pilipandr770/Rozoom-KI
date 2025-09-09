#!/usr/bin/env python3
"""
Тест создания расписания для AdminUser
"""
import os
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

def test_create_schedule_for_admin():
    """Тестирует создание расписания для AdminUser"""
    from app import create_app, db
    from app.auth import AdminUser
    from app.models import ContentSchedule, PublishFrequency, BlogCategory, User
    from datetime import datetime

    app = create_app()

    with app.app_context():
        # Создаем тестовую категорию, если её нет
        category = BlogCategory.query.first()
        if not category:
            category = BlogCategory(name="Test Category", slug="test-category")
            db.session.add(category)
            db.session.commit()

        # Создаем тестового AdminUser, если его нет
        admin_user = AdminUser.query.filter_by(email="test@example.com").first()
        if not admin_user:
            admin_user = AdminUser(username="testadmin", email="test@example.com")
            admin_user.set_password("password")
            db.session.add(admin_user)
            db.session.commit()

        print(f"AdminUser ID: {admin_user.id}, Email: {admin_user.email}")

        # Тестируем нашу исправленную логику
        # Проверяем, есть ли User с таким же email
        author = User.query.filter_by(email=admin_user.email).first()
        if not author:
            print("Создаем User на основе AdminUser...")
            # Создаем User на основе AdminUser
            author = User(
                email=admin_user.email,
                name=admin_user.username,
                is_admin=True
            )
            db.session.add(author)
            db.session.flush()
            print(f"Создан User с ID: {author.id}")
        else:
            print(f"Найден существующий User с ID: {author.id}")

        # Создаем расписание с правильным author_id
        schedule = ContentSchedule(
            name="Test Schedule",
            topic_area="Test topic",
            description="Test description",
            keywords="test, keywords",
            frequency=PublishFrequency.DAILY,
            category_id=category.id,
            author_id=author.id,  # Теперь используем правильный ID из таблицы users
            next_generation_date=datetime.utcnow()
        )

        try:
            db.session.add(schedule)
            db.session.commit()
            print("✅ Расписание успешно создано с правильным author_id")
            print(f"   Расписание ID: {schedule.id}")
            print(f"   Author ID: {schedule.author_id}")
            print(f"   Author Email: {schedule.author.email}")
        except Exception as e:
            print(f"❌ Ошибка при создании расписания: {str(e)}")

if __name__ == "__main__":
    test_create_schedule_for_admin()
