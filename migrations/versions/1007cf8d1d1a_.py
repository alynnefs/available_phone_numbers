"""empty message

Revision ID: 1007cf8d1d1a
Revises: 
Create Date: 2021-01-20 22:51:26.417169

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1007cf8d1d1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('didnumber',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('value', sa.String(length=17), nullable=True),
    sa.Column('monthyPrice', sa.Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True),
    sa.Column('setupPrice', sa.Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True),
    sa.Column('currency', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('didnumber')
    # ### end Alembic commands ###
