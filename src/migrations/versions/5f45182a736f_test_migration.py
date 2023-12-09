"""test_migration

Revision ID: 5f45182a736f
Revises: 9f9c0dfb5e34
Create Date: 2023-12-09 07:21:53.570785

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5f45182a736f'
down_revision = '9f9c0dfb5e34'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=mysql.VARCHAR(length=24),
               type_=sa.VARCHAR(length=240),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('name',
               existing_type=sa.VARCHAR(length=240),
               type_=mysql.VARCHAR(length=24),
               existing_nullable=False)

    # ### end Alembic commands ###