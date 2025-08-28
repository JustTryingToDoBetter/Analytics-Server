"""create healthcheck table

Revision ID: 7d3f68fb1246
Revises: 
Create Date: 2025-08-28 10:24:50.222129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d3f68fb1246'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("healthcheck",
                    sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True),
                    sa.Column("note", sa.Text, nullable=True),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    pass


def downgrade() -> None:
    op.drop_table("healthcheck")
    pass
