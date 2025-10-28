from datetime import datetime, timezone, timedelta

from sqlalchemy import Integer, TEXT
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column

ISO_FMT_Z = "%Y-%m-%dT%H:%M:%S%z"


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class ActionSegment(Base):
    __tablename__ = "action_segments"
    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True, init=False
    )

    action_name: Mapped[str] = mapped_column(TEXT, nullable=False)
    str_start_at: Mapped[str] = mapped_column(TEXT, nullable=False, init=False)
    str_end_at: Mapped[str | None] = mapped_column(TEXT, nullable=True, init=False)

    @property
    def dt_start_at(self) -> datetime:
        return datetime.strptime(self.str_start_at, ISO_FMT_Z)

    @dt_start_at.setter
    def dt_start_at(self, dt: datetime):
        if dt.tzinfo is None:
            raise ValueError("datetime fields must be timezone aware")
        self.str_start_at = dt.strftime(ISO_FMT_Z)

    @property
    def dt_end_at(self) -> datetime | None:
        if self.str_end_at is not None:
            return datetime.strptime(self.str_end_at, ISO_FMT_Z)
        else:
            return None

    @dt_end_at.setter
    def dt_end_at(self, dt: datetime | None):
        if dt is None:
            self.str_end_at = None
        if dt.tzinfo is None:
            raise ValueError("datetime fields must be timezone aware")
        self.str_end_at = dt.strftime(ISO_FMT_Z)

    @property
    def duration(self) -> timedelta:
        if self.dt_end_at is not None:
            return self.dt_end_at - self.dt_start_at
        else:
            return datetime.now(tz=timezone.utc) - self.dt_start_at

    @property
    def str_duration(self) -> str:
        total_seconds = int(self.duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

class Tag(Base):
    ...