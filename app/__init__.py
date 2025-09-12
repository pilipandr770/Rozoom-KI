from flask import Flask, current_app
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import text
import os

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
csrf = CSRFProtect()

# Import here to avoid circular imports
from app.auth import login_manager
from app.babel import init_babel


def setup_schema_handling(app):
    """Configure schema handling based on the database dialect.

    For Postgres: Set search_path to use schema
    For SQLite: Remove schema from all table definitions
    """
    from sqlalchemy import text, event

    # Get database info (compatible with Flask-SQLAlchemy >=3)
    try:
        engine = db.session.get_bind()
    except Exception:
        try:
            engine = db.get_engine(app)
        except Exception:
            app.logger.warning("Database engine not available yet, deferring schema setup")
            return

    dialect = engine.dialect.name
    schema = app.config.get('POSTGRES_SCHEMA')

    # For SQLite: Remove schema from all tables at runtime
    if dialect == 'sqlite':
        # Inspect all tables and remove schema
        for table in db.metadata.tables.values():
            table.schema = None

        # Listen for table creation to ensure no schema is used
        @event.listens_for(db.metadata, 'after_create')
        def after_create(target, connection, **kw):
            for table in target.tables.values():
                if table.schema:
                    table.schema = None

    # For Postgres: Set search_path
    elif dialect in ('postgresql', 'postgres') and schema:
        try:
            with engine.connect() as conn:
                conn.execute(text(f"SET search_path TO {schema}, public"))

            # Ensure every new connection sets the search path
            @event.listens_for(engine, "connect")
            def connect(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute(f"SET search_path TO {schema}, public")
                cursor.close()
        except Exception as e:
            app.logger.error(f"Error setting up Postgres schema: {e}")


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
                    app.logger.info(f"SSL parameters removed from database URL: {new_db_url}")
                    
                    # Forcefully disable SSL by setting environment variable
                    import os
                    os.environ['DISABLE_POSTGRES_SSL'] = 'true'
                    
                    # Reinitialize database with new URL
                    db.init_app(app)
                    
                    # Try connecting again
                    try:
                        db.session.execute(text('SELECT 1'))
                        app.logger.info("Database connection successful after disabling SSL")
                    except Exception as retry_error:
                        app.logger.error(f"Database connection failed even after disabling SSL: {retry_error}")
                        # Try one more time with completely clean URL
                        clean_url = new_db_url.split('?')[0] if '?' in new_db_url else new_db_url
                        app.config['SQLALCHEMY_DATABASE_URI'] = clean_url
                        db.init_app(app)
                        try:
                            db.session.execute(text('SELECT 1'))
                            app.logger.info("Database connection successful with clean URL")
                        except Exception as final_error:
                            app.logger.error(f"Final database connection attempt failed: {final_error}")
                            raise final_error
                else:
                    app.logger.error(f"SSL error on non-PostgreSQL database: {e}")
                    raise e
            else:
                app.logger.error(f"SSL error on non-PostgreSQL database: {e}")
                raise e
        else:
            app.logger.error(f"Database connection error: {e}")
            raise e


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    
    # Force SQLite for development if FLASK_ENV is set to development
    if os.environ.get('FLASK_ENV') == 'development' and not os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    
    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Test database connection and handle SSL issues
    with app.app_context():
        test_database_connection(app)
    
    # Initialize Flask-Login
    login_manager.init_app(app)
    
    # Initialize Flask-Mail
    mail.init_app(app)
    
    # Initialize Flask-Babel
    init_babel(app)
    
    # Initialize CSRF protection
    csrf.init_app(app)
    
    # Исключить API чата из CSRF защиты
    @csrf.exempt
    def exempt_chat_api():
        from flask import request
        if request.path.startswith('/api/chat'):
            return True
        return False
    
    # Обработчик CSRF-ошибок
    @app.errorhandler(400)
    def handle_csrf_error(e):
        from flask import request, redirect, url_for, flash, session
        
        error_str = str(e)
        app.logger.error(f"400 ошибка: {error_str}")
        
        if 'csrf_token' in error_str or 'CSRF' in error_str:
            app.logger.warning(f"CSRF ошибка: {error_str}, реферер: {request.referrer}")
            
            # Check if token expired
            if 'истек' in error_str or 'expired' in error_str:
                flash('Срок действия сессии истек. Пожалуйста, попробуйте снова.', 'warning')
                # Regenerate CSRF token
                session.pop('_csrf_token', None)
                # If this is a form submission from contact page, redirect back there
                if request.referrer and 'contact' in request.referrer:
                    return redirect(url_for('pages.contact'))
            else:
                flash('Ошибка безопасности: CSRF токен отсутствует или неверен. Пожалуйста, попробуйте снова.', 'danger')
            
            # Determine where to redirect based on the referrer URL
            if request.referrer:
                if 'login' in request.referrer:
                    return redirect(url_for('auth.login'))
                elif 'contact' in request.referrer:
                    return redirect(url_for('pages.contact'))
            
            # Default fallback - redirect to login
            return redirect(url_for('auth.login'))
        return e
    
    # Configure schema handling based on DB dialect
    with app.app_context():
        try:
            setup_schema_handling(app)
        except Exception as e:
            app.logger.warning(f"Schema setup deferred: {e}")
    
    # Add route to refresh CSRF token via AJAX
    @app.route('/refresh-csrf-token')
    def refresh_csrf_token():
        from flask import jsonify, session
        from flask_wtf.csrf import generate_csrf
        
        # Generate a fresh CSRF token
        token = generate_csrf()
        
        return jsonify({'csrf_token': token})
    
    # Initialize or update database schema manually
    from .database import init_database_schema
    try:
        init_database_schema(app)
    except Exception as e:
        app.logger.warning(f"Database schema update deferred: {e}")
    
    # Create admin user
    from app.auth import create_admin_user
    create_admin_user(app)
    
    # Register blueprints
    from .pages import pages_bp
    from .api import api_bp
    from .routes.admin import admin
    from .routes.blog import blog
    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.lang import lang_bp
    from .routes.auto_content import auto_content
    
    app.register_blueprint(pages_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(admin)
    app.register_blueprint(blog)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(lang_bp)
    app.register_blueprint(auto_content)
    
    # Register CLI commands
    from .commands import register_commands
    register_commands(app)
    
    # Register template filters
    from . import template_filters
    template_filters.init_app(app)
    
    # Initialize scheduler for background tasks in production
    if not app.debug and not app.testing:
        try:
            from scheduler import init_scheduler
            scheduler = init_scheduler()
            app.scheduler = scheduler
        except Exception as e:
            app.logger.error(f"Error initializing scheduler: {e}")
    
    return app
