"""add created time to users table

Revision ID: 83acaa2d5737
Revises: 8e10c7b8d018
Create Date: 2021-06-29 16:36:03.169389

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '83acaa2d5737'
down_revision = '8e10c7b8d018'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('created_on', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('updated_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'updated_on')
    op.drop_column('user', 'created_on')
    # ### end Alembic commands ###
