"""Pydantic schemas for request/response validation."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


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
    code: str | None = None


# Chat Schemas
class ChatMessage(BaseModel):
    """A single chat message."""

    role: str = Field(description="Message role: 'user', 'assistant', or 'system'")
    content: str = Field(min_length=1, description="Message content")


class ChatRequest(BaseModel):
    """Schema for chat completion request."""

    messages: list[ChatMessage] = Field(min_length=1, description="Conversation messages")
    model: str | None = Field(default=None, description="Model override (defaults to server config)")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    max_tokens: int | None = Field(default=None, gt=0, description="Max tokens in response")


class ChatResponse(BaseModel):
    """Schema for chat completion response."""

    response: str = Field(description="The assistant's response text")
    model: str = Field(description="Model used for the response")
