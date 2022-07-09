"""create posts table

Revision ID: 2c651d5c5e5f
Revises: 
Create Date: 2022-06-04 21:32:12.487985

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c651d5c5e5f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts_alembic',sa.Column('id',sa.Integer(),nullable=False,primary_key=True),sa.Column('title',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_table('posts_alembic')
    pass
