"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-05-08

"""
from alembic import op
import sqlalchemy as sa

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True, index=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.Enum('admin', 'analyst', 'viewer', name='user_role'), nullable=False, server_default='analyst'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'uploads',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('filename', sa.String(255), nullable=False),
        sa.Column('dataset_type', sa.Enum('procurement', 'supplier', 'inventory', 'budget', name='dataset_type'), nullable=False),
        sa.Column('status', sa.Enum('pending', 'processing', 'valid', 'invalid', name='upload_status'), nullable=False, server_default='pending'),
        sa.Column('row_count', sa.Integer(), nullable=False, server_default='0'),
        sa.Column('error_log', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        'procurement_transactions',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('upload_id', sa.Integer(), sa.ForeignKey('uploads.id'), nullable=False, index=True),
        sa.Column('transaction_id', sa.String(100), nullable=True),
        sa.Column('date', sa.Date(), nullable=True, index=True),
        sa.Column('category', sa.String(200), nullable=True, index=True),
        sa.Column('product', sa.String(200), nullable=True),
        sa.Column('supplier', sa.String(200), nullable=True, index=True),
        sa.Column('quantity', sa.Float(), nullable=True),
        sa.Column('unit_cost', sa.Float(), nullable=True),
        sa.Column('total_cost', sa.Float(), nullable=True),
        sa.Column('region', sa.String(100), nullable=True),
        sa.Column('warehouse', sa.String(100), nullable=True),
    )

    op.create_table(
        'suppliers',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('upload_id', sa.Integer(), sa.ForeignKey('uploads.id'), nullable=False, index=True),
        sa.Column('supplier_name', sa.String(200), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('lead_time', sa.Float(), nullable=True),
        sa.Column('contract_value', sa.Float(), nullable=True),
        sa.Column('risk_level', sa.String(50), nullable=True),
        sa.Column('performance_rating', sa.Float(), nullable=True),
    )

    op.create_table(
        'inventory_items',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('upload_id', sa.Integer(), sa.ForeignKey('uploads.id'), nullable=False, index=True),
        sa.Column('product', sa.String(200), nullable=True),
        sa.Column('category', sa.String(200), nullable=True),
        sa.Column('stock_level', sa.Float(), nullable=True),
        sa.Column('reorder_level', sa.Float(), nullable=True),
        sa.Column('warehouse', sa.String(100), nullable=True),
        sa.Column('inventory_value', sa.Float(), nullable=True),
    )

    op.create_table(
        'budget_records',
        sa.Column('id', sa.Integer(), primary_key=True, index=True),
        sa.Column('upload_id', sa.Integer(), sa.ForeignKey('uploads.id'), nullable=False, index=True),
        sa.Column('category', sa.String(200), nullable=True),
        sa.Column('budget', sa.Float(), nullable=True),
        sa.Column('actual_spend', sa.Float(), nullable=True),
        sa.Column('variance', sa.Float(), nullable=True),
        sa.Column('region', sa.String(100), nullable=True),
    )


def downgrade() -> None:
    op.drop_table('budget_records')
    op.drop_table('inventory_items')
    op.drop_table('suppliers')
    op.drop_table('procurement_transactions')
    op.drop_table('uploads')
    op.drop_table('users')
    op.execute('DROP TYPE IF EXISTS upload_status')
    op.execute('DROP TYPE IF EXISTS dataset_type')
    op.execute('DROP TYPE IF EXISTS user_role')
