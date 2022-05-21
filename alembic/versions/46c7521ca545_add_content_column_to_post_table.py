"""add content column to post table

Revision ID: 46c7521ca545
Revises: 05feb3d63e60
Create Date: 2022-05-20 07:04:17.405236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '46c7521ca545'
down_revision = '05feb3d63e60'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
    pass
