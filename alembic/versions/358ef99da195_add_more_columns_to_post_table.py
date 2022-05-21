"""add more columns to post table

Revision ID: 358ef99da195
Revises: f8e2827cdde9
Create Date: 2022-05-20 07:40:31.770281

"""
from re import M
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '358ef99da195'
down_revision = 'f8e2827cdde9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable = False, server_default = 'TRUE')),

    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True),
        server_default=sa.text('now()'), 
        nullable=False))

    pass


def downgrade():
    op.drop_column('posts', 'published'),
    op.drop_column('posts', 'created_at')
    pass
