from __future__ import annotations
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DATABASE_URL prioritaire, fallback SQLite fichier pour CI

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/dev.db")

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL, echo=False, future=True)
# Engine + SessionLocal initiaux (seront reconfigures via set_database_url en tests/app factory)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def set_database_url(url: str) -> None:
    """
    Reconfigure l engine/SessionLocal sur une nouvelle URL (utile pour tests).
    Idempotent; ferme l ancien engine si present.
    """
    global engine, SessionLocal, DATABASE_URL
    DATABASE_URL = url
    try:
        engine.dispose()
    except Exception:
        pass
    engine = create_engine(url, echo=False, future=True)
    SessionLocal.configure(bind=engine)

@contextmanager
def session_scope() -> Generator:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
