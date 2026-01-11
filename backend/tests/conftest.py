"""Pytest fixtures for backend testing."""

import os
from datetime import datetime, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session, SQLModel

from src.db.models import Session as SessionModel
from src.db.models import Task, User
from src.main import app

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=None,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a test database session."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture(scope="function")
def test_client(db_session):
    """Create a test client."""

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_session] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user."""
    user = User(
        email="test@example.com",
        password_hash="hashed_password_123",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_session(db_session, test_user):
    """Create a test session for auth."""
    session = SessionModel(
        user_id=test_user.id,
        token=f"test_token_{uuid4()}",
        expires_at=datetime.utcnow() + timedelta(hours=1),
    )
    db_session.add(session)
    db_session.commit()
    db_session.refresh(session)
    return session


@pytest.fixture
def test_task(db_session, test_user):
    """Create a test task."""
    task = Task(
        user_id=test_user.id,
        title="Test Task",
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)
    return task


@pytest.fixture
def auth_headers(test_user_session):
    """Create authorization headers for a test session."""
    return {"Authorization": f"Bearer {test_user_session.token}"}


def get_session():
    """Placeholder for dependency."""
    pass
