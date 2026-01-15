"""Database connection and session management."""

import os
from sqlalchemy import create_engine, pool
from sqlmodel import Session, SQLModel

from src.config import settings

# Lazy-load engine to avoid import-time connection issues
_engine = None


def get_engine():
    """Get or create database engine."""
    global _engine
    if _engine is None:
        # Use test database URL if in test mode
        database_url = os.getenv("TEST_DATABASE_URL") or settings.database_url

        # Create engine with connection pooling
        _engine = create_engine(
            database_url,
            echo=settings.debug,
            poolclass=pool.QueuePool,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            connect_args={"connect_timeout": 10} if "postgresql" in database_url else {},
        )
    return _engine


def get_session():
    """Get a database session."""
    engine = get_engine()
    with Session(engine) as session:
        yield session


def init_db():
    """Initialize database tables."""
    engine = get_engine()
    SQLModel.metadata.create_all(engine)
