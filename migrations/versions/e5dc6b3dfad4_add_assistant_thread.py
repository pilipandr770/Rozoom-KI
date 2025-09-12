"""Add AssistantThread model

Revision ID: e5dc6b3dfad4
Revises: 
Create Date: 2023-10-31 14:32:45.123456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e5dc6b3dfad4'
down_revision = None  # This should be updated to your latest migration
branch_labels = None
depends_on = None


def upgrade():
    # Create assistant_threads table
    op.create_table('assistant_threads',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('conversation_id', sa.String(length=64), nullable=False),
        sa.Column('thread_id', sa.String(length=64), nullable=False),
        sa.Column('user_id', sa.String(length=64), nullable=True),
        sa.Column('language', sa.String(length=5), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('last_used_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('conversation_id'),
        sa.UniqueConstraint('thread_id')
    )
    
    # Create index on conversation_id for faster lookups
    op.create_index(op.f('ix_assistant_threads_conversation_id'), 'assistant_threads', ['conversation_id'], unique=True)


def downgrade():
    # Drop the table
    op.drop_index(op.f('ix_assistant_threads_conversation_id'), table_name='assistant_threads')
    op.drop_table('assistant_threads')
