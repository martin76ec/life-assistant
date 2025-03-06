from typing import List, Optional

from sqlalchemy import BigInteger, Boolean, Column, Date, DateTime, Double, ForeignKeyConstraint, Integer, Numeric, PrimaryKeyConstraint, String, Table, Text, text
from sqlalchemy.dialects.postgresql import OID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import datetime
import decimal

class Base(DeclarativeBase):
    pass


t_pg_stat_statements = Table(
    'pg_stat_statements', Base.metadata,
    Column('userid', OID),
    Column('dbid', OID),
    Column('toplevel', Boolean),
    Column('queryid', BigInteger),
    Column('query', Text),
    Column('plans', BigInteger),
    Column('total_plan_time', Double(53)),
    Column('min_plan_time', Double(53)),
    Column('max_plan_time', Double(53)),
    Column('mean_plan_time', Double(53)),
    Column('stddev_plan_time', Double(53)),
    Column('calls', BigInteger),
    Column('total_exec_time', Double(53)),
    Column('min_exec_time', Double(53)),
    Column('max_exec_time', Double(53)),
    Column('mean_exec_time', Double(53)),
    Column('stddev_exec_time', Double(53)),
    Column('rows', BigInteger),
    Column('shared_blks_hit', BigInteger),
    Column('shared_blks_read', BigInteger),
    Column('shared_blks_dirtied', BigInteger),
    Column('shared_blks_written', BigInteger),
    Column('local_blks_hit', BigInteger),
    Column('local_blks_read', BigInteger),
    Column('local_blks_dirtied', BigInteger),
    Column('local_blks_written', BigInteger),
    Column('temp_blks_read', BigInteger),
    Column('temp_blks_written', BigInteger),
    Column('blk_read_time', Double(53)),
    Column('blk_write_time', Double(53)),
    Column('temp_blk_read_time', Double(53)),
    Column('temp_blk_write_time', Double(53)),
    Column('wal_records', BigInteger),
    Column('wal_fpi', BigInteger),
    Column('wal_bytes', Numeric),
    Column('jit_functions', BigInteger),
    Column('jit_generation_time', Double(53)),
    Column('jit_inlining_count', BigInteger),
    Column('jit_inlining_time', Double(53)),
    Column('jit_optimization_count', BigInteger),
    Column('jit_optimization_time', Double(53)),
    Column('jit_emission_count', BigInteger),
    Column('jit_emission_time', Double(53))
)


t_pg_stat_statements_info = Table(
    'pg_stat_statements_info', Base.metadata,
    Column('dealloc', BigInteger),
    Column('stats_reset', DateTime(True))
)


class Reminders(Base):
    __tablename__ = 'reminders'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='reminders_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message: Mapped[str] = mapped_column(Text)
    reminder_date: Mapped[datetime.datetime] = mapped_column(DateTime)
    status: Mapped[Optional[str]] = mapped_column(String(20), server_default=text("'pending'::character varying"))
    recurrence: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))


class SpendingGroup(Base):
    __tablename__ = 'spending_group'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='spending_group_pkey'),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(Text)
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    spendings: Mapped[List['Spendings']] = relationship('Spendings', back_populates='group')


class Spendings(Base):
    __tablename__ = 'spendings'
    __table_args__ = (
        ForeignKeyConstraint(['group_id'], ['spending_group.id'], name='spendings_group_id_fkey'),
        PrimaryKeyConstraint('id', name='spendings_pkey')
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    total: Mapped[decimal.Decimal] = mapped_column(Numeric(10, 2))
    date: Mapped[datetime.date] = mapped_column(Date)
    group_id: Mapped[Optional[int]] = mapped_column(Integer)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50))
    created_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    is_deleted: Mapped[Optional[bool]] = mapped_column(Boolean, server_default=text('false'))

    group: Mapped[Optional['SpendingGroup']] = relationship('SpendingGroup', back_populates='spendings')
