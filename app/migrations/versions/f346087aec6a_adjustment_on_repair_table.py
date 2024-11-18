"""Adjustment on repair Table

Revision ID: f346087aec6a
Revises: 6f89c26a273a
Create Date: 2024-11-17 23:53:51.203785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f346087aec6a'
down_revision: Union[str, None] = '6f89c26a273a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('repair', 'timeSpent',
               existing_type=sa.DOUBLE_PRECISION(precision=53),
               type_=postgresql.INTERVAL(),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('repair', 'timeSpent',
               existing_type=postgresql.INTERVAL(),
               type_=sa.DOUBLE_PRECISION(precision=53),
               existing_nullable=True)
    # ### end Alembic commands ###
