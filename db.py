'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
'''

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()

_engine = None
_SessionLocal = None

def _ensure_engine():
    global _engine, _SessionLocal
    if _engine is None:
        url = os.getenv("DATABASE_URL")
        if not url:
            # Mensaje claro en logs y evita crash de import
            raise RuntimeError("DATABASE_URL no definida. Añádela en Vercel → Settings → Environment Variables.")
        _engine = create_engine(url, pool_pre_ping=True)
        _SessionLocal = sessionmaker(bind=_engine, autocommit=False, autoflush=False)

def get_db():
    _ensure_engine()
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()