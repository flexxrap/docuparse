"""add doc_type and parsed_data to documents

Revision ID: 0002
Revises: 0001
Create Date: 2026-06-15

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("doc_type", sa.String(length=20), nullable=True))
    op.add_column("documents", sa.Column("parsed_data", sa.JSON(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "parsed_data")
    op.drop_column("documents", "doc_type")
