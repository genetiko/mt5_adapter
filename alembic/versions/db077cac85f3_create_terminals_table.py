"""Create terminals table

Revision ID: db077cac85f3
Revises: 
Create Date: 2023-03-26 15:45:38.962555

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db077cac85f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'terminals',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(200), nullable=False),
        sa.Column('server', sa.String(200), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('terminals')
