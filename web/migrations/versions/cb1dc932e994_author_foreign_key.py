"""author foreign key

Revision ID: cb1dc932e994
Revises: 1c926fc58801
Create Date: 2020-06-01 09:04:53.868869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb1dc932e994'
down_revision = '1c926fc58801'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reminder', sa.Column('author_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'reminder', 'user', ['author_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reminder', type_='foreignkey')
    op.drop_column('reminder', 'author_id')
    # ### end Alembic commands ###