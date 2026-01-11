"""Database connection and session management."""

from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from src.config import settings

# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    poolclass=pool.QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    connect_args={"connect_timeout": 10},
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_session():
    """Get a database session."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db():
    """Initialize database tables."""
    SQLModel.metadata.create_all(engine)
