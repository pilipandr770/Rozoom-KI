"""
Command for updating database schema on-the-fly
"""
import click
from flask.cli import with_appcontext
from sqlalchemy import inspect, text
from app import db
from flask import current_app


@click.command('update-schema')
@click.option('--force', is_flag=True, help='Force update even if columns exist')
@with_appcontext
def update_schema_command(force):
    """Update database schema on-the-fly."""
    click.echo('Updating database schema...')
    update_schema(force)
    click.echo('Done.')


def update_schema(force=False):
    """Update database schema with necessary changes."""
    # use session bind to be compatible with newer Flask-SQLAlchemy
    try:
        engine = db.session.get_bind()
    except Exception:
        engine = db.get_engine()
    inspector = inspect(engine)
    
    # Check if chat_messages table exists
    if 'chat_messages' not in inspector.get_table_names():
        click.echo('chat_messages table does not exist. Skipping.')
        return
    
    # Получаем список столбцов
    columns = [col['name'] for col in inspector.get_columns('chat_messages')]
    
    # Check conversation_id column
    if 'conversation_id' not in columns or force:
        try:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS conversation_id VARCHAR(36)"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_chat_messages_conversation_id ON chat_messages (conversation_id)"))
                click.echo('Added conversation_id column to chat_messages table')
        except Exception as e:
            current_app.logger.error(f"Failed to add conversation_id column to chat_messages: {e}")
            click.echo(f'Error adding conversation_id: {e}', err=True)
    else:
        click.echo('conversation_id column already exists in chat_messages table')
        
    # Check timestamp column
    if 'timestamp' not in columns or force:
        try:
            with engine.begin() as conn:
                conn.execute(text("ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
                conn.execute(text("CREATE INDEX IF NOT EXISTS ix_chat_messages_timestamp ON chat_messages (timestamp)"))
                click.echo('Added timestamp column to chat_messages table')
        except Exception as e:
            current_app.logger.error(f"Failed to add timestamp column to chat_messages: {e}")
            click.echo(f'Error adding timestamp: {e}', err=True)
    else:
        click.echo('timestamp column already exists in chat_messages table')
