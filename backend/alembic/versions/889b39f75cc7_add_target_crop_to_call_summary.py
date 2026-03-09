"""add target crop to call summary

Revision ID: 889b39f75cc7
Revises: a1b2c3d4e5f6
Create Date: 2026-03-07 12:55:42.167737

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '889b39f75cc7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('call_summaries', sa.Column('target_crop', sa.String(length=100), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('call_summaries', 'target_crop')
