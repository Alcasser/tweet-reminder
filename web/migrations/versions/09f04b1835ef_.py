"""empty message

Revision ID: 09f04b1835ef
Revises: 13434c08285f
Create Date: 2020-06-06 20:30:57.121344

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09f04b1835ef'
down_revision = '13434c08285f'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('reminder', 'reminder_status_id', type_=sa.BigInteger(), nullable=False)


def downgrade():
    op.alter_column('reminder', 'reminder_status_id', type_=sa.Integer(), nullable=False)
