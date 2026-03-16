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
    
    def get_id(self):
        """Prefix admin IDs to avoid collision with regular User IDs in Flask-Login session"""
        return f"admin_{self.id}"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login.
    
    IDs are prefixed to avoid collisions between AdminUser and User tables:
    - AdminUser: stored as 'admin_<id>'
    - User:      stored as 'user_<id>'
    Legacy unprefixed IDs are handled for backwards compatibility.
    """
    from flask import current_app
    from app import db

    try:
        if isinstance(user_id, str) and user_id.startswith('admin_'):
            return db.session.get(AdminUser, int(user_id[6:]))

        if isinstance(user_id, str) and user_id.startswith('user_'):
            from app.models import User
            return db.session.get(User, int(user_id[5:]))

        # Legacy fallback: bare numeric ID (old sessions before prefix migration)
        uid = int(user_id)
        from app.models import User
        user = db.session.get(User, uid)
        if user:
            return user
        return db.session.get(AdminUser, uid)

    except Exception as e:
        try:
            current_app.logger.error(f"Error loading user {user_id}: {str(e)}")
        except Exception:
            pass
        return None

# Function to create admin user for initial setup
def create_admin_user(app):
    with app.app_context():
        from sqlalchemy import inspect, text
        from sqlalchemy.exc import ProgrammingError
        
        # Note: PostgreSQL schema is configured at metadata level in create_app()
        # Tables should already be created by create_tables.sh during deployment
        schema = app.config.get('POSTGRES_SCHEMA', 'rozoom_ki_schema') if 'postgresql' in app.config['SQLALCHEMY_DATABASE_URI'] else None
        
        # Verify tables exist
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names(schema=schema)
        
        if not existing_tables:
            app.logger.error(f"CRITICAL: No tables found in schema '{schema}'. Database initialization failed during deployment.")
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
