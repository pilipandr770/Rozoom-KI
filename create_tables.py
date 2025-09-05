"""
Скрипт для создания таблиц базы данных напрямую через SQLAlchemy,
без использования Flask-Migrate
"""
import os
import sys
from pathlib import Path

# Добавляем корневой каталог проекта в sys.path
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))

from app import create_app, db
from app.models import *  # Импортируем все модели

def create_tables():
    """Создает все таблицы в базе данных"""
    app = create_app()
    
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        print("Таблицы успешно созданы.")

if __name__ == "__main__":
    create_tables()
