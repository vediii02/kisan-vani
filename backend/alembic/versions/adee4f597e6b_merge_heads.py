"""merge_heads

Revision ID: adee4f597e6b
Revises: 042ea2385a50, c7f2a0b3d4e5
Create Date: 2026-03-06 12:49:33.456034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'adee4f597e6b'
down_revision: Union[str, Sequence[str], None] = ('042ea2385a50', 'c7f2a0b3d4e5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
