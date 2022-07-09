"""add foreign key constraint to posts table

Revision ID: d12a964135c6
Revises: c35f6d44634b
Create Date: 2022-06-06 23:54:12.894216

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd12a964135c6'
down_revision = 'c35f6d44634b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts_alembic',sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('posts_alembic_users_fk',source_table="posts_alembic",referent_table="users_alembic",local_cols=['owner_id'],remote_cols=['id'],ondelete="CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_alembic_users_fk',table_name="posts_alembic")
    op.drop_column('posts_alembic','owner_id')  
    pass
