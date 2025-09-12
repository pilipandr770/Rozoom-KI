"""
Скрипт для пересоздания миграций в случае конфликтов
Использование:
    python recreate_migrations.py
"""
import os
import shutil
import subprocess
from pathlib import Path

def main():
    # Путь к директории с миграциями
    migrations_dir = Path("migrations/versions")
    
    # Проверяем существование директории
    if not migrations_dir.exists():
        print(f"Директория {migrations_dir} не существует")
        return
    
    # Создаем резервную копию директории
    backup_dir = Path("migrations/versions_backup")
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    
    shutil.copytree(migrations_dir, backup_dir)
    print(f"Создана резервная копия миграций в {backup_dir}")
    
    # Удаляем все файлы миграций, кроме пустых __init__.py
    for file in migrations_dir.glob("*.py"):
        if file.name != "__init__.py":
            os.remove(file)
    
    print("Удалены все файлы миграций")
    
    # Создаем новую миграцию
    try:
        subprocess.run(["flask", "db", "migrate", "-m", "recreate_all_tables"], check=True)
        print("Создана новая миграция")
        
        # Применяем миграцию
        subprocess.run(["flask", "db", "upgrade"], check=True)
        print("Миграция успешно применена")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при выполнении команд миграции: {e}")
        # Восстанавливаем из резервной копии
        shutil.rmtree(migrations_dir)
        shutil.copytree(backup_dir, migrations_dir)
        print("Восстановлена резервная копия миграций")

if __name__ == "__main__":
    main()
