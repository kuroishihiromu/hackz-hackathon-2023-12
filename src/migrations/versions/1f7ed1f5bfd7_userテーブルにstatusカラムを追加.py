"""userテーブルにstatusカラムを追加

Revision ID: 1f7ed1f5bfd7
Revises: f8afa49eb502
Create Date: 2023-12-12 08:49:20.544545

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1f7ed1f5bfd7'
down_revision = 'f8afa49eb502'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('status', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('status')

    # ### end Alembic commands ###
