"""add addtl cols to posts_alembic table

Revision ID: 45fae43a8dd4
Revises: d12a964135c6
Create Date: 2022-06-07 00:09:46.732491

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45fae43a8dd4'
down_revision = 'd12a964135c6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts_alembic',sa.Column('published',sa.Boolean(),nullable=False,server_default='TRUE'))
    op.add_column('posts_alembic',sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable='False',server_default=sa.text('now()')))
    pass


def downgrade():
    op.drop_column('posts_alembic','published')
    op.drop_column('posts_alembic','created_at')

    pass
