Andrii Pylypchuk — Flask landing + Stripe + Chat-widget

Quick start:

1. Create virtualenv and install deps:

   python -m venv .venv
   .\.venv\Scripts\pip install -r requirements.txt

2. Copy `.env.example` to `.env` and set values.

3. Run app:

   python run.py

Database migrations (Flask-Migrate):

1. Initialize migrations (once):

   flask db init

2. Create migration after models change:

   flask db migrate -m "initial"

3. Apply migrations:

   flask db upgrade

Note: set `FLASK_APP=run.py` and activate virtualenv before running these commands.

If you don't have a local Postgres server, you can create tables locally with SQLite for development:

1. Ensure `.env` has `DATABASE_URL` set to a sqlite URL or leave empty to use `sqlite:///dev.db`.
2. Run the helper script:

   python scripts\db\create_sqlite_db.py

This will create tables locally and is useful for development when Postgres is not available (psql connection refused error is expected unless Postgres is running).
# Andrii Pylypchuk — "Години розробки" (Flask + Stripe)

Цей репозиторій містить сайт-продаж годин розробки із пакетами, оплатою через Stripe, багатомовністю (DE/EN, опційно UA) та блогом.  
**Швидкий старт:** відкрий `AGENT.md`  це єдине джерело правди для Copilot Agent.

## Структура
- AGENT.md  інструкція для Copilot Agent (що робити, пріоритети, стиль).
- PROJECT_SPEC.md — технічне завдання (ТЗ) з KPI, функціями, sitemap, приймальними критеріями.
- ROADMAP.md  етапи релізів (MVP  V1  V2).
- /agent  короткий контекст, задачі, чек-листи, промпти.
- /docs — архітектура, сторінки, Stripe, аналітика, legal.
- /.vscode — локальні налаштування VS Code (пріоритет контенту для агента).

## Запуск робіт з агентом
1) Відкрий `AGENT.md`.  
2) У Chat (справа) натисни **Add Context** і додай `AGENT.md` + `PROJECT_SPEC.md` (або просто звертайся: _"Follow AGENT.md and start from /agent/TASKS.md: Task 01"_).  
3) Працюй ітеративно по задачах з /agent/TASKS.md.  
