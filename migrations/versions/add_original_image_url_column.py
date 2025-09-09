"""add_original_image_url_column

Revision ID: 002
Revises: 001
Create Date: 2025-09-09 19:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade():
    # Add original_image_url column to generated_content table
    op.add_column('generated_content', sa.Column('original_image_url', sa.String(500), nullable=True))
    
    # Add original_image_url column to blog_posts table
    op.add_column('blog_posts', sa.Column('original_image_url', sa.String(500), nullable=True))


def downgrade():
    # Drop columns
    op.drop_column('generated_content', 'original_image_url')
    op.drop_column('blog_posts', 'original_image_url')
