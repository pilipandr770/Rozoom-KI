# Исправление проблемы с SSL-соединением к PostgreSQL

## Обнаруженная проблема

При развертывании на сервере Render.com возникала ошибка SSL-соединения к базе данных PostgreSQL:

```
psycopg2.OperationalError: SSL error: decryption failed or bad record mac
```

## Причина проблемы

Ошибка возникала при попытке доступа к странице блога `/blog`, где выполнялся запрос к базе данных. Проблема была связана с:

1. **SSL-сертификатами**: На Render.com иногда возникают проблемы с SSL-сертификатами PostgreSQL
2. **Параметры SSL**: Неправильная обработка SSL-параметров в URL подключения к БД
3. **Отсутствие fallback**: Приложение не имело механизма для отключения SSL в случае проблем

## Решение

### 1. Обновление конфигурации базы данных (`app/config.py`)

Добавлена более гибкая обработка SSL-параметров:

```python
# SSL configuration for PostgreSQL connections
DISABLE_SSL = os.getenv('DISABLE_POSTGRES_SSL', 'False').lower() in ('true', 'yes', '1')

if database_url and 'postgresql://' in database_url and not DISABLE_SSL:
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
```

### 2. Добавление тестирования подключения (`app/__init__.py`)

Добавлена функция `test_database_connection()` для проверки подключения и автоматического исправления проблем SSL:

```python
def test_database_connection(app):
    """Test database connection and handle SSL issues gracefully"""
    try:
        # Try to connect to the database
        db.session.execute(text('SELECT 1'))
        app.logger.info("Database connection successful")
    except Exception as e:
        error_msg = str(e).lower()
        
        # Check if it's an SSL-related error
        if 'ssl' in error_msg or 'decryption failed' in error_msg or 'bad record mac' in error_msg:
            app.logger.warning(f"SSL connection error detected: {e}")
            
            # Try to disable SSL and reconnect
            if 'postgresql://' in app.config['SQLALCHEMY_DATABASE_URI']:
                app.logger.info("Attempting to disable SSL for database connection...")
                
                # Remove SSL parameters from the database URL
                db_url = app.config['SQLALCHEMY_DATABASE_URI']
                if '?' in db_url:
                    base_url = db_url.split('?')[0]
                    params = db_url.split('?')[1].split('&')
                    # Remove SSL-related parameters
                    non_ssl_params = [p for p in params if not p.startswith('ssl')]
                    
                    if non_ssl_params:
                        new_db_url = base_url + '?' + '&'.join(non_ssl_params)
                    else:
                        new_db_url = base_url
                    
                    app.config['SQLALCHEMY_DATABASE_URI'] = new_db_url
                    app.logger.info("SSL parameters removed from database URL")
                    
                    # Reinitialize database with new URL
                    db.init_app(app)
                    
                    # Try connecting again
                    try:
                        db.session.execute(text('SELECT 1'))
                        app.logger.info("Database connection successful after disabling SSL")
                    except Exception as retry_error:
                        app.logger.error(f"Database connection failed even after disabling SSL: {retry_error}")
                        raise retry_error
                else:
                    app.logger.error("Cannot disable SSL - no parameters found in database URL")
                    raise e
            else:
                app.logger.error(f"SSL error on non-PostgreSQL database: {e}")
                raise e
        else:
            app.logger.error(f"Database connection error: {e}")
            raise e
```

### 3. Дополнительные параметры SQLAlchemy

Добавлены параметры для лучшей обработки соединений:

```python
# Additional SQLAlchemy settings for better error handling
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,  # Test connections before use
    'pool_recycle': 300,    # Recycle connections after 5 minutes
}
```

## Переменные окружения

Добавлена новая переменная окружения для ручного управления SSL:

- `DISABLE_POSTGRES_SSL=true` - полностью отключает добавление SSL-параметров к URL базы данных

## Результат

После внесения изменений:

1. **Приложение корректно обрабатывает SSL-ошибки** и автоматически пытается отключить SSL
2. **Логи содержат подробную информацию** о процессе исправления проблем подключения
3. **Добавлена возможность ручного управления** SSL через переменные окружения
4. **Улучшена стабильность подключения** к базе данных на Render.com

Теперь при возникновении SSL-проблем приложение автоматически попытается исправить ситуацию, что должно решить ошибку "SSL error: decryption failed or bad record mac".
