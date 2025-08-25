from datetime import datetime, timezone

from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Action(Base):
    __tablename__ = "actions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String())

class ActionPlan(Base):
    __tablename__ = "action_plans"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"))

    duration: Mapped[int] = mapped_column(Integer)
    deadline: Mapped[datetime] = mapped_column(DateTime(timezone=True))

class ActionSegment(Base):
    __tablename__ = "action_segments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, init=False)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"))

    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)




"""
I will tie segments and plans to the same action.
Since plans are made with intention of being done within the 24
hour segment before them, it will add all segments in that timeframe
to calculate completed time.
"""