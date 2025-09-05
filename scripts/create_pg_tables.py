"""
Script to create blog tables in the PostgreSQL database
"""
import os
import sys

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models import BlogPost, BlogCategory, BlogTag

def create_blog_tables():
    """Create blog tables in the database."""
    app = create_app()
    with app.app_context():
        # Create tables for these models if they don't exist
        try:
            # Create blog tables only
            for table in [BlogPost.__table__, BlogCategory.__table__, BlogTag.__table__]:
                table_name = table.name
                print(f"Creating table: {table_name}")
                # Check if table exists
                conn = db.engine.connect()
                # Different query depending on PostgreSQL vs SQLite
                if db.engine.dialect.name == 'postgresql':
                    result = conn.execute(f"""
                        SELECT EXISTS (
                            SELECT FROM information_schema.tables 
                            WHERE table_name = '{table_name}'
                        );
                    """)
                    if result.scalar():
                        print(f"Table {table_name} already exists, dropping it...")
                        conn.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                    
                    # Create the table
                    table.create(db.engine)
                else:
                    # For SQLite
                    result = conn.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")
                    if result.fetchone():
                        print(f"Table {table_name} already exists, dropping it...")
                        conn.execute(f"DROP TABLE IF EXISTS {table_name};")
                    
                    # Create the table
                    table.create(db.engine)
                
                print(f"Created table: {table_name}")
                conn.close()
            
            print("All blog tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    create_blog_tables()
    print("Database setup completed!")
