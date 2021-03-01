"""Add Well Table

Revision ID: 6c78b1614df3
Revises: d44ebc9a7bd7
Create Date: 2021-03-01 16:42:55.063475

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c78b1614df3'
down_revision = 'd44ebc9a7bd7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Wells',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('well_id', sa.String(length=10), nullable=False),
    sa.Column('country', sa.String(length=100), nullable=False),
    sa.Column('district', sa.String(length=100), nullable=False),
    sa.Column('sub_district', sa.String(length=100), nullable=False),
    sa.Column('village', sa.String(length=100), nullable=False),
    sa.Column('latitude', sa.Float(), nullable=False),
    sa.Column('longitude', sa.Float(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_Wells_well_id'), 'Wells', ['well_id'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Wells_well_id'), table_name='Wells')
    op.drop_table('Wells')
    # ### end Alembic commands ###