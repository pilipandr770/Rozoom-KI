#!/usr/bin/env python3
"""
setup_cascade_migrations.py

Скрипт для настройки миграций Alembic с поддержкой CASCADE для удаления таблиц.
Копирует модифицированный шаблон env.py в директорию миграций.
"""

import os
import sys
import shutil

def setup_cascade_migrations():
    """Настраивает миграции с поддержкой CASCADE"""
    try:
        # Путь к директории миграций
        migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'migrations')
        
        # Проверяем, существует ли директория миграций
        if not os.path.exists(migrations_dir):
            print(f"Директория миграций не найдена: {migrations_dir}")
            print("Сначала запустите flask db init для создания структуры миграций")
            return False
        
        # Путь к шаблону env.py
        template_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 
            'migration_templates', 
            'modified_env.py.template'
        )
        
        # Проверяем, существует ли шаблон
        if not os.path.exists(template_path):
            print(f"Шаблон env.py не найден: {template_path}")
            return False
        
        # Путь к файлу env.py
        env_py_path = os.path.join(migrations_dir, 'env.py')
        
        # Создаем резервную копию существующего env.py
        if os.path.exists(env_py_path):
            backup_path = env_py_path + '.bak'
            print(f"Создание резервной копии env.py: {backup_path}")
            shutil.copy2(env_py_path, backup_path)
        
        # Копируем шаблон в директорию миграций
        print(f"Копирование модифицированного env.py в {env_py_path}")
        shutil.copy2(template_path, env_py_path)
        
        print("Настройка миграций с поддержкой CASCADE успешно завершена")
        return True
    except Exception as e:
        print(f"Ошибка при настройке миграций с поддержкой CASCADE: {str(e)}")
        return False

if __name__ == "__main__":
    success = setup_cascade_migrations()
    sys.exit(0 if success else 1)
