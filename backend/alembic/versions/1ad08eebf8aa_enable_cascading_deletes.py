"""enable_cascading_deletes

Revision ID: 1ad08eebf8aa
Revises: bbe26bb415c3
Create Date: 2026-03-05 12:03:57.963338

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ad08eebf8aa'
down_revision: Union[str, Sequence[str], None] = 'bbe26bb415c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add ON DELETE CASCADE to FK constraints and add users.status column."""

    # --- 1. users.organisation_id → organisations.id (CASCADE) ---
    op.drop_constraint(
        'users_organisation_id_fkey', 'users', type_='foreignkey'
    )
    op.create_foreign_key(
        'users_organisation_id_fkey', 'users',
        'organisations', ['organisation_id'], ['id'],
        ondelete='CASCADE',
    )

    # --- 2. users.company_id → companies.id (CASCADE) ---
    op.drop_constraint(
        'users_company_id_fkey', 'users', type_='foreignkey'
    )
    op.create_foreign_key(
        'users_company_id_fkey', 'users',
        'companies', ['company_id'], ['id'],
        ondelete='CASCADE',
    )

    # --- 3. kb_entries.organisation_id → organisations.id (CASCADE) ---
    op.drop_constraint(
        'kb_entries_organisation_id_fkey', 'kb_entries', type_='foreignkey'
    )
    op.create_foreign_key(
        'kb_entries_organisation_id_fkey', 'kb_entries',
        'organisations', ['organisation_id'], ['id'],
        ondelete='CASCADE',
    )

    # --- 4. organisation_kb_files.organisation_id → organisations.id (CASCADE) ---
    op.drop_constraint(
        'organisation_kb_files_organisation_id_fkey', 'organisation_kb_files',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'organisation_kb_files_organisation_id_fkey', 'organisation_kb_files',
        'organisations', ['organisation_id'], ['id'],
        ondelete='CASCADE',
    )

    # --- 5. Add status column to users ---
    op.add_column(
        'users',
        sa.Column('status', sa.String(length=20), server_default='active', nullable=True),
    )


def downgrade() -> None:
    """Revert cascading deletes and remove users.status column."""

    # Remove status column
    op.drop_column('users', 'status')

    # Revert organisation_kb_files FK
    op.drop_constraint(
        'organisation_kb_files_organisation_id_fkey', 'organisation_kb_files',
        type_='foreignkey',
    )
    op.create_foreign_key(
        'organisation_kb_files_organisation_id_fkey', 'organisation_kb_files',
        'organisations', ['organisation_id'], ['id'],
    )

    # Revert kb_entries FK
    op.drop_constraint(
        'kb_entries_organisation_id_fkey', 'kb_entries', type_='foreignkey'
    )
    op.create_foreign_key(
        'kb_entries_organisation_id_fkey', 'kb_entries',
        'organisations', ['organisation_id'], ['id'],
    )

    # Revert users.company_id FK
    op.drop_constraint(
        'users_company_id_fkey', 'users', type_='foreignkey'
    )
    op.create_foreign_key(
        'users_company_id_fkey', 'users',
        'companies', ['company_id'], ['id'],
    )

    # Revert users.organisation_id FK
    op.drop_constraint(
        'users_organisation_id_fkey', 'users', type_='foreignkey'
    )
    op.create_foreign_key(
        'users_organisation_id_fkey', 'users',
        'organisations', ['organisation_id'], ['id'],
    )
