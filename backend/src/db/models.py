"""SQLModel ORM model definitions."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    """User model for authentication."""

    id: Optional[UUID] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password_hash: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)


class Task(SQLModel, table=True):
    """Task model for todo items."""

    id: Optional[UUID] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    title: str = Field(max_length=500)
    completed: bool = Field(default=False, index=True)
    is_archived: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    user: Optional[User] = Relationship(back_populates="tasks")


class Session(SQLModel, table=True):
    """Session model for Better Auth integration."""

    id: Optional[UUID] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    token: str = Field(unique=True)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    def is_expired(self) -> bool:
        """Check if session is expired."""
        return datetime.utcnow() > self.expires_at
