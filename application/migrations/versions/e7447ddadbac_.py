"""empty message

Revision ID: e7447ddadbac
Revises: 
Create Date: 2021-01-24 11:17:57.374721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7447ddadbac'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('did_number',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('value', sa.String(length=17), nullable=True),
    sa.Column('monthyPrice', sa.Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True),
    sa.Column('setupPrice', sa.Numeric(precision=8, scale=2, decimal_return_scale=2), nullable=True),
    sa.Column('currency', sa.String(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_login',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('public_id', sa.String(length=255), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_login')
    op.drop_table('did_number')
    # ### end Alembic commands ###
