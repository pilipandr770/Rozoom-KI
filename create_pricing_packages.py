import os
import sys
from flask import Flask
from app import create_app, db
from app.models import PricePackage

app = create_app()

def create_default_packages():
    with app.app_context():
        # Проверка, существует ли уже таблица и есть ли в ней записи
        if PricePackage.__table__.exists(db.engine) and PricePackage.query.first():
            print("Пакеты цен уже существуют, пропускаем создание стандартных пакетов.")
            return
            
        # Создаем стандартные пакеты цен
        packages = [
            PricePackage(
                name='Basic Package',
                hours=10,
                price_per_hour=100.0,
                description='Perfect for small projects and quick updates.',
                is_active=True
            ),
            PricePackage(
                name='Standard Package',
                hours=30,
                price_per_hour=80.0,
                description='Ideal for medium-sized projects and ongoing development.',
                is_active=True
            ),
            PricePackage(
                name='Premium Package',
                hours=100,
                price_per_hour=60.0,
                description='Best value for larger projects and long-term development.',
                is_active=True
            )
        ]
        
        # Добавляем пакеты в базу данных
        db.session.bulk_save_objects(packages)
        db.session.commit()
        
        print(f"Создано {len(packages)} стандартных пакетов цен.")

if __name__ == '__main__':
    with app.app_context():
        # Создаем таблицу, если она не существует
        db.create_all()
        
        # Создаем стандартные пакеты
        create_default_packages()
        
        print("Миграция успешно выполнена.")
