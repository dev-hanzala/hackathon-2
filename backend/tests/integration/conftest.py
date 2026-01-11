"""Pytest fixtures for integration testing."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

# Use in-memory SQLite for integration tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def integration_db_engine():
    """Create a test database engine for integration tests."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=None,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def integration_db_session(integration_db_engine):
    """Create a test database session for integration tests."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=integration_db_engine,
    )
    session = TestingSessionLocal()
    yield session
    session.close()
