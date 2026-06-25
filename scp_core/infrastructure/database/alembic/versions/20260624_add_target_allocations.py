"""Add target allocations and diligence run tables

Revision ID: 1a2b3c4d5e6f
Revises: 
Create Date: 2026-06-25 04:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1a2b3c4d5e6f'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('diligence_run',
        sa.Column('run_id', sa.String(), nullable=False),
        sa.Column('portfolio_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('portfolio.id')),
        sa.Column('run_date', sa.DateTime(), nullable=True),
        sa.Column('strategy_type', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('run_id')
    )
    
    op.create_table('run_artifact',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('run_id', sa.String(), sa.ForeignKey('diligence_run.run_id')),
        sa.Column('source_key', sa.String(), nullable=True),
        sa.Column('file_path', sa.String(), nullable=True),
        sa.Column('file_type', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('pm_exception',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ticker', sa.String(), nullable=True),
        sa.Column('approved_min', sa.Float(), nullable=True),
        sa.Column('approved_target', sa.Float(), nullable=True),
        sa.Column('approved_cap', sa.Float(), nullable=True),
        sa.Column('fiduciary_caveat', sa.String(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('target_allocation',
        sa.Column('ticker', sa.String(length=20), nullable=False),
        sa.Column('target_weight', sa.Float(), nullable=False),
        sa.Column('pm_exception_min', sa.Float(), nullable=True),
        sa.Column('pm_exception_max', sa.Float(), nullable=True),
        sa.Column('is_negative_nopat', sa.Boolean(), nullable=True),
        sa.Column('caveat_text', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('ticker')
    )

    op.create_table('pms_position_snapshot',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('ticker', sa.String(length=20), nullable=True),
        sa.Column('as_of_date', sa.Date(), nullable=True),
        sa.Column('current_weight', sa.Float(), nullable=True),
        sa.Column('implementation_gap', sa.Float(), nullable=True),
        sa.Column('band_status', sa.String(), nullable=True),
        sa.Column('daily_return', sa.Float(), nullable=True),
        sa.Column('governance_monitor_status', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('pms_position_snapshot')
    op.drop_table('target_allocation')
    op.drop_table('pm_exception')
    op.drop_table('run_artifact')
    op.drop_table('diligence_run')
