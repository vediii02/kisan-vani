"""rename_primary_phone_to_phone_number

Revision ID: ad1ba727adac
Revises: 20260227_add_company_id
Create Date: 2026-02-28 10:11:27.489137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad1ba727adac'
down_revision: Union[str, Sequence[str], None] = '20260227_add_company_id'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
