"""Create instruments table

Revision ID: fe63fe29ae84
Revises: db077cac85f3
Create Date: 2023-03-26 15:45:48.753755

"""
from alembic import op
from sqlalchemy import Column, Integer, ForeignKey, String, Float, UniqueConstraint, Boolean

from terminals import settings

# revision identifiers, used by Alembic.
revision = 'fe63fe29ae84'
down_revision = 'db077cac85f3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'instruments',
        Column('id', Integer, primary_key=True),
        Column('source_id', Integer, ForeignKey('terminals.sources.id', ondelete='CASCADE')),
        Column('name', String(32), nullable=False),
        Column('path', String(100), nullable=False),
        Column('currency_base', String(32), nullable=False),
        Column('currency_profit', String(32), nullable=False),
        Column('currency_margin', String(32), nullable=False),
        Column('description', String(100), nullable=False),
        Column('digits', Integer, nullable=False),
        Column('volume_min', Float, nullable=False),
        Column('volume_max', Float, nullable=False),
        Column('volume_step', Float, nullable=False),
        Column('spread_floating', Boolean, nullable=False),
        UniqueConstraint('source_id', 'path', name='uc_terminal_path'),
        schema=settings.db.schema
    )

    def downgrade() -> None:
        op.drop_table('instruments')
