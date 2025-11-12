from flask import current_app
from app import db
from sqlalchemy import text, inspect

def ensure_chat_message_model():
    """
    DISABLED: All schema changes now handled by db.create_all() or Alembic migrations.
    Raw SQL migrations don't respect PostgreSQL schema configuration.
    """
    try:
        current_app.logger.info("✅ Chat message schema handled by SQLAlchemy models")
        return
        
        # OLD CODE DISABLED:
        # verify connection and clear any failed tx
        # try:
        #     db.session.rollback()
        # except Exception:
        #     pass
        # db.session.execute(text('SELECT 1'))
        #
        # inspector = inspect(db.engine)
        # if not inspector.has_table('chat_messages'):
        #     current_app.logger.info("chat_messages table doesn't exist yet. It will be created by models/migrations.")
        #     return

        # refresh columns view each time after changes
        def get_columns():
            return {col['name'] for col in inspector.get_columns('chat_messages')}

        # DISABLED: Raw SQL migrations don't respect PostgreSQL schema
        # All schema changes should be done via Alembic migrations or db.create_all()
        # cols = get_columns()
        #
        # if 'conversation_id' not in cols:
        #     current_app.logger.info("Adding conversation_id column to chat_messages table")
        #     with db.engine.begin() as conn:
        #         conn.execute(text("ALTER TABLE chat_messages ADD COLUMN conversation_id VARCHAR(64)"))
        #         try:
        #             conn.execute(text("CREATE INDEX ix_chat_messages_conversation_id ON chat_messages (conversation_id)"))
        #         except Exception:
        #             pass
        #
        # cols = get_columns()
        #
        # if 'thread_id' not in cols:
        #     current_app.logger.info("Adding thread_id column to chat_messages table")
        #     with db.engine.begin() as conn:
        #         conn.execute(text("ALTER TABLE chat_messages ADD COLUMN thread_id VARCHAR(64)"))
        #         try:
        #             conn.execute(text("CREATE INDEX ix_chat_messages_thread_id ON chat_messages (thread_id)"))
        #         except Exception:
        #             pass
        
        current_app.logger.info("✅ Schema migrations disabled - using Alembic/SQLAlchemy models")

    except Exception as e:
        current_app.logger.error(f"Error checking/updating database schema: {e}")

def ensure_assistant_thread_model():
    """
    Ensure assistant_threads table exists (for Assistants API threads).
    """
    try:
        try:
            db.session.rollback()
        except Exception:
            pass
        db.session.execute(text('SELECT 1'))

        inspector = inspect(db.engine)
        if not inspector.has_table('assistant_threads'):
            current_app.logger.info("Creating assistant_threads table...")
            # Create via SQLAlchemy Table metadata if available
            from app.models.assistant_thread import AssistantThread
            AssistantThread.__table__.create(db.engine)
            current_app.logger.info("assistant_threads table created successfully")
        else:
            # Table exists
            pass
    except Exception as e:
        current_app.logger.error(f"Error ensuring assistant_threads table: {e}")

# Initialize the database migration
def initialize_db_migrations(app=None):
    """
    Initialize database migrations for chat message changes.
    Run this during app startup to ensure the database schema is up to date.
    
    Args:
        app: Flask application instance. If provided, will use app.logger.
             Otherwise will use standard logging.
    """
    import logging
    from flask import current_app

    # Make sure we use the app context when provided
    if app:
        with app.app_context():
            try:
                ensure_chat_message_model()
                ensure_assistant_thread_model()
                app.logger.info("Chat database schema initialized successfully")
                return True
            except Exception as e:
                app.logger.error(f"Error initializing database migrations: {e}")
                return False
    else:
        # Fallback to standard logging if no app provided
        try:
            ensure_chat_message_model()
            ensure_assistant_thread_model()
            logging.info("Chat database schema initialized successfully")
            return True
        except Exception as e:
            logging.error(f"Error initializing database migrations: {e}")
            return False
