"""
Run database migrations script with proper application context
"""
from app import create_app, db
from flask_migrate import upgrade

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        print("Starting database migrations...")
        upgrade()
        print("Database migrations complete!")
