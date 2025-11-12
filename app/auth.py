"""
User authentication module
"""
from flask_login import LoginManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
import os

login_manager = LoginManager()

# Configure login manager
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Simple User model with UserMixin for Flask-Login
class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=True, nullable=False)  # Add is_admin attribute
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login"""
    from flask import current_app
    from app import db

    try:
        # Ensure we have an application context
        if not current_app:
            return None

        with current_app.app_context():
            # Try to load regular user first
            from app.models import User
            user = User.query.get(int(user_id))
            if user:
                return user

            # If not found, try admin user
            return AdminUser.query.get(int(user_id))
    except Exception as e:
        current_app.logger.error(f"Error loading user {user_id}: {str(e)}")
        return None

# Function to create admin user for initial setup
def create_admin_user(app):
    with app.app_context():
        from sqlalchemy import inspect, text
        from sqlalchemy.exc import ProgrammingError
        
        # Note: PostgreSQL schema is configured at metadata level in create_app()
        schema = app.config.get('POSTGRES_SCHEMA', 'rozoom_ki_schema') if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI'] else None
        
        # Aggressively clean up ALL indexes that might conflict
        if schema:
            try:
                with db.engine.begin() as conn:
                    # Get all indexes in the schema
                    result = conn.execute(text(f"""
                        SELECT indexname 
                        FROM pg_indexes 
                        WHERE schemaname = '{schema}'
                    """))
                    indexes = [row[0] for row in result]
                    
                    # Drop all indexes
                    for index_name in indexes:
                        try:
                            conn.execute(text(f"DROP INDEX IF EXISTS {schema}.{index_name}"))
                        except Exception:
                            pass
                    
                    app.logger.info(f"Cleaned up {len(indexes)} existing indexes before table creation")
            except Exception as e:
                app.logger.warning(f"Could not clean up indexes: {e}")
        
        # Create all tables - if this fails, the database is in a bad state
        try:
            db.create_all()
            app.logger.info("Database tables created/verified successfully")
        except Exception as e:
            app.logger.error(f"CRITICAL: Could not create database tables: {str(e)}")
            # Don't raise - let the app start and tables can be created later
        
        # Verify admin_users table exists
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names(schema=schema)
        
        if not existing_tables:
            app.logger.error(f"CRITICAL: No tables found in schema '{schema}'. Database may need manual initialization.")
            return
        
        app.logger.info(f"Found {len(existing_tables)} tables in database: {', '.join(existing_tables)}")
        
        if 'admin_users' not in existing_tables:
            app.logger.warning(f"admin_users table not found. Available tables: {existing_tables}")
            return
        
        admin = AdminUser.query.filter_by(username='admin').first()
        if not admin:
            try:
                # Try to create admin user with email
                admin = AdminUser(
                    username='admin',
                    email=os.environ.get('ADMIN_EMAIL', 'admin@rozoom-ki.com')
                )
                admin.set_password('admin')  # Default password, should be changed in production
                db.session.add(admin)
                db.session.commit()
                print("Admin user created.")
            except Exception as e:
                # If email column doesn't exist yet
                print(f"Warning: {e}")
                admin = AdminUser(username='admin')
                admin.set_password('admin')
                db.session.add(admin)
                db.session.commit()
                print("Admin user created without email field.")
        else:
            print("Admin user already exists.")
