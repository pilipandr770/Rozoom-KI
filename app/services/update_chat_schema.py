"""
Database migration script to update the schema for the ChatMessage model
to support the direct API approach instead of the Assistants API.

This script should be run with Flask app context.
"""

from flask import current_app
from app import db
from app.models.chat_message import ChatMessage
from sqlalchemy import text, inspect
import sys

def run_migrations():
    """Run the necessary database migrations for the ChatMessage model."""
    try:
        # Check if we have a database connection
        db.session.execute(text('SELECT 1'))
        current_app.logger.info("Database connection successful")
        
        # Check if ChatMessage table exists
        inspector = inspect(db.engine)
        has_table = inspector.has_table('chat_messages')
        
        if not has_table:
            current_app.logger.info("Creating chat_messages table...")
            ChatMessage.__table__.create(db.engine)
            current_app.logger.info("chat_messages table created successfully")
        else:
            current_app.logger.info("chat_messages table already exists")
            
            # Check if conversation_id and thread_id columns exist
            columns = [col['name'] for col in inspector.get_columns('chat_messages')]
            
            # Add missing columns if needed
            if 'conversation_id' not in columns:
                current_app.logger.info("Adding conversation_id column...")
                db.engine.execute(text(
                    "ALTER TABLE chat_messages ADD COLUMN conversation_id VARCHAR(64)"
                ))
                db.engine.execute(text(
                    "CREATE INDEX ix_chat_messages_conversation_id ON chat_messages (conversation_id)"
                ))
                current_app.logger.info("conversation_id column added")
                
            if 'thread_id' not in columns:
                current_app.logger.info("Adding thread_id column...")
                db.engine.execute(text(
                    "ALTER TABLE chat_messages ADD COLUMN thread_id VARCHAR(64)"
                ))
                db.engine.execute(text(
                    "CREATE INDEX ix_chat_messages_thread_id ON chat_messages (thread_id)"
                ))
                current_app.logger.info("thread_id column added")
                
        current_app.logger.info("Migration completed successfully")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error during migration: {e}")
        return False

if __name__ == "__main__":
    # This script should be imported and run with Flask app context
    print("This script should be run with Flask app context.")
    print("Example: with app.app_context(): run_migrations()")
    sys.exit(1)
