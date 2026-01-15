"""SQLModel ORM model definitions."""

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """User model for authentication."""

    __tablename__ = "user"  # Explicit table name

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)


class Task(SQLModel, table=True):
    """Task model for todo items."""

    __tablename__ = "task"  # Explicit table name

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=500)
    completed: bool = Field(default=False, index=True)
    is_archived: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), index=True)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    # Relationships
    user: User | None = Relationship(back_populates="tasks")


class Session(SQLModel, table=True):
    """Session model for Better Auth integration."""

    __tablename__ = "session"  # Explicit table name

    id: UUID | None = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    token: str = Field(unique=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.now(UTC) > self.expires_at
