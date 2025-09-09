# Исправление проблем миграции базы данных на Render.com

## Проблема

При деплое на Render.com вы можете столкнуться со следующей ошибкой:
```
ОШИБКА [flask_migrate] Ошибка: Не удается найти ревизию, идентифицированную как 'ac4cda9e7cef'
```

Это происходит из-за несоответствия между историей миграций в репозитории и состоянием базы данных на Render.com. Часто возникает при переходе с SQLite на PostgreSQL или при деплое на новый экземпляр базы данных.

## Решение проблемы

Для исправления проблемы созданы специальные скрипты:

### Вариант 1: Автоматическое исправление через альтернативный запуск

Приложение настроено на автоматическое исправление проблем с миграциями. Если основной скрипт запуска `render_start.sh` завершается с ошибкой, автоматически запускается `direct_start.sh`, который создает таблицы напрямую, минуя систему миграций Flask-Migrate.

### Вариант 2: Ручное исправление через консоль Render

1. Откройте Shell для вашего веб-сервиса на Render.com
2. Выполните команду:
   ```
   bash fix_migrations.sh
   ```
3. Перезапустите веб-сервис

### Вариант 3: Полный сброс базы данных и миграций

Если предыдущие варианты не помогли, можно полностью сбросить базу данных и начать с нуля:

1. Откройте Shell для вашего веб-сервиса на Render.com
2. Выполните следующие команды:
   ```
   python -c "from app import create_app; from flask_migrate import init, migrate, upgrade; app = create_app(); from app import db; import os, shutil; migrations_dir = os.path.join(os.path.dirname(os.path.abspath('.')), 'migrations'); shutil.rmtree(migrations_dir) if os.path.exists(migrations_dir) else None; app.app_context().push(); init(); migrate(message='initial'); upgrade()"
   ```
3. Перезапустите веб-сервис

## Дополнительные скрипты

- **init_migrations.py** - инициализирует миграции с нуля
- **init_postgres_schemas.py** - создает необходимые схемы PostgreSQL
- **setup_postgres_tables.py** - создает таблицы напрямую через SQLAlchemy
- **fix_migrations.sh** - комбинированный скрипт для исправления всех проблем
- **direct_start.sh** - альтернативный скрипт запуска, минующий систему миграций

## Миграция данных из SQLite (если необходимо)

Если вам нужно перенести данные из локальной SQLite базы в PostgreSQL:

1. Экспортируйте данные из локальной базы:
   ```
   python setup_postgres_tables.py --sqlite=dev.db
   ```
2. Загрузите экспорт в Render.com и выполните импорт:
   ```
   python setup_postgres_tables.py --sqlite=exported_data.json
   ```
