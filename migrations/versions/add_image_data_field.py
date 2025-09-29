"""Add image_data field to BlogPost for storing images in database

Revision ID: add_image_data_field
Revises: f456ad120936
Create Date: 2025-09-29 23:06:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'add_image_data_field'
down_revision = 'f456ad120936'
branch_labels = None
depends_on = None


def upgrade():
    # Add image_data column to blog_posts table
    op.add_column('blog_posts', sa.Column('image_data', sa.LargeBinary(), nullable=True))
    # Add image_data column to generated_content table
    op.add_column('generated_content', sa.Column('image_data', sa.LargeBinary(), nullable=True))


def downgrade():
    # Remove image_data column from blog_posts table
    op.drop_column('blog_posts', 'image_data')
    # Remove image_data column from generated_content table
    op.drop_column('generated_content', 'image_data')