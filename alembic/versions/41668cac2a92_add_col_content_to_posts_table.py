"""add col content to posts table

Revision ID: 41668cac2a92
Revises: 2c651d5c5e5f
Create Date: 2022-06-04 21:55:48.367368

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41668cac2a92'
down_revision = '2c651d5c5e5f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts_alembic',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('posts_alembic','content')
    pass
