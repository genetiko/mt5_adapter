"""Create terminals table

Revision ID: db077cac85f3
Revises: 
Create Date: 2023-03-26 15:45:38.962555

"""
from alembic import op

from sqlalchemy import Column, Integer, String

from terminals import settings

# revision identifiers, used by Alembic.
revision = 'db077cac85f3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'sources',
        Column('id', Integer, primary_key=True),
        Column('name', String(200), nullable=False, unique=True),
        Column('server', String(200), nullable=False),
        schema=settings.db.schema
    )


def downgrade() -> None:
    op.drop_table('sources')
