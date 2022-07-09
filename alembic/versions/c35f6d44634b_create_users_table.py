"""create users table

Revision ID: c35f6d44634b
Revises: 41668cac2a92
Create Date: 2022-06-04 22:25:05.047573

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c35f6d44634b'
down_revision = '41668cac2a92'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users_alembic',
                     sa.Column('id',sa.Integer(),nullable=False,primary_key=True),
                     sa.Column('email',sa.String(),nullable=False),
                     sa.Column('password',sa.String(),nullable=False),
                     sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable='False',server_default=sa.text('now()')),
                     sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users_alembic')
    pass
