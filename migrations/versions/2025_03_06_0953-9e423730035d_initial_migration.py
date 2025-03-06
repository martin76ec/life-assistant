"""Initial migration

Revision ID: 9e423730035d
Revises:
Create Date: 2025-03-06 09:53:04.156251

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9e423730035d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
  # ### commands auto generated by Alembic - please adjust! ###
  op.create_table(
    "reminders",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("message", sa.Text(), nullable=True),
    sa.Column("reminder_date", sa.DateTime(), nullable=True),
    sa.Column("status", sa.String(length=20), server_default=sa.text("pending"), nullable=True),
    sa.Column("recurrence", sa.String(length=50), nullable=True),
    sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("(false)"), nullable=True),
    sa.PrimaryKeyConstraint("id", name="reminders_pkey"),
  )
  op.create_table(
    "spending_group",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("name", sa.String(length=100), nullable=True),
    sa.Column("description", sa.Text(), nullable=True),
    sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("(false)"), nullable=True),
    sa.PrimaryKeyConstraint("id", name="spending_group_pkey"),
  )
  op.create_table(
    "spendings",
    sa.Column("id", sa.Integer(), nullable=False),
    sa.Column("description", sa.Text(), nullable=True),
    sa.Column("total", sa.Numeric(precision=10, scale=2), nullable=True),
    sa.Column("date", sa.Date(), nullable=True),
    sa.Column("group_id", sa.Integer(), nullable=True),
    sa.Column("payment_method", sa.String(length=50), nullable=True),
    sa.Column("created_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column("updated_at", sa.DateTime(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=True),
    sa.Column("is_deleted", sa.Boolean(), server_default=sa.text("(false)"), nullable=True),
    sa.ForeignKeyConstraint(["group_id"], ["spending_group.id"], name="spendings_group_id_fkey"),
    sa.PrimaryKeyConstraint("id", name="spendings_pkey"),
  )
  # ### end Alembic commands ###


def downgrade() -> None:
  # ### commands auto generated by Alembic - please adjust! ###
  op.drop_table("spendings")
  op.drop_table("spending_group")
  op.drop_table("reminders")
  # ### end Alembic commands ###
