"""Create column

Revision ID: a3f73dfb9bbe
Revises: 
Create Date: 2019-02-03 14:14:56.017349

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a3f73dfb9bbe'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column('subcategory', sa.String(70))
    )


def downgrade():
    pass
