"""add graph processing state to chunks

Revision ID: 43cb6fb95c33
Revises: 45e5822a3ac6
Create Date: 2026-09-10 21:42:29.164699

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '43cb6fb95c33'
down_revision: str | Sequence[str] | None = '45e5822a3ac6'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""

    op.add_column(
        "chunks",
        sa.Column(
            "graph_processed",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )

    op.add_column(
        "chunks",
        sa.Column(
            "graph_processed_at",
            sa.DateTime(timezone=True),
            nullable=True,
        ),
    )

    op.create_index(
        op.f("ix_chunks_graph_processed"),
        "chunks",
        ["graph_processed"],
        unique=False,
    )

    # The temporary server default was only needed
    # to safely migrate existing rows.
    op.alter_column(
        "chunks",
        "graph_processed",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(
        op.f("ix_chunks_graph_processed"),
        table_name="chunks",
    )

    op.drop_column(
        "chunks",
        "graph_processed_at",
    )

    op.drop_column(
        "chunks",
        "graph_processed",
    )