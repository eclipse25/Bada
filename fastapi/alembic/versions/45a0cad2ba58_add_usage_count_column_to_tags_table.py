"""Add usage_count column to Tags table

Revision ID: 45a0cad2ba58
Revises: 55ff5d630c76
Create Date: 2024-05-21 14:25:06.128307

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45a0cad2ba58'
down_revision: Union[str, None] = '55ff5d630c76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_colleges_address'), 'colleges', ['address'], unique=False)
    op.create_index(op.f('ix_colleges_school_code'), 'colleges', ['school_code'], unique=False)
    op.create_index(op.f('ix_colleges_school_name'), 'colleges', ['school_name'], unique=False)
    op.add_column('tags', sa.Column('usage_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tags', 'usage_count')
    op.drop_index(op.f('ix_colleges_school_name'), table_name='colleges')
    op.drop_index(op.f('ix_colleges_school_code'), table_name='colleges')
    op.drop_index(op.f('ix_colleges_address'), table_name='colleges')
    # ### end Alembic commands ###
