




from sqlalchemy import BigInteger, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, Mapped, mapped_column

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Action(Base):
    __tablename__ = "actions"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(String(255))

class ActionInterval(Base):
    __tablename__ = "action_intervals"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True, init=False)
    action_id: Mapped[int] = mapped_column(ForeignKey("actions.id"))