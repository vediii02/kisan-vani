"""add_company_id_to_products

Revision ID: 20260227_add_company_id
Revises: 20260227_rmv_appr_cols
Create Date: 2026-02-27 18:50:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20260227_add_company_id'
down_revision = '20260227_rmv_appr_cols'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add company_id column to products table
    op.add_column('products', sa.Column('company_id', sa.Integer(), nullable=True))
    op.create_index('idx_company_id', 'products', ['company_id'])
    op.create_foreign_key('products', 'company_id', 'companies', ['id'], ondelete='CASCADE')


def downgrade() -> None:
    """Downgrade schema."""
    # Remove company_id column from products table
    op.drop_constraint('products', 'fk_products_company_id_companies')
    op.drop_index('idx_company_id', table_name='products')
    op.drop_column('products', 'company_id')
