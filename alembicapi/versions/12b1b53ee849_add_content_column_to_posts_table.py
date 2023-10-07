"""add content column to posts table

Revision ID: 12b1b53ee849
Revises: 280c54fd4609
Create Date: 2023-10-07 13:21:52.110889

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '12b1b53ee849'
down_revision: Union[str, None] = '280c54fd4609'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'content')
