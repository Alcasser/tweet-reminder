"""empty message

Revision ID: 697c5242454b
Revises: ba98311c68e4
Create Date: 2020-06-14 13:42:42.280826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '697c5242454b'
down_revision = 'ba98311c68e4'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('user', 'external_id', type_=sa.BigInteger())


def downgrade():
    op.alter_column('user', 'external_id', type_=sa.Integer())
