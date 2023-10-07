"""add foreign-key

Revision ID: e18bf024a368
Revises: e5fa5fb7f9d4
Create Date: 2023-10-07 13:42:36.209208

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e18bf024a368'
down_revision: Union[str, None] = 'e5fa5fb7f9d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table='posts',
                          referent_table='users', local_cols=['user_id'], remote_cols=['id'], ondelete="CASCADE")


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
