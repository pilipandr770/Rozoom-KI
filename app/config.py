import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES_SCHEMA = os.getenv('POSTGRES_SCHEMA', 'rozoom_ki_schema')
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
