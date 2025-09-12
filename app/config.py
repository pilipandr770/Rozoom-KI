import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # CSRF Protection settings
    # Increase CSRF token validity to 1 day (86400 seconds) instead of the default 1 hour
    WTF_CSRF_TIME_LIMIT = 86400
    WTF_CSRF_SSL_STRICT = False  # Don't enforce HTTPS for CSRF tokens
    
    # SQLAlchemy настройки с поддержкой для SQLite (локально) и PostgreSQL (продакшен)
    database_url = os.getenv('DATABASE_URL')
    
    # Исправляем URL для PostgreSQL, если он начинается с "postgres://" вместо "postgresql://"
    # (Render.com иногда предоставляет такой формат)
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # SSL configuration for PostgreSQL connections
    DISABLE_SSL = os.getenv('DISABLE_POSTGRES_SSL', 'False').lower() in ('true', 'yes', '1')
    
    if database_url and 'postgresql://' in database_url:
        if DISABLE_SSL:
            # Completely disable SSL if explicitly requested
            app.logger.info("SSL disabled by DISABLE_POSTGRES_SSL environment variable")
            # Remove any existing SSL parameters
            if '?' in database_url:
                base_url = database_url.split('?')[0]
                params = database_url.split('?')[1].split('&')
                # Remove SSL-related parameters
                non_ssl_params = [p for p in params if not p.startswith('ssl')]
                if non_ssl_params:
                    database_url = base_url + '?' + '&'.join(non_ssl_params)
                else:
                    database_url = base_url
        else:
            # Add SSL parameters for PostgreSQL connections (required for Render.com)
            try:
                # Parse the URL to properly add SSL parameters
                if '?' in database_url:
                    # URL already has parameters
                    if 'sslmode=' not in database_url:
                        database_url += '&sslmode=require'
                else:
                    # URL has no parameters
                    database_url += '?sslmode=require'
                
                # Ensure other SSL parameters are set for better compatibility
                ssl_params = []
                if '?' in database_url:
                    existing_params = database_url.split('?')[1].split('&')
                    for param in existing_params:
                        if param.startswith('ssl'):
                            ssl_params.append(param)
                
                # Add default SSL parameters if not present
                if not any('sslmode=' in param for param in ssl_params):
                    ssl_params.append('sslmode=require')
                
                # Reconstruct URL with proper SSL parameters
                base_url = database_url.split('?')[0]
                database_url = base_url + '?' + '&'.join(ssl_params)
                
            except Exception as e:
                # If SSL parameter parsing fails, log warning and use original URL
                print(f"Warning: Failed to parse SSL parameters for database URL: {e}")
                # Keep original database_url without SSL modifications
    
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///dev.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Additional SQLAlchemy settings for better error handling
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,  # Test connections before use
        'pool_recycle': 300,    # Recycle connections after 5 minutes
    }
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
