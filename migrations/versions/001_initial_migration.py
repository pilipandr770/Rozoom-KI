"""Initial migration

Revision ID: 001
Revises: 
Create Date: 2025-09-08 16:56:07.446498

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Add conversation_id column to chat_messages table
    op.add_column('chat_messages', sa.Column('conversation_id', sa.String(36), nullable=True))
    op.create_index(op.f('ix_chat_messages_conversation_id'), 'chat_messages', ['conversation_id'], unique=False)


def downgrade():
    # Remove conversation_id column from chat_messages table
    op.drop_index(op.f('ix_chat_messages_conversation_id'), table_name='chat_messages')
    op.drop_column('chat_messages', 'conversation_id')
