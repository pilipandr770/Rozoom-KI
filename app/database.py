"""
Database initialization and schema updates
"""
from sqlalchemy import text, inspect
from app import db

def init_database_schema(app):
    """Initialize or update database schema manually when needed"""
    with app.app_context():
        # use session bind instead of deprecated db.get_engine(app)
        try:
            engine = db.session.get_bind()
        except Exception:
            app.logger.warning("Database session not available yet, deferring schema init")
            return

        inspector = inspect(engine)
        
        # Create all tables if they don't exist
        try:
            db.create_all()
            app.logger.info("Database tables have been created if they did not exist")
        except Exception as e:
            app.logger.error(f"Failed to create database tables: {str(e)}")
        
        # Check and add email column to AdminUser if needed
        if 'admin_users' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('admin_users')]
            if 'email' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE admin_users ADD COLUMN IF NOT EXISTS email VARCHAR(120)"))
                        app.logger.info("Added email column to admin_users table")
                except Exception as e:
                    app.logger.error(f"Failed to add email column to admin_users: {str(e)}")
        
        # Check and add columns to leads table
        if 'leads' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('leads')]
            
            if 'phone' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone VARCHAR(100)"))
                        app.logger.info("Added phone column to leads table")
                except Exception as e:
                    app.logger.error(f"Failed to add phone column to leads: {str(e)}")
            
            if 'company' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE leads ADD COLUMN IF NOT EXISTS company VARCHAR(255)"))
                        app.logger.info("Added company column to leads table")
                except Exception as e:
                    app.logger.error(f"Failed to add company column to leads: {str(e)}")
            
        # Check and add conversation_id column to chat_messages table
        if 'chat_messages' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('chat_messages')]
            
            if 'conversation_id' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS conversation_id VARCHAR(36)"))
                        # Create an index for conversation_id
                        conn.execute(text("CREATE INDEX IF NOT EXISTS ix_chat_messages_conversation_id ON chat_messages (conversation_id)"))
                        app.logger.info("Added conversation_id column to chat_messages table")
                except Exception as e:
                    app.logger.error(f"Failed to add conversation_id column to chat_messages: {str(e)}")
                    # We'll handle the error in the API layer with our dynamic schema handling
            if 'data' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE leads ADD COLUMN IF NOT EXISTS data TEXT"))
                        app.logger.info("Added data column to leads table")
                except Exception as e:
                    app.logger.error(f"Failed to add data column to leads: {str(e)}")
                    
            if 'source' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE leads ADD COLUMN IF NOT EXISTS source VARCHAR(100)"))
                        app.logger.info("Added source column to leads table")
                except Exception as e:
                    app.logger.error(f"Failed to add source column to leads: {str(e)}")
                    
            if 'status' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE leads ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'new'"))
                        app.logger.info("Added status column to leads table")
                except Exception as e:
                    app.logger.error(f"Failed to add status column to leads: {str(e)}")
        
        # Check and update User table for authentication
        if 'users' in inspector.get_table_names():
            columns = [col['name'] for col in inspector.get_columns('users')]
            
            if 'password_hash' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(256)"))
                        app.logger.info("Added password_hash column to users table")
                except Exception as e:
                    app.logger.error(f"Failed to add password_hash column to users: {str(e)}")
            
            if 'is_active' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE"))
                        app.logger.info("Added is_active column to users table")
                except Exception as e:
                    app.logger.error(f"Failed to add is_active column to users: {str(e)}")
                    
            if 'is_admin' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE"))
                        app.logger.info("Added is_admin column to users table")
                except Exception as e:
                    app.logger.error(f"Failed to add is_admin column to users: {str(e)}")
                    
            if 'created_at' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
                        app.logger.info("Added created_at column to users table")
                except Exception as e:
                    app.logger.error(f"Failed to add created_at column to users: {str(e)}")
                    
            if 'last_login' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP"))
                        app.logger.info("Added last_login column to users table")
                except Exception as e:
                    app.logger.error(f"Failed to add last_login column to users: {str(e)}")
                    
            if 'phone' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(100)"))
                        app.logger.info("Added phone column to users table")
                except Exception as e:
                    app.logger.error(f"Failed to add phone column to users: {str(e)}")
                    
            if 'company' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS company VARCHAR(255)"))
                        app.logger.info("Added company column to users table")
                except Exception as e:
                    app.logger.error(f"Failed to add company column to users: {str(e)}")
                    
            if 'name' not in columns:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS name VARCHAR(255)"))
                        app.logger.info("Added name column to users table")
                except Exception as e:
                    app.logger.error(f"Failed to add name column to users: {str(e)}")
                    
            # Fix username constraint to allow NULL values
            try:
                with engine.begin() as conn:
                    conn.execute(text("ALTER TABLE users ALTER COLUMN username DROP NOT NULL"))
                    app.logger.info("Modified username constraint to allow NULL values")
            except Exception as e:
                app.logger.info(f"Note about username constraint: {str(e)}")
        
        # Create projects table if it doesn't exist
        # Note: This fallback is deprecated - SQLAlchemy should handle table creation
        # Kept for backwards compatibility only
        if 'projects' not in inspector.get_table_names():
            app.logger.warning("Projects table missing - should be created by SQLAlchemy models")
        
        # Create project_tasks table if it doesn't exist
        # Note: This fallback is deprecated - SQLAlchemy should handle table creation
        # Kept for backwards compatibility only
        if 'project_tasks' not in inspector.get_table_names():
            app.logger.warning("Project_tasks table missing - should be created by SQLAlchemy models")
                
        # Create project_updates table if it doesn't exist
        # Note: This fallback is deprecated - SQLAlchemy should handle table creation
        # Kept for backwards compatibility only
        if 'project_updates' not in inspector.get_table_names():
            app.logger.warning("Project_updates table missing - should be created by SQLAlchemy models")
                
# Для возможности запуска как отдельный скрипт
if __name__ == "__main__":
    from app import create_app
    app = create_app()
    init_database_schema(app)
    print("База данных успешно инициализирована.")
