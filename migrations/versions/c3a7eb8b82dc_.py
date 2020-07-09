"""empty message

Revision ID: c3a7eb8b82dc
Revises: 
Create Date: 2020-06-28 17:44:55.418750

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3a7eb8b82dc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('avi_url', sa.Text(), nullable=True),
    sa.Column('username', sa.String(length=20), nullable=False),
    sa.Column('h_password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('bio', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('containers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('admin_id', sa.Integer(), nullable=True),
    sa.Column('is_channel', sa.Boolean(), nullable=False),
    sa.Column('title', sa.String(length=25), nullable=False),
    sa.Column('topic', sa.Text(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['admin_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('container_users',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('container_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['container_id'], ['containers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'container_id')
    )
    op.create_table('messages',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('container_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.Text(), nullable=False),
    sa.Column('created_on', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['container_id'], ['containers.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('messages')
    op.drop_table('container_users')
    op.drop_table('containers')
    op.drop_table('users')
    # ### end Alembic commands ###