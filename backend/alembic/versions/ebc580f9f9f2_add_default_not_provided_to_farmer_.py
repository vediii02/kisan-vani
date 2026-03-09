"""add default not provided to farmer fields

Revision ID: ebc580f9f9f2
Revises: d59aeda63fec
Create Date: 2026-03-09 11:28:28.406827

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebc580f9f9f2'
down_revision: Union[str, Sequence[str], None] = 'd59aeda63fec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column('farmers', 'village', server_default='Not provided')
    op.alter_column('farmers', 'district', server_default='Not provided')
    op.alter_column('farmers', 'state', server_default='Not provided')
    op.alter_column('farmers', 'crop_type', server_default='Not provided')
    op.alter_column('farmers', 'land_size', server_default='Not provided')
    op.alter_column('farmers', 'crop_area', server_default='Not provided')
    op.alter_column('farmers', 'problem_area', server_default='Not provided')
    op.alter_column('farmers', 'crop_age_days', server_default='Not provided')

    op.execute("UPDATE farmers SET village = 'Not provided' WHERE village IS NULL")
    op.execute("UPDATE farmers SET district = 'Not provided' WHERE district IS NULL")
    op.execute("UPDATE farmers SET state = 'Not provided' WHERE state IS NULL")
    op.execute("UPDATE farmers SET crop_type = 'Not provided' WHERE crop_type IS NULL")
    op.execute("UPDATE farmers SET land_size = 'Not provided' WHERE land_size IS NULL")
    op.execute("UPDATE farmers SET crop_area = 'Not provided' WHERE crop_area IS NULL")
    op.execute("UPDATE farmers SET problem_area = 'Not provided' WHERE problem_area IS NULL")
    op.execute("UPDATE farmers SET crop_age_days = 'Not provided' WHERE crop_age_days IS NULL")

def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('farmers', 'village', server_default=None)
    op.alter_column('farmers', 'district', server_default=None)
    op.alter_column('farmers', 'state', server_default=None)
    op.alter_column('farmers', 'crop_type', server_default=None)
    op.alter_column('farmers', 'land_size', server_default=None)
    op.alter_column('farmers', 'crop_area', server_default=None)
    op.alter_column('farmers', 'problem_area', server_default=None)
    op.alter_column('farmers', 'crop_age_days', server_default=None)
