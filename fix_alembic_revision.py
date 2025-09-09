#!/usr/bin/env python3
"""
fix_alembic_revision.py

Скрипт для исправления проблемы с ошибкой "Не удается найти ревизию, идентифицированную как 'ac4cda9e7cef'"
путем создания пустой ревизии с указанным идентификатором.

Этот подход альтернативен удалению записи из alembic_version и может быть полезен, 
если вы хотите сохранить историю миграций.
"""

import os
import sys
from flask_migrate import init, migrate, upgrade, current, revision
from app import create_app, db

PROBLEMATIC_REVISION = 'ac4cda9e7cef'

def fix_missing_revision():
    """Создает пустую ревизию с указанным ID"""
    app = create_app()
    
    with app.app_context():
        from alembic.config import Config
        from alembic import command
        from alembic.script import ScriptDirectory
        from alembic.util.exc import CommandError
        
        print(f"Проверка наличия проблемной ревизии '{PROBLEMATIC_REVISION}'...")
        
        # Проверяем текущую ревизию
        try:
            result = current()
            current_rev = result.split(' ')[0] if result else None
            print(f"Текущая ревизия: {current_rev}")
            
            if current_rev == PROBLEMATIC_REVISION:
                print(f"Обнаружена проблемная ревизия '{PROBLEMATIC_REVISION}' в базе данных")
            
                # Получаем доступ к директории скриптов миграций
                alembic_cfg = Config("migrations/alembic.ini")
                script_dir = ScriptDirectory.from_config(alembic_cfg)
                
                try:
                    # Проверяем, существует ли ревизия с таким ID
                    script = script_dir.get_revision(PROBLEMATIC_REVISION)
                    print(f"Ревизия '{PROBLEMATIC_REVISION}' уже существует в файловой системе: {script.path}")
                    return True
                except Exception:
                    # Ревизия не найдена, создаем ее
                    print(f"Ревизия '{PROBLEMATIC_REVISION}' не найдена в файловой системе. Создаем пустую ревизию...")
                    
                    try:
                        # Создаем пустую ревизию с указанным идентификатором
                        revision(message="empty revision to fix migration issue", rev_id=PROBLEMATIC_REVISION)
                        print(f"Создана пустая ревизия с ID '{PROBLEMATIC_REVISION}'")
                        return True
                    except CommandError as e:
                        print(f"Ошибка при создании пустой ревизии: {str(e)}")
                        return False
        except Exception as e:
            print(f"Ошибка при проверке текущей ревизии: {str(e)}")
            return False
            
        # Если текущая ревизия не проблемная, то ничего не делаем
        print("Проблемная ревизия не обнаружена в базе данных")
        return True

if __name__ == "__main__":
    success = fix_missing_revision()
    sys.exit(0 if success else 1)
