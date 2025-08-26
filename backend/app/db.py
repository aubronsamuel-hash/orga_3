from __future__ import annotations
import os
from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# DATABASE_URL prioritaire, fallback SQLite fichier pour CI jalon 2

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./backend/dev.db")

class Base(DeclarativeBase):
    pass

engine = create_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

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
