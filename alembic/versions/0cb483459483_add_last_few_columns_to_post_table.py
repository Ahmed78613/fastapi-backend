"""add last few columns to post table

Revision ID: 0cb483459483
Revises: 2a6ae3578468
Create Date: 2023-03-16 13:31:21.600851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0cb483459483"
down_revision = "2a6ae3578468"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )
    pass


def downgrade():
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
    pass
