"""Add website_link and description fields to organisation and company models

Revision ID: 20260227_add_website_and_description
Revises: ac1c1e5caf25
Create Date: 2026-02-27 15:57:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '20260227_add_website_and_description'
down_revision: Union[str, Sequence[str], None] = 'ac1c1e5caf25'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add website_link and description to organisations table
    op.add_column('organisations', sa.Column('website_link', sa.String(length=500), nullable=True))
    op.add_column('organisations', sa.Column('description', sa.Text(), nullable=True))
    
    # Add website_link and description to companies table
    op.add_column('companies', sa.Column('website_link', sa.String(length=500), nullable=True))
    op.add_column('companies', sa.Column('description', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove website_link and description from organisations table
    op.drop_column('organisations', 'description')
    op.drop_column('organisations', 'website_link')
    
    # Remove website_link and description from companies table
    op.drop_column('companies', 'description')
    op.drop_column('companies', 'website_link')
