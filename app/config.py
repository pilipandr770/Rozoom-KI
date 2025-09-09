import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # SQLAlchemy настройки с поддержкой для SQLite (локально) и PostgreSQL (продакшен)
    database_url = os.getenv('DATABASE_URL')
    
    # Исправляем URL для PostgreSQL, если он начинается с "postgres://" вместо "postgresql://"
    # (Render.com иногда предоставляет такой формат)
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Add SSL parameters for PostgreSQL connections (required for Render.com)
    if database_url and 'postgresql://' in database_url:
        if '?' not in database_url:
            database_url += '?sslmode=require'
        else:
            database_url += '&sslmode=require'
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_SCHEMA = os.getenv('POSTGRES_SCHEMA', 'rozoom_ki_schema')
    POSTGRES_SCHEMA_CLIENTS = os.getenv('POSTGRES_SCHEMA_CLIENTS', 'rozoom_ki_clients')
    POSTGRES_SCHEMA_SHOP = os.getenv('POSTGRES_SCHEMA_SHOP', 'rozoom_ki_shop')
    POSTGRES_SCHEMA_PROJECTS = os.getenv('POSTGRES_SCHEMA_PROJECTS', 'rozoom_ki_projects')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Babel settings for internationalization
    LANGUAGES = ['en', 'de']
    BABEL_DEFAULT_LOCALE = 'de'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    
    # Mail settings
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.example.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', 'yes', '1')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ('true', 'yes', '1')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@rozoom-ki.com')
