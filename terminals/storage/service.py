from typing import List

from sqlalchemy.dialects.postgresql import insert

from terminals import SessionMaker
from .models import Terminal, Instrument


def insert_sources(sources):
    with SessionMaker() as session:
        session.execute(insert(Terminal)
                        .values(sources)
                        .on_conflict_do_nothing())
        session.commit()


def get_sources() -> List[Terminal]:
    with SessionMaker() as session:
        return session.query(Terminal).all()


def insert_instruments(instruments):
    with SessionMaker() as session:
        session.execute(insert(Instrument)
                        .values(instruments)
                        .on_conflict_do_nothing())
        session.commit()


def get_instruments(source_id) -> List[Instrument]:
    with SessionMaker() as session:
        return session.query(Instrument).where(Instrument.source_id == source_id).all()


def get_instrument(instrument_id):
    with SessionMaker() as session:
        return session.query(Instrument).get(instrument_id)
