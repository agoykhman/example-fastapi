"""create post table

Revision ID: 05feb3d63e60
Revises: 
Create Date: 2022-05-20 06:47:45.030411

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05feb3d63e60'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',sa.Column('id', sa.Integer(), nullable = False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass


