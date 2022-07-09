"""add addtl column to users table

Revision ID: 6ede0f3b416d
Revises: 45fae43a8dd4
Create Date: 2022-06-12 21:00:50.804684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ede0f3b416d'
down_revision = '45fae43a8dd4'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users_alembic',sa.Column('phone_number',sa.String(),nullable=False))
    pass


def downgrade():
    op.drop_column('users_alembic','phone_number')
    pass
