"""Pydantic schemas for request/response validation."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# User Schemas
class UserBase(BaseModel):
    """Base user schema."""

    email: EmailStr


class UserCreate(UserBase):
    """Schema for user registration."""

    password: str = Field(min_length=8, max_length=255)


class UserSignIn(UserBase):
    """Schema for user login."""

    password: str = Field(min_length=1, max_length=255)


class UserResponse(UserBase):
    """Schema for user response."""

    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Task Schemas
class TaskBase(BaseModel):
    """Base task schema."""

    title: str = Field(min_length=1, max_length=500)


class TaskCreate(TaskBase):
    """Schema for task creation."""

    pass


class TaskUpdate(TaskBase):
    """Schema for task update."""

    pass


class TaskCompleteRequest(BaseModel):
    """Schema for marking task complete."""

    pass


class TaskIncompleteRequest(BaseModel):
    """Schema for marking task incomplete."""

    pass


class TaskResponse(TaskBase):
    """Schema for task response."""

    id: UUID
    user_id: UUID
    completed: bool
    is_archived: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# Session/Auth Schemas
class SessionResponse(BaseModel):
    """Schema for session/auth response."""

    token: str
    user: UserResponse
    expires_at: datetime


class AuthResponse(BaseModel):
    """Schema for auth endpoint response."""

    token: str
    user: UserResponse


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    detail: str
    code: Optional[str] = None
