"""Authentication service for user management.

T039: Authentication service with registration, signin, logout, session validation.
"""

from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.config import settings
from src.db.models import Session as SessionModel
from src.db.models import User
from src.middleware.auth import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from src.services.db_service import DBService


class AuthService:
    """Authentication service for user management."""

    @staticmethod
    def register_user(db: Session, email: str, password: str) -> tuple[User, str]:
        """Register a new user and return user with access token.

        Args:
            db: Database session
            email: User email address
            password: Plain text password (will be hashed)

        Returns:
            Tuple of (User, access_token)

        Raises:
            HTTPException: If email already registered (409)
        """
        # Check if user already exists
        existing_user = DBService.get_user_by_email(db, email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered",
            )

        # Hash password and create user
        hashed_password = get_password_hash(password)
        user = DBService.create_user(db, email, hashed_password)

        # Create access token for auto-login after registration
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

        return user, access_token

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> tuple[User, str]:
        """Authenticate user with email and password.

        Args:
            db: Database session
            email: User email address
            password: Plain text password

        Returns:
            Tuple of (User, access_token)

        Raises:
            HTTPException: If credentials are invalid (401)
        """
        user = DBService.get_user_by_email(db, email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )

        # Create access token
        access_token = create_access_token(data={"sub": str(user.id), "email": user.email})

        return user, access_token

    @staticmethod
    def logout_user(db: Session, token: str) -> None:
        """Logout user by invalidating their session.

        For JWT-based auth, this is mainly a no-op on the backend since JWTs
        are stateless. The client should remove the token from storage.

        If session tracking is needed, we can add the token to a blacklist.

        Args:
            db: Database session
            token: JWT access token
        """
        # For MVP, JWT logout is handled client-side
        # In production, consider adding token to a blacklist or using refresh tokens
        pass

    @staticmethod
    def validate_token(token: str) -> Optional[dict]:
        """Validate a JWT token and return payload if valid.

        Args:
            token: JWT access token

        Returns:
            Token payload dict if valid, None otherwise
        """
        return decode_access_token(token)

    @staticmethod
    def get_user_from_token(db: Session, token: str) -> Optional[User]:
        """Get user from JWT token.

        Args:
            db: Database session
            token: JWT access token

        Returns:
            User if token is valid and user exists, None otherwise
        """
        payload = decode_access_token(token)
        if not payload:
            return None

        user_id_str = payload.get("sub")
        if not user_id_str:
            return None

        try:
            user_id = UUID(user_id_str)
        except ValueError:
            return None

        return DBService.get_user_by_id(db, user_id)

    @staticmethod
    def create_session(db: Session, user_id: UUID, expires_delta: Optional[timedelta] = None) -> SessionModel:
        """Create a database session for user (optional, for session tracking).

        Args:
            db: Database session
            user_id: User UUID
            expires_delta: Token expiration delta

        Returns:
            Session model
        """
        if expires_delta is None:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        expires_at = datetime.now(timezone.utc) + expires_delta
        token = create_access_token(data={"sub": str(user_id)}, expires_delta=expires_delta)

        return DBService.create_session(db, user_id, token, expires_at)

    @staticmethod
    def delete_session(db: Session, token: str) -> None:
        """Delete a session by token.

        Args:
            db: Database session
            token: Session token
        """
        DBService.delete_session(db, token)
