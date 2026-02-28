"""remove_approval_columns_from_products

Revision ID: 20260227_rmv_appr_cols
Revises: 20260227_add_website_and_description
Create Date: 2026-02-27 18:38:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260227_rmv_appr_cols'
down_revision = '20260227_add_website_and_description'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove approval-related columns from products table
    op.drop_column('products', 'approval_status')
    op.drop_column('products', 'approved_by')
    op.drop_column('products', 'approved_at')
    op.drop_column('products', 'ban_reason')


def downgrade() -> None:
    """Downgrade schema."""
    # Add back approval-related columns to products table
    op.add_column('products', sa.Column('approval_status', sa.Enum('pending', 'approved', 'banned'), nullable=True, server_default='pending'))
    op.add_column('products', sa.Column('approved_by', sa.Integer(), nullable=True))
    op.add_column('products', sa.Column('approved_at', sa.DateTime(), nullable=True))
    op.add_column('products', sa.Column('ban_reason', sa.Text(), nullable=True))
