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
    # Try to load regular user first
    from app.models import User
    user = User.query.get(int(user_id))
    if user:
        return user
    
    # If not found, try admin user
    return AdminUser.query.get(int(user_id))

# Function to create admin user for initial setup
def create_admin_user(app):
    with app.app_context():
        # Create admin user table if it doesn't exist
        db.create_all()
        
        # Check if admin user exists
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
