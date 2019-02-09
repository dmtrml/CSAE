from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column(
        'session',
         sa.Column('is_active', sa.Boolean(), nullable=True)
    )
    op.execute("""
        UPDATE session
        SET is_active = 'f'
    """)
    op.alter_column('session', 'is_active', nullable=False)


def downgrade():
    op.drop_column('session', 'is_active')