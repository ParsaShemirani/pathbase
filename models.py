from __future__ import annotations

from datetime import datetime

from sqlalchemy import String, ForeignKey, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Action(Base):
    __tablename__ = "actions"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )

    name: Mapped[str] = mapped_column(String())

    action_segments: Mapped[list[ActionSegment]] = relationship(back_populates="action", init=False)


class ActionSegment(Base):
    __tablename__ = "action_segments"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"))

    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    action: Mapped[Action] = relationship(back_populates="action_segments", init=False)

    end_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )

"""
class TimeFrame(Base):
    __tablename__ = "time_frames"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )

    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ActionPlan(Base):
    __tablename__ = "action_plans"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )
    time_frame_id: Mapped[int] = mapped_column(ForeignKey("time_frames.id"))
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"))

    duration: Mapped[int] = mapped_column(Integer)

"""