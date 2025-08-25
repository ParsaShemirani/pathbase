


from datetime import datetime, timezone

from sqlalchemy import Integer, BigInteger, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Action(Base):
    __tablename__ = "actions"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String())



class ActionInstance(Base):
    __tablename__ = "action_instances"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"))

    planned_duration: Mapped[int | None] = mapped_column(Integer)
    planned_end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    recorded_duration: Mapped[int | None] = mapped_column(Integer)

class ActionInterval(Base):
    __tablename__ = "action_intervals"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    action_instance_id: Mapped[int] = mapped_column(ForeignKey("action_instances.id"))