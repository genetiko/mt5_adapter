"""Create instruments table

Revision ID: fe63fe29ae84
Revises: db077cac85f3
Create Date: 2023-03-26 15:45:48.753755

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'fe63fe29ae84'
down_revision = 'db077cac85f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'instruments',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('terminal_id', sa.Integer, sa.ForeignKey('terminals.id', ondelete='CASCADE')),
        sa.Column('name', sa.String(32), nullable=False),
        sa.Column('path', sa.String(100), nullable=False),
        sa.Column('currency_base', sa.String(32), nullable=False),
        sa.Column('currency_profit', sa.String(32), nullable=False),
        sa.Column('currency_margin', sa.String(32), nullable=False),
        sa.UniqueConstraint('terminal_id', 'path', name='uc_terminal_path')
    )


def downgrade() -> None:
    op.drop_table('instruments')
