"""create tenants table

Revision ID: 2ec40875f6c6
Revises: 
Create Date: 2026-02-11 06:36:44.568387

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '2ec40875f6c6'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('tenants',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('domain', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('active', 'inactive', 'suspended', name='tenantstatus'),nullable=False, server_default='active'), 
    sa.Column('is_active', sa.Boolean(), nullable=False, server_default=sa.text('true')),  # ✅ Add default
    sa.Column('created_source', sa.String(length=100), nullable=False, server_default='self_signup'),  # ✅ Add default
    sa.Column('data_region', sa.String(length=50), nullable=False, server_default='IN'),  # ✅ Add default
    sa.Column('timezone', sa.String(length=50), nullable=False, server_default='Asia/Kolkata'),  # ✅ Add default
    sa.Column('locale', sa.String(length=20), nullable=False, server_default='en_IN'),  # ✅ Add default
    sa.Column('tenant_metadata', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenants_created_at'), 'tenants', ['created_at'], unique=False)
    op.create_index(op.f('ix_tenants_domain'), 'tenants', ['domain'], unique=True)
    op.create_index(op.f('ix_tenants_id'), 'tenants', ['id'], unique=False)
    op.create_index(op.f('ix_tenants_status'), 'tenants', ['status'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_tenants_status'), table_name='tenants')
    op.drop_index(op.f('ix_tenants_id'), table_name='tenants')
    op.drop_index(op.f('ix_tenants_domain'), table_name='tenants')
    op.drop_index(op.f('ix_tenants_created_at'), table_name='tenants')
    op.drop_table('tenants')
    op.execute('DROP TYPE IF EXISTS tenantstatus')  # ✅ Add this