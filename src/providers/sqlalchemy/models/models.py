from datetime import date, datetime
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Text, text
from sqlmodel import Field, Relationship, SQLModel


class Reminders(SQLModel, table=True):
  __table_args__ = (PrimaryKeyConstraint("id", name="reminders_pkey"),)

  id: Optional[int] = Field(default=None, sa_column=Column("id", Integer, primary_key=True))
  message: str = Field(sa_column=Column("message", Text))
  reminder_date: datetime = Field(sa_column=Column("reminder_date", DateTime))
  status: Optional[str] = Field(default=None, sa_column=Column("status", String(20), server_default=text("'pending'::character varying")))
  recurrence: Optional[str] = Field(default=None, sa_column=Column("recurrence", String(50)))
  created_at: Optional[datetime] = Field(default=None, sa_column=Column("created_at", DateTime, server_default=text("CURRENT_TIMESTAMP")))
  updated_at: Optional[datetime] = Field(default=None, sa_column=Column("updated_at", DateTime, server_default=text("CURRENT_TIMESTAMP")))
  is_deleted: Optional[bool] = Field(default=None, sa_column=Column("is_deleted", Boolean, server_default=text("false")))


class SpendingGroup(SQLModel, table=True):
  __tablename__ = "spending_group"
  __table_args__ = (PrimaryKeyConstraint("id", name="spending_group_pkey"),)

  id: Optional[int] = Field(default=None, sa_column=Column("id", Integer, primary_key=True))
  name: str = Field(sa_column=Column("name", String(100)))
  description: Optional[str] = Field(default=None, sa_column=Column("description", Text))
  created_at: Optional[datetime] = Field(default=None, sa_column=Column("created_at", DateTime, server_default=text("CURRENT_TIMESTAMP")))
  updated_at: Optional[datetime] = Field(default=None, sa_column=Column("updated_at", DateTime, server_default=text("CURRENT_TIMESTAMP")))
  is_deleted: Optional[bool] = Field(default=None, sa_column=Column("is_deleted", Boolean, server_default=text("false")))

  spendings: List["Spendings"] = Relationship(back_populates="group")


class Spendings(SQLModel, table=True):
  __table_args__ = (
    ForeignKeyConstraint(["group_id"], ["spending_group.id"], name="spendings_group_id_fkey"),
    PrimaryKeyConstraint("id", name="spendings_pkey"),
  )

  id: Optional[int] = Field(default=None, sa_column=Column("id", Integer, primary_key=True))
  description: str = Field(sa_column=Column("description", Text))
  total: Decimal = Field(sa_column=Column("total", Numeric(10, 2)))
  date_: date = Field(sa_column=Column("date", Date))
  group_id: Optional[int] = Field(default=None, sa_column=Column("group_id", Integer))
  payment_method: Optional[str] = Field(default=None, sa_column=Column("payment_method", String(50)))
  created_at: Optional[datetime] = Field(default=None, sa_column=Column("created_at", DateTime, server_default=text("CURRENT_TIMESTAMP")))
  updated_at: Optional[datetime] = Field(default=None, sa_column=Column("updated_at", DateTime, server_default=text("CURRENT_TIMESTAMP")))
  is_deleted: Optional[bool] = Field(default=None, sa_column=Column("is_deleted", Boolean, server_default=text("false")))

  group: Optional["SpendingGroup"] = Relationship(back_populates="spendings")
