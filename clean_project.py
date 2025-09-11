#!/usr/bin/env python3
"""
Скрипт для безопасной очистки проекта от ненужных файлов разработки.
Запускайте с осторожностью и проверяйте список файлов перед удалением.
"""

import os
import shutil
from pathlib import Path

def get_files_to_delete():
    """Возвращает список файлов для удаления, сгруппированных по категориям"""

    files_to_delete = {
        "Тестовые файлы в корне": [
            "test_auto_content.py",
            "test_db_connection.py",
            "test_deployment_locally.py",
            "test_email_notification.py",
            "test_enhanced_tech_spec.py",
            "test_fallback.py",
            "test_fully_detailed_tech_spec.py",
            "test_full_notification.py",
            "test_load_user.py",
            "test_network_stability.py",
            "test_openai_connection.py",
            "test_schedule_admin.py",
            "test_telegram.py",
            "test_telegram_network.py",
            "test_updated_questionnaire.py"
        ],

        "Скрипты создания и настройки": [
            "add_image_columns.py",
            "add_image_columns.sql",
            "add_is_admin_column.py",
            "add_is_admin_to_users.py",
            "add_translations.py",
            "append_translations.py",
            "create_admin.py",
            "create_admin_render.py",
            "create_pricing_packages.py",
            "create_tables.py",
            "init_migrations.py",
            "init_postgres_schemas.py",
            "make_admin.py",
            "setup_cascade_migrations.py",
            "setup_postgres_tables.py",
            "setup_render_storage.py",
            "simple_create_tables.py"
        ],

        "Скрипты проверки и диагностики": [
            "check_admin.py",
            "check_admin2.py",
            "check_categories.py",
            "check_db_status.py",
            "check_deployment.sh",
            "check_environment.py",
            "check_production_config.py",
            "check_translations.py",
            "diagnose_openai.py",
            "diagnostics_openai.py",
            "diagnostic_telegram.py",
            "direct_db_init.py",
            "direct_image_migration.py",
            "direct_start.sh"
        ],

        "Скрипты миграции и исправления": [
            "drop_all_tables.py",
            "extract_translations.py",
            "fix_alembic_revision.py",
            "fix_app_database.py",
            "fix_db_init.py",
            "fix_duplicate_columns.py",
            "fix_migrations.sh",
            "fix_migration_issue.py",
            "fix_revision_issue.py",
            "migrate_images.py",
            "migrate_images_v2.py"
        ],

        "Файлы переводов и локализации": [
            "babel.cfg",
            "compile_mo.py",
            "compile_translations.py",
            "dashboard_translations.txt",
            "missing_translations.txt",
            "new_translations.txt",
            "quick_compile_translations.py",
            "translations_cli.py",
            "update_translations.py"
        ],

        "Временные и дублирующие файлы": [
            "gunicorn_config.py.bak",
            "run_migrations.bat",
            "run_migrations.ps1",
            "run_migrations.sh",
            "scheduler.py",
            "tsconfig.json"
        ],

        "Директории для очистки": [
            "__pycache__",
            "migration_templates"
        ]
    }

    return files_to_delete

def get_scripts_to_clean():
    """Возвращает скрипты в папке scripts/, которые можно удалить"""

    scripts_to_delete = [
        "add_timestamp.py",
        "check_chat_messages.py",
        "check_conversation.py",
        "check_conversation_ids.py",
        "check_database_tables.py",
        "clean_blog_content.py",
        "continue_chat.py",
        "create_pg_tables.py",
        "fix_categories.py",
        "fix_telegram_notifications.ps1",
        "fix_translations.py",
        "fix_translations.sh",
        "fix_translation_duplicates.ps1",
        "link_questionnaire_to_projects.py",
        "seed_blog.py",
        "seed_blog_simple.py",
        "seed_blog_sqlite.py",
        "telegram_connectivity_test.py",
        "test_chat_api.py",
        "test_db_connection.py",
        "test_telegram.py",
        "test_telegram_direct.py",
        "__pycache__"
    ]

    return scripts_to_delete

def safe_delete_file(filepath):
    """Безопасное удаление файла с проверкой существования"""
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
            print(f"✓ Удален: {filepath}")
            return True
        except Exception as e:
            print(f"✗ Ошибка удаления {filepath}: {e}")
            return False
    else:
        print(f"- Файл не найден: {filepath}")
        return False

def safe_delete_directory(dirpath):
    """Безопасное удаление директории"""
    if os.path.exists(dirpath):
        try:
            shutil.rmtree(dirpath)
            print(f"✓ Удалена директория: {dirpath}")
            return True
        except Exception as e:
            print(f"✗ Ошибка удаления директории {dirpath}: {e}")
            return False
    else:
        print(f"- Директория не найдена: {dirpath}")
        return False

