#!/usr/bin/env python3
"""
fix_app_database.py

Скрипт для исправления ошибки KeyError: <Flask 'app'> в app.database.py
Создает патч для app/database.py, который исправляет проблему с движком базы данных
"""

import os
import sys
import re

def fix_app_database():
    """
    Исправляет ошибку в app/database.py, связанную с
    использованием устаревшего метода db.get_engine(app)
    """
    try:
        # Путь к файлу database.py
        database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app', 'database.py')
        
        if not os.path.exists(database_path):
            print(f"Файл database.py не найден по пути: {database_path}")
            return False
            
        # Читаем содержимое файла
        with open(database_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Паттерн для поиска устаревшего метода
        old_pattern = r"engine\s*=\s*db\.get_engine\(app\)"
        
        # Замена на новый метод
        new_code = "engine = db.session.get_bind()"
        
        # Выполняем замену
        if re.search(old_pattern, content):
            updated_content = re.sub(old_pattern, new_code, content)
            
            # Сохраняем обновленный файл
            with open(database_path, 'w', encoding='utf-8') as f:
                f.write(updated_content)
                
            print("Файл app/database.py успешно исправлен")
            return True
        else:
            print("Шаблон для замены не найден в файле database.py")
            return False
            
    except Exception as e:
        print(f"Ошибка при исправлении файла database.py: {str(e)}")
        return False

if __name__ == "__main__":
    success = fix_app_database()
    sys.exit(0 if success else 1)
