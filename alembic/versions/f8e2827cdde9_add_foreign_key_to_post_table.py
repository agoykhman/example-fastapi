"""add foreign-key to post table

Revision ID: f8e2827cdde9
Revises: 5d5d849e8591
Create Date: 2022-05-20 07:30:45.988036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f8e2827cdde9'
down_revision = '5d5d849e8591'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts',sa.Column('user_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk', source_table = 'posts', 
        referent_table = 'users', 
        local_cols = ['user_id'], 
        remote_cols = ['id'], 
        ondelete = 'CASCADE')
    pass


def downgrade():
    op.drop_constraint('post_users_fk', 'posts'),
    op.drop_column('posts','user_id')
    pass
