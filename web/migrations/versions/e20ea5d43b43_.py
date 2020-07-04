"""empty message

Revision ID: e20ea5d43b43
Revises: ad33d0351f2d
Create Date: 2020-06-05 19:58:51.352363

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e20ea5d43b43'
down_revision = 'ad33d0351f2d'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('reminder', sa.Column('reminder_status_id', sa.BigInteger(), nullable=False))


def downgrade():
    op.add_column('reminder', sa.Column('reminder_status_id', sa.Integer(), nullable=False))
