"""remove_users_is_active_column

Revision ID: c7f2a0b3d4e5
Revises: 1ad08eebf8aa
Create Date: 2026-03-05 19:10:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7f2a0b3d4e5'
down_revision: Union[str, Sequence[str], None] = '1ad08eebf8aa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Remove is_active column from users table. Status column replaces it."""

    # First, sync existing data: set status based on is_active for any rows
    # where status might be NULL or inconsistent
    op.execute("""
        UPDATE users
        SET status = CASE
            WHEN status IS NOT NULL AND status != '' THEN status
            WHEN is_active = true THEN 'active'
            ELSE 'inactive'
        END
        WHERE status IS NULL OR status = ''
    """)

    # Now drop the is_active column
    op.drop_column('users', 'is_active')


def downgrade() -> None:
    """Re-add is_active column to users table."""
    op.add_column(
        'users',
        sa.Column('is_active', sa.Boolean(), server_default='true', nullable=True),
    )

    # Sync is_active from status
    op.execute("""
        UPDATE users
        SET is_active = CASE
            WHEN status = 'active' THEN true
            ELSE false
        END
    """)
