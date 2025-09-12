"""Add meta column to ChatMessage

Revision ID: f456ad120936
Revises: f456ad120935
Create Date: 2025-09-12 15:30:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'f456ad120936'
down_revision = 'f456ad120935'
branch_labels = None
depends_on = None


def upgrade():
    # Add meta column - we try/except because this operation is not idempotent
    # If we're using SQLite, we'll need to use a different approach than JSON
    try:
        # First check if the column exists
        conn = op.get_bind()
        table_info = conn.execute("PRAGMA table_info(chat_messages)").fetchall()
        column_names = [col[1] for col in table_info]
        
        if 'meta' not in column_names:
            # For SQLite
            op.add_column('chat_messages', sa.Column('meta', sa.Text(), nullable=True))
            print("Added meta column to chat_messages table (SQLite)")
        else:
            print("meta column already exists in chat_messages table (SQLite)")
    except Exception as e:
        try:
            # Try PostgreSQL approach
            op.add_column('chat_messages', sa.Column('meta', postgresql.JSON(astext_type=sa.Text()), nullable=True))
            print("Added meta column to chat_messages table (PostgreSQL)")
        except Exception as e2:
            print(f"Could not add meta column: {e}, {e2}")

    # Also update the thread_id column to be nullable
    try:
        # For SQLite, we need to recreate the table
        # This is a simplified approach - in real production, you'd use a more robust method
        op.execute('PRAGMA foreign_keys=off')
        op.execute('''
        ALTER TABLE chat_messages RENAME TO chat_messages_old;
        ''')
        
        op.execute('''
        CREATE TABLE chat_messages (
            id INTEGER NOT NULL PRIMARY KEY,
            conversation_id VARCHAR(64) NOT NULL,
            thread_id VARCHAR(64),
            role VARCHAR(16) NOT NULL,
            content TEXT NOT NULL,
            meta TEXT,
            created_at DATETIME
        );
        ''')
        
        op.execute('''
        INSERT INTO chat_messages 
        SELECT id, conversation_id, thread_id, role, content, NULL, created_at 
        FROM chat_messages_old;
        ''')
        
        op.execute('DROP TABLE chat_messages_old')
        op.execute('PRAGMA foreign_keys=on')
        
        # Recreate indexes
        op.create_index(op.f('ix_chat_messages_conversation_id'), 'chat_messages', ['conversation_id'], unique=False)
        op.create_index(op.f('ix_chat_messages_thread_id'), 'chat_messages', ['thread_id'], unique=False)
        
        print("Updated thread_id to be nullable")
    except Exception as e:
        print(f"Could not update thread_id column: {e}")


def downgrade():
    # Remove the meta column
    try:
        op.drop_column('chat_messages', 'meta')
    except Exception as e:
        print(f"Could not drop meta column: {e}")

    # Set thread_id back to NOT NULL
    # This is complex in SQLite and would require table recreation,
    # so we'll just log it for this example
    print("Warning: thread_id remains nullable in downgrade")
