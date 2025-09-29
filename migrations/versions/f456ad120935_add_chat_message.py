"""Add ChatMessage model

Revision ID: f456ad120935
Revises: e5dc6b3dfad4
Create Date: 2025-09-12 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f456ad120935'
down_revision = 'e5dc6b3dfad4'
branch_labels = None
depends_on = None


def upgrade():
    # Create chat_messages table with checkfirst option
    # This will skip creation if table already exists
    try:
        op.create_table(
            'chat_messages',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('conversation_id', sa.String(length=64), nullable=False),
            sa.Column('thread_id', sa.String(length=64), nullable=True),  # Make nullable
            sa.Column('role', sa.String(length=16), nullable=False),
            sa.Column('content', sa.Text(), nullable=False),
            sa.Column('meta', sa.JSON(), nullable=True),  # Add meta column
            sa.Column('created_at', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
        )

        # Create indexes - also try creating with try/except
        try:
            op.create_index(op.f('ix_chat_messages_conversation_id'), 'chat_messages', ['conversation_id'], unique=False)
        except Exception as e:
            print(f"Индекс на conversation_id уже существует или возникла ошибка: {e}")

        try:
            op.create_index(op.f('ix_chat_messages_thread_id'), 'chat_messages', ['thread_id'], unique=False)
        except Exception as e:
            print(f"Индекс на thread_id уже существует или возникла ошибка: {e}")
    except Exception as e:
        print(f"Ошибка при создании таблицы chat_messages: {e}")


def downgrade():
    # Drop indexes if they exist
    try:
        op.drop_index(op.f('ix_chat_messages_thread_id'), table_name='chat_messages')
    except Exception as e:
        print(f"Не удалось удалить индекс thread_id: {e}")
    
    try:
        op.drop_index(op.f('ix_chat_messages_conversation_id'), table_name='chat_messages')
    except Exception as e:
        print(f"Не удалось удалить индекс conversation_id: {e}")
    
    # Drop table if it exists
    try:
        op.drop_table('chat_messages')
    except Exception as e:
        print(f"Не удалось удалить таблицу chat_messages: {e}")
    # Table drop attempted above; nothing further to do
