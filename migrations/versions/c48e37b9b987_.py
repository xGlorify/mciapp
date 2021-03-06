"""empty message

Revision ID: c48e37b9b987
Revises: 387f057afe9a
Create Date: 2017-08-03 13:03:37.754728

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c48e37b9b987'
down_revision = '387f057afe9a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('materials', sa.Column('Attachment', sa.String(length=100), nullable=True))
    op.drop_column('workorder', 'Attachment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('workorder', sa.Column('Attachment', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('materials', 'Attachment')
    # ### end Alembic commands ###
