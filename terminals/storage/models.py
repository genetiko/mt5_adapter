from sqlalchemy import ForeignKey, MetaData
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from terminals.config import settings


class Base(DeclarativeBase):
    metadata = MetaData(schema=settings.db.schema)


class Terminal(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    server: Mapped[str] = mapped_column()


class Instrument(Base):
    __tablename__ = "instruments"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"))
    name: Mapped[str] = mapped_column()
    path: Mapped[str] = mapped_column()
    currency_base: Mapped[str] = mapped_column()
    currency_margin: Mapped[str] = mapped_column()
    currency_profit: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    digits: Mapped[int] = mapped_column()
    volume_min: Mapped[float] = mapped_column()
    volume_max: Mapped[float] = mapped_column()
    volume_step: Mapped[float] = mapped_column()
    spread_floating: Mapped[bool] = mapped_column()
