from flask import Flask, current_app
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
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
        engine = db.get_engine(app)
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


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)
    
    # Force SQLite for development if FLASK_ENV is set to development
    if os.environ.get('FLASK_ENV') == 'development' and not os.environ.get('DATABASE_URL'):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    
    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)
    
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
        from flask import request, redirect, url_for, flash
        
        error_str = str(e)
        app.logger.error(f"400 ошибка: {error_str}")
        
        if 'csrf_token' in error_str or 'CSRF' in error_str:
            app.logger.warning(f"CSRF ошибка: {error_str}, реферер: {request.referrer}")
            flash('Ошибка безопасности: CSRF токен отсутствует или неверен. Пожалуйста, попробуйте снова.', 'danger')
            return redirect(request.referrer or url_for('admin.dashboard'))
        return e
    
    # Configure schema handling based on DB dialect
    with app.app_context():
        try:
            setup_schema_handling(app)
        except Exception as e:
            app.logger.warning(f"Schema setup deferred: {e}")
    
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
