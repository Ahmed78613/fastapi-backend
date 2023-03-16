"""create posts table

Revision ID: 2766d268472e
Revises: 
Create Date: 2023-03-16 13:18:05.610140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2766d268472e"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("title", sa.String(), nullable=False),
    )
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
