"""Pytest fixtures for backend testing."""

from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import create_engine, event
from sqlmodel import Session, SQLModel

from src.db.database import get_session
from src.db.models import Session as SessionModel
from src.db.models import Task, User
from src.main import app
from src.middleware.auth import create_access_token, get_password_hash

# Use in-memory SQLite for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_engine():
    """Create a test database engine."""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

    # Enable foreign key support for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, _connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create a test database session."""
    with Session(db_engine) as session:
        yield session


@pytest.fixture(scope="function")
def override_get_session(db_session):
    """Override the get_session dependency."""

    def _override_get_session():
        try:
            yield db_session
        finally:
            pass

    return _override_get_session


@pytest_asyncio.fixture(scope="function")
async def client(db_session, override_get_session):
    """Create an async test client."""
    # db_session is needed to set up the database tables, but not used directly
    _ = db_session  # Explicitly mark as intentionally unused
    app.dependency_overrides[get_session] = override_get_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(db_session):
    """Create a test user with unhashed password."""
    # This user has a raw hash that won't work for authentication testing
    user = User(
        email="raw_test@example.com",
        password_hash="hashed_password_123",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def registered_user(db_session):
    """Create a test user with properly hashed password for auth testing."""
    password_hash = get_password_hash("TestPassword123")
    user = User(
        email="test@example.com",
        password_hash=password_hash,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def auth_token(registered_user):
    """Create a valid JWT token for the registered user."""
    token = create_access_token(data={"sub": str(registered_user.id), "email": registered_user.email})
    return token


@pytest.fixture
def auth_headers(auth_token):
    """Create authorization headers with valid JWT token."""
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
def test_user_session(db_session, test_user):
    """Create a test session for auth (legacy fixture)."""
    session = SessionModel(
        user_id=test_user.id,
        token=f"test_token_{uuid4()}",
        expires_at=datetime.now(UTC) + timedelta(hours=1),
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
