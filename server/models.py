from __future__ import annotations

from sqlalchemy import Integer, TEXT
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class ActionSegment(Base):
    __tablename__ = "action_segments"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )

    action_name: Mapped[str]
    start_at: Mapped[str] = mapped_column(TEXT)
    end_at: Mapped[str | None] = mapped_column(TEXT)