def clean_project():
    """Основная функция очистки проекта"""

    print("🧹 НАЧИНАЕМ БЕЗОПАСНУЮ ОЧИСТКУ ПРОЕКТА")
    print("=" * 50)

    # Получаем списки файлов для удаления
    files_to_delete = get_files_to_delete()
    scripts_to_delete = get_scripts_to_clean()

    total_deleted = 0
    total_errors = 0

    # Удаляем файлы в корне проекта
    print("\n📁 Очистка корневой директории:")
    for category, files in files_to_delete.items():
        if not files:
            continue

        print(f"\n{category}:")
        for filename in files:
            filepath = os.path.join(os.getcwd(), filename)
            if filename in files_to_delete["Директории для очистки"]:
                if safe_delete_directory(filepath):
                    total_deleted += 1
                else:
                    total_errors += 1
            else:
                if safe_delete_file(filepath):
                    total_deleted += 1
                else:
                    total_errors += 1

    # Удаляем файлы в папке scripts/
    print("\n📁 Очистка директории scripts/:")
    for filename in scripts_to_delete:
        filepath = os.path.join(os.getcwd(), "scripts", filename)
        if filename == "__pycache__":
            if safe_delete_directory(filepath):
                total_deleted += 1
            else:
                total_errors += 1
        else:
            if safe_delete_file(filepath):
                total_deleted += 1
            else:
                total_errors += 1

    # Очистка __pycache__ в других местах
    print("\n📁 Очистка __pycache__ директорий:")
    for root, dirs, files in os.walk(os.getcwd()):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            if safe_delete_directory(pycache_path):
                total_deleted += 1
            else:
                total_errors += 1

    print("\n" + "=" * 50)
    print("🎉 ОЧИСТКА ЗАВЕРШЕНА!")
    print(f"✅ Успешно удалено: {total_deleted} файлов/директорий")
    print(f"❌ Ошибок: {total_errors}")

    if total_errors > 0:
        print("\n⚠️  Некоторые файлы не удалось удалить. Проверьте права доступа.")

    print("\n🔍 РЕКОМЕНДАЦИИ:")
    print("1. Проверьте, что проект все еще работает после очистки")
    print("2. Запустите приложение и протестируйте основные функции")
    print("3. Если что-то сломалось - восстановите файлы из git")

def show_preview():
    """Показывает превью того, что будет удалено"""

    print("🧹 ПРЕВЬЮ ОЧИСТКИ ПРОЕКТА")
    print("=" * 50)

    files_to_delete = get_files_to_delete()
    scripts_to_delete = get_scripts_to_clean()

    total_files = 0

    print("\n📁 Файлы в корневой директории:")
    for category, files in files_to_delete.items():
        if files:
            print(f"\n{category} ({len(files)} файлов):")
            for filename in files:
                filepath = os.path.join(os.getcwd(), filename)
                if os.path.exists(filepath):
                    print(f"  ✓ {filename}")
                    total_files += 1
                else:
                    print(f"  - {filename} (уже удален)")

    print("\n📁 Файлы в директории scripts/:")
    for filename in scripts_to_delete:
        filepath = os.path.join(os.getcwd(), "scripts", filename)
        if os.path.exists(filepath):
            print(f"  ✓ scripts/{filename}")
            total_files += 1
        else:
            print(f"  - scripts/{filename} (уже удален)")

    print("\n📁 __pycache__ директории:")
    pycache_count = 0
    for root, dirs, files in os.walk(os.getcwd()):
        if "__pycache__" in dirs:
            pycache_path = os.path.join(root, "__pycache__")
            if os.path.exists(pycache_path):
                print(f"  ✓ {os.path.relpath(pycache_path)}")
                pycache_count += 1

    print("\n" + "=" * 50)
    print(f"📊 ИТОГО: {total_files} файлов + {pycache_count} __pycache__ директорий")
    print("\n⚠️  ВНИМАНИЕ:")
    print("• Этот скрипт удалит все перечисленные файлы")
    print("• Убедитесь, что эти файлы действительно не нужны")
    print("• Сделайте резервную копию проекта перед запуском")
    print("• После очистки протестируйте работу приложения")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--preview":
        show_preview()
    else:
        print("🧹 СКРИПТ ОЧИСТКИ ПРОЕКТА")
        print("\nИспользование:")
        print("  python clean_project.py --preview    # Показать что будет удалено")
        print("  python clean_project.py              # Выполнить очистку")
        print("\n⚠️  Резервное копирование:")
        print("  git add . && git commit -m 'Before cleanup'")
        print("\nЗапуск без параметров начнет очистку!")
        response = input("\nВы уверены, что хотите продолжить? (yes/no): ")
        if response.lower() == 'yes':
            clean_project()
        else:
            print("Очистка отменена.")
