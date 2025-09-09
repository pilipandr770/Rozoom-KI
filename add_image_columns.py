#!/usr/bin/env python
"""
Скрипт для добавления колонки original_image_url в таблицы
"""
import os
import sys
import logging
import sqlalchemy as sa

# Add the app directory to path so we can import app modules
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def add_column_if_not_exists():
    """Add the original_image_url column if it doesn't exist"""
    app = create_app()
    
    with app.app_context():
        try:
            # Read the SQL file
            with open('add_image_columns.sql', 'r') as f:
                sql = f.read()
            
            # Execute the SQL
            db.session.execute(sa.text(sql))
            db.session.commit()
            print("Successfully added original_image_url columns (if they didn't exist already)")
            return True
        except Exception as e:
            print(f"Error adding columns: {str(e)}")
            return False

if __name__ == '__main__':
    success = add_column_if_not_exists()
    sys.exit(0 if success else 1)
