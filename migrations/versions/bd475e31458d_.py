"""empty message

Revision ID: bd475e31458d
Revises: ed51ae152adb
Create Date: 2020-05-04 14:54:14.853367

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd475e31458d'
down_revision = 'ed51ae152adb'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('probability', sa.String(length=512), nullable=False))
    op.add_column('user', sa.Column('zone', sa.String(length=512), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'zone')
    op.drop_column('user', 'probability')
    # ### end Alembic commands ###
