"""
Migration to remove operator role and update existing operator users to company role
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '20260225_remove_operator_role'
down_revision = '92b079f0dbab'
branch_labels = None
depends_on = None

def upgrade():
    # Update all existing operator users to company role
    op.execute("""
        UPDATE users 
        SET role = 'company' 
        WHERE role = 'operator'
    """)
    
    # Update company model comment to reflect new hierarchy
    op.execute("""
        ALTER TABLE companies 
        MODIFY COLUMN max_operators INT COMMENT 'Max company users allowed'
    """)

def downgrade():
    # Revert company users back to operator role
    op.execute("""
        UPDATE users 
        SET role = 'operator' 
        WHERE role = 'company'
    """)
    
    # Revert company model comment
    op.execute("""
        ALTER TABLE companies 
        MODIFY COLUMN max_operators INT COMMENT 'Max operators allowed for this company'
    """)
