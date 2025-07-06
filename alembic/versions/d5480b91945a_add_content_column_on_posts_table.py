"""add content column on posts table

Revision ID: d5480b91945a
Revises: 5ea6a2d13bc9
Create Date: 2025-07-06 16:05:15.400744

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5480b91945a'
down_revision: Union[str, Sequence[str], None] = '5ea6a2d13bc9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('post_type', sa.String(length=100), nullable=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'post_type')
    pass
