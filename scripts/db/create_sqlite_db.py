"""
Create all tables in a local SQLite database for development/testing.

This script will load the Flask app and SQLAlchemy metadata and create
all tables. If models declare a PostgreSQL schema, the script will strip
the schema when using SQLite (SQLite doesn't support schemas).

Usage:
  python scripts\db\create_sqlite_db.py

It reads DATABASE_URL from .env (falls back to sqlite:///dev.db).
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is on sys.path so `import app` works when script is run directly
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

load_dotenv()

def main():
  # force sqlite for local dev
  os.environ['DATABASE_URL'] = 'sqlite:///app/dev.db'

  # import app after we ensured DATABASE_URL points to sqlite
  from app import create_app, db

  app = create_app()
  try:
    engine = db.session.get_bind()
  except Exception:
    engine = db.get_engine(app)

  with app.app_context():
    # Drop all tables first to ensure clean slate
    db.drop_all()

    # Create all tables fresh
    db.create_all()
    print('Created tables on', engine.url)

if __name__ == '__main__':
    main()
