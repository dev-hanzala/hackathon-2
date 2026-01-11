"""Authentication middleware for Better Auth integration."""

from typing import Optional
from uuid import UUID

from fastapi import HTTPException, Request, status
from sqlalchemy.orm import Session

from src.db.models import Session as SessionModel
from src.services.db_service import DBService


async def get_current_user(request: Request, session: Session) -> UUID:
    """Extract and validate current user from request."""
    # Get token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )

    # Expected format: "Bearer <token>"
    try:
        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            raise ValueError("Invalid auth scheme")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )

    # Validate session token
    db_session = DBService.get_session_by_token(session, token)
    if not db_session or db_session.is_expired():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    return db_session.user_id


class AuthMiddleware:
    """Middleware for authentication."""

    @staticmethod
    def create_session(session: Session, user_id: UUID, token: str, expires_at) -> SessionModel:
        """Create a new session."""
        db_session = SessionModel(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        session.add(db_session)
        session.commit()
        session.refresh(db_session)
        return db_session

    @staticmethod
    def invalidate_session(session: Session, token: str) -> None:
        """Invalidate a session by token."""
        db_session = DBService.get_session_by_token(session, token)
        if db_session:
            session.delete(db_session)
            session.commit()

    @staticmethod
    def validate_token(session: Session, token: str) -> Optional[UUID]:
        """Validate a token and return user_id if valid."""
        db_session = DBService.get_session_by_token(session, token)
        if db_session and not db_session.is_expired():
            return db_session.user_id
        return None
