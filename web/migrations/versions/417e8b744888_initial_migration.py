"""Initial migration

Revision ID: 417e8b744888
Revises: 
Create Date: 2020-05-31 14:08:55.074105

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '417e8b744888'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reminder', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reminder', 'author_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###